import streamlit as st
import pandas as pd
import os
import subprocess
import plotly.express as px

from streamlit_option_menu import option_menu
from get_cards_data import get_cards_data
from get_csv_data import get_csv
from get_csv_collection import get_csv_collec
from get_all_data import get_dataframes
from utils import dump_json, create_folder_if_not_exists, create_or_read_file
from os.path import join

# Parameters
LANGUAGES = ["fr"]
DUMP_TEMP_FILES = False
OUTPUT_FOLDER = "data"
TEMP_FOLDER = "temp"
INCLUDE_PROMO_CARDS = False
INCLUDE_UNIQUES = False
INCLUDE_KS = True
FORCE_INCLUDE_KS_UNIQUES = False 
INCLUDE_FOILERS = False
SKIP_NOT_ALL_LANGUAGES = False
COLLECTION_TOKEN=None

NAME_LANGUAGES = ["fr"]
ABILITIES_LANGUAGES = ["fr"]
MAIN_LANGUAGE = "fr"
GROUP_SUBTYPES = False
INCLUDE_WEB_ASSETS = False

CARDS_DATA_PATH = "data/cards.json"
COLLECTION_DATA_PATH = "data/collection.json"
FACTIONS_DATA_PATH = "data/factions.json"
TYPES_DATA_PATH = "data/types.json"
SUBTYPES_DATA_PATH = "data/subtypes.json"
RARITIES_DATA_PATH = "data/rarities.json"
CSV_OUTPUT_PATH = "data/cards_" + MAIN_LANGUAGE + ".csv"
CSV_COLLEC_OUTPUT_PATH = "data/collection_" + MAIN_LANGUAGE + ".csv"
ALL_CARDS_PATH = "data/cards_fr.csv"
MY_COLLECTION_PATH = "data/collection_fr.csv"
CSV_ALL_OUTPUT_PATH = "data/global_vision.csv"

saved_token = create_or_read_file("token.txt")

st.set_page_config(
    page_title= "PotoAltered",
                 layout="wide",
                 page_icon=":sparkles:",
                 menu_items={
        'Get Help': 'mailto:w_saturnin@gmail.com',
        'Report a bug': "https://github.com/WillyMaillot87/PotoAltered/issues",
        'About': "# PotoAltered. \n Une app très cool faite par Willy Maillot"}
        )

def run_script(saved_token):
    try :
        #get_cards_data :
        cards, types, subtypes, factions, rarities = get_cards_data()
        create_folder_if_not_exists(OUTPUT_FOLDER)
        dump_json(cards,    join(OUTPUT_FOLDER, 'cards.json'))
        dump_json(types,    join(OUTPUT_FOLDER, 'types.json'))
        dump_json(subtypes, join(OUTPUT_FOLDER, 'subtypes.json'))
        dump_json(factions, join(OUTPUT_FOLDER, 'factions.json'))
        dump_json(rarities, join(OUTPUT_FOLDER, 'rarities.json'))

        #get_collection_data :
        collection, types, subtypes, factions, rarities = get_cards_data(collection_token=saved_token)
        create_folder_if_not_exists(OUTPUT_FOLDER)
        dump_json(collection,    join(OUTPUT_FOLDER, 'collection.json'))

        #get_csv_data :
        get_csv()

        #get_csv_collection :
        get_csv_collec()

        #get_all_data
        get_dataframes(ALL_CARDS_PATH, MY_COLLECTION_PATH)

        st.success("Le chargement de la collection est terminé.")
    except subprocess.CalledProcessError as e:
        st.error(f"Erreur lors de l'execution du script : {e}")

def run():
### MENU ###
    selected = option_menu(
        menu_title=None,
        options=["Home", "Collection", "Tradable"],
        icons=["house", "collection", "arrow-left-right"],
        # menu_icon=None,
        orientation="horizontal"
    )

### HOME PAGE ###
    if selected == "Home" : 
        
        col1, col2 = st.columns(2)

        with col1 : 
            st.title("Bienvenue !")
            st.markdown("""Dans le but de pouvoir récupérer les données de ta collection personnelle, je t'invite à coller ton token JWT dans le champ ci-dessous. 
Ce token est directement envoyé à l'API d'Altered pour t'identifier et accéder à ta collection.
Le token n'est pas envoyé en ligne, il reste stocké uniquement sur ton application à toi.
Cette étape n'est à faire qu'une seule fois pour télécharger les données de ta collection.
                    
Ne communiques ton token à personne !
                    """)

            mini_col1, mini_col2 = st.columns(2, vertical_alignment="bottom")

            if "input_token" not in st.session_state:
                st.session_state["input_token"] = ""

            with mini_col1 :
                input_token = st.text_input("COLLER LE TOKEN ICI :", st.session_state["input_token"])
            
            with mini_col2 :
                submit = st.button("Charger la collection")

            if submit:
                st.session_state["input_token"] = input_token
                # st.write("Téléchargement en cours... BLA BLA BLA ... BIP BIP BOOP BIP...01001110100111010101010")
                # # Écrire le token dans le fichier .env
                # with open('.env', 'w') as f:
                #     f.write(f"TOKEN='{input_token}'")
                with open("token.txt", "w") as f:
                    f.write(input_token)
                st.write("Token sauvegardé")

                with open("token.txt", "r") as f:
                    saved_token = f.read()
            # # Bouton pour enregistrer le token dans le fichier .env et pour lancer les scripts
            # if submit:
            #     # Écrire le token dans le fichier .env
            #     with open('token.txt', 'w') as f:
            #         f.write(f"TOKEN={input_token}")
            #     st.write("Token sauvegardé !")

                # Executer les scripts
                run_script(saved_token)

        with col2 :
            st.image("images/PotoAltered.png", width=800)


### COLLECTION PAGE ###
    if selected == "Collection" : 

        if os.path.isfile("data/global_vision.csv") :
            df = pd.read_csv("data/global_vision.csv")    

            df['Forest-Mountain-Water'] = df[['forestPower', 'mountainPower', 'waterPower']].apply(lambda x: list(x), axis=1)

            new_names_fr = {'name_fr' : 'Nom',
                            'faction' : 'Faction', 
                            'collectorNumber' : 'Numéro',
                            'type' : 'Type', 
                            'rarity' : 'Rareté',
                            'handCost' : 'Coût de main', 
                            'reserveCost' : 'Coût de réserve', 
                            'Forest-Mountain-Water' : 'Forêt-Montagne-Eau',
                            'forestPower' : 'Fôret', 
                            'mountainPower' : 'Montagne', 
                            'waterPower' : 'Eau', 
                            'abilities_fr' : 'Capacité',
                            'supportAbility_fr' : 'Capacité de soutien',
                            'imagePath' : 'Image', 
                            'inMyCollection' : 'En possession', 
                            'Kickstarter' : 'Dont KS', 
                            'to_give' : 'En excès', 
                            'to_get' : 'Manquantes',
                            'progress' : 'Complétion'
                            }

            df = df.rename(columns = new_names_fr)

            column_order = ('Image',
                            'Nom',
                            'Faction',
                            'Type', 
                            'Rareté',
                            'En possession',
                            'Dont KS',
                            'En excès', 
                            'Manquantes',
                            'Complétion',
                            'Coût de main', 
                            'Coût de réserve', 
                            'Forêt-Montagne-Eau',
                            # 'Fôret', 
                            # 'Montagne', 
                            # 'Eau', 
                            'Capacité',
                            'Capacité de soutien',
                            'Numéro'
                            )

            # df_my_collec = df[(df['Rareté'] != 'Neutre') & (df['En possession'] > 0)]
            # st.bar_chart(df_my_collec, x="Rareté", y="En possession", color="Faction", stack=False)

            column_configuration = {
                'Complétion' : st.column_config.ProgressColumn(
                    "Complétion",
                    help="Progression sur l'atteinte du maximum par deck pour cette carte",
                    format="%d%%",
                    min_value=0,
                    max_value=100
                ),
                'Image': st.column_config.ImageColumn(
                    "Image", 
                    help="Aperçut de la carte. Double cliquer pour agrandir.",
                    width = "small"
                    ),
                }

            filter_col, df_col = st.columns([1, 4])
            
            with filter_col :
                columns_cat = ['Faction', 
                               'Rareté',
                               'Type']
                
                columns_string = ['Nom',
                                  'Numéro',
                                  'id']
                
                columns_int = ['En possession',
                               'Dont KS',
                               'En excès',
                               'Manquantes',
                               'Coût de main',
                               'Coût de réserve',
                               'Fôret',
                               'Montagne',
                               'Eau']
                
                columns_float = ['Complétion']
                
                columns_to_select = columns_cat + columns_string + columns_int + columns_float

                st.header(f"Filtres : ")

                df = df.copy()

                modification_container = st.container(border=True)

                with modification_container:
                    to_filter_columns = st.multiselect("Filtrer le tableau", columns_to_select)
                    for column in to_filter_columns:
                        left, right = st.columns((1, 20))
                        if column in columns_cat :
                            user_cat_input = right.multiselect(
                            f"Valeurs pour {column}",
                            df[column].unique(),
                            default=list(df[column].unique()),
                            )
                            df = df[df[column].isin(user_cat_input)]

                        elif column in columns_float:
                            _min = float(df[column].min())
                            _max = float(df[column].max())
                            step = (_max - _min) / 4
                            user_num_input = right.slider(
                                f"Valeurs pour {column}",
                                min_value=_min,
                                max_value=_max,
                                value=(_min, _max),
                                step=step,
                            )
                            df = df[df[column].between(*user_num_input)]

                        elif column in columns_int:
                            _min = int(df[column].min())
                            _max = int(df[column].max())
                            step = 1
                            user_num_input = right.slider(
                                f"Valeurs pour {column}",
                                min_value=_min,
                                max_value=_max,
                                value=(_min, _max),
                                step=step,
                            )
                            df = df[df[column].between(*user_num_input)]

                        else:
                            user_text_input = right.text_input(
                                f"Substring or regex in {column}",
                            )
                            if user_text_input:
                                df = df[df[column].astype(str).str.contains(user_text_input)]


                excess = st.button("Afficher les cartes en trop", use_container_width=True)
                missing = st.button("Afficher les cartes manquantes", use_container_width=True)
                st.button("Reset", use_container_width=True)

                if excess :
                    df = df[df['En excès'] > 0]
                if missing :
                    df = df[df['Manquantes'] > 0]
                else :
                    df = df

                # Download
                @st.cache_data
                def convert_df(df):
                    return df.to_csv(index=False).encode('utf-8')


                csv = convert_df(df)

                st.download_button(
                    "Press to Download",
                    csv,
                    "cartes_altered.csv",
                    "text/csv",
                    key='download-csv',
                    type="primary",
                    use_container_width=True
                    )

            with df_col :
                st.header("Collection")
                event = st.dataframe(df,
                column_config=column_configuration,
                column_order=column_order,
                use_container_width=True,
                hide_index=True,
                # on_select="rerun",
                # selection_mode="multi-row",
                )

            # cards = event.selection.rows
            # second_df = df[['Image','Nom','Faction','Rareté','Type','Numéro','En excès', 'Manquantes']].iloc[cards]

            # st.header(f"Cartes sélectionnées : {len(cards)}")
            # st.dataframe(second_df, column_config=column_configuration, use_container_width=True)
        

            st.header("Statistiques : ")
            stats, graph = st.columns([1, 2], vertical_alignment="center")
            
            shape_all = df.shape[0]
            shape_collec = df[df['En possession'] > 0].shape[0]

            with stats :
                st.markdown(f"**{shape_all}** cartes à collectionner")
                st.markdown(f"**{shape_collec}** cartes dans la collection")
                st.markdown(f"Collection complétée à **{(shape_collec / shape_all) * 100:.2f}** %")

            # Barplot :
            df_barplot = df[['Type','Rareté','En possession', 'En excès', 'Manquantes']]
            df_barplot['Max Deck'] = (df['En possession'] + df['Manquantes']) - df['En excès']

            df_barplot['Progression'] = (df_barplot['En possession'] - df_barplot['En excès']) / df_barplot['Max Deck']
            df_barplot = df_barplot.groupby(['Rareté', 'Type'])['Progression'].mean().reset_index()
            df_barplot = df_barplot.query("Type in ['Héros', 'Personnage', 'Sort', 'Permanent']")

            fig = px.bar(df_barplot, 
                        x='Progression', 
                        y='Rareté', 
                        color='Type', 
                        barmode='group',
                        text=df_barplot['Progression'].apply(lambda x: f"{x:.2%}")          
                        )

            fig.update_layout(barcornerradius=15,
                            #   showlegend=False,
                              xaxis_title=None,
                              yaxis_title=None,
                              height=350,
                              legend=dict(
                                y=0.5, x=-0.2  # Ajustez la valeur pour positionner la légende plus haut ou plus bas
                            ))


            with graph :
                st.plotly_chart(fig, use_container_width=True, theme="streamlit")

        else :
            st.error("La collection n'est pas créée. Merci d'ajouter votre token via la page 'Home'.")    

### TRADABLE PAGE ###     
    if selected == "Tradable" : 
        st.header("En construction :building_construction:")


        df_collection = df[df['En possession'] > 0].copy()
        df_collection.drop(['Coût de main',
                            'Coût de réserve',
                            'Fôret-Montagne-Eau',
                            'Capacité',
                            'Capacité de soutien',
                            'Numéro'],
                            axis=1,
                            inplace=True)

        left, right = st.columns([1, 1])

        with left:
            st.dataframe(df_collection,
                column_config=column_configuration,
                column_order=column_order,
                use_container_width=True,
                hide_index=True)

if __name__ == "__main__":
    run()
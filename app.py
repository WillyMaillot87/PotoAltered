import streamlit as st
from streamlit_option_menu import option_menu
import pandas as pd
import os
import subprocess


st.set_page_config(
    page_title= "PotoAltered",
                 layout="wide",
                 page_icon=":sparkles:",
                 menu_items={
        'Get Help': 'mailto:w_saturnin@gmail.com',
        'Report a bug': "mailto:w_saturnin@gmail.com",
        'About': "# PotoAltered. \n Une app très cool faite par Willy Maillot"}
        )

# add new and/or renamed tab in this ordered dict by
# passing the name in the sidebar as key and the imported tab
# as value as follow :

def run_script():
    try :
        subprocess.run(['bash', 'run_all.sh'])
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

            # # Bouton pour enregistrer le token dans le fichier .env et pour lancer les scripts
            # if submit:
            #     # Écrire le token dans le fichier .env
            #     with open('token.txt', 'w') as f:
            #         f.write(f"TOKEN={input_token}")
            #     st.write("Token sauvegardé !")

                # Executer les scripts
                run_script()

        with col2 :
            st.image("PotoAltered.png", width=800)


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
        





        else :
            st.error("La collection n'est pas créée. Merci d'ajouter votre token via la page 'Home'.")    

### TRADABLE PAGE ###     
    if selected == "Tradable" : 
        st.header("En construction :building_construction:")



if __name__ == "__main__":
    run()
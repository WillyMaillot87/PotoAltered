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
        st.success("La collection est téléchargée !")
    except subprocess.CalledProcessError as e:
        st.error(f"Erreur lors de l'execution du script : {e}")

def run():
    # MENU 
    selected = option_menu(
        menu_title=None,
        options=["Home", "Collection", "Tradable"],
        icons=["house", "collection", "arrow-left-right"],
        # menu_icon=None,
        orientation="horizontal"
    )

    # new_names_fr = {'name_fr' : 'Nom', 
    #          'collectorNumber' : 'Numéro', 
    #          'rarity' : 'Rareté',
    #          'handCost' : 'Coût de main', 
    #          'reserveCost' : 'Coût de réserve', 
    #          'forestPower' : 'Fôret', 
    #          'mountainPower' : 'Montagne', 
    #          'waterPower' : 'Eau', 
    #          'abilities_fr' : 'Capacité',
    #          'supportAbility_fr' : 'Capacité de soutien',
    #          'imagePath' : 'image', 
    #          'inMyCollection' : 'En possession', 
    #          'Kickstarter' : 'dont KS', 
    #          'to_give' : 'En excès', 
    #          'to_get' : 'Manquantes',
    #          'progress' : 'Progression'
    # }

    # df = df.rename(columns = new_names_fr)

### HOME PAGE ###
    if selected == "Home" : 
        
        col1, col2 = st.columns(2)

        with col1 : 
            st.title("Bienvenue !")
            st.text("""Dans le but de pouvoir récupérer les données de votre collection personnelle,
je vous invite à coller votre token JWT dans le champ ci-dessous. 
Ce token est directement envoyé à l'API d'Altered pour vous identifier et accéder à votre collection.
Le token n'est pas stocké dans l'application ni en local, ni en ligne.

Cette étape n'est à faire qu'une seule fois pour télécharger les données de votre collection.
                    
Ne communiquez votre token à personne !
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
                st.write("Téléchargement en cours... BLA BLA BLA ... BIP BIP BOOP BIP...01001110100111010101010")
                # Écrire le token dans le fichier .env
                with open('.env', 'w') as f:
                    f.write(f"TOKEN={input_token}")

            # Bouton pour enregistrer le token dans le fichier .env et pour lancer les scripts
            if submit:
                # Écrire le token dans le fichier .env
                with open('.env', 'w') as f:
                    f.write(f"TOKEN={input_token}")

                # Executer les scripts
                run_script()

        with col2 :
            st.image("PotoAltered.png", width=800)


### COLLECTION PAGE ###
    if selected == "Collection" : 

        if os.path.isfile("data/global_vision.csv") :
            df = pd.read_csv("data/global_vision.csv")    

            st.header("Collection")

            df_my_collection = df[df['inMyCollection'] > 0]

            # df_my_collection["image"] = df_my_collection["URL image"].apply(lambda x: st.image(x, width=80))
        
            column_configuration = {'name_fr' : 'Nom', 
                'collectorNumber' : 'Numéro',
                'faction' : 'Faction', 
                'rarity' : 'Rareté',
                'type' : 'Type',
                'handCost' : 'Coût de main', 
                'reserveCost' : 'Coût de réserve', 
                'forestPower' : 'Fôret', 
                'mountainPower' : 'Montagne', 
                'waterPower' : 'Eau', 
                'abilities_fr' : 'Capacité',
                'supportAbility_fr' : 'Capacité de soutien',
                'inMyCollection' : 'En possession', 
                'Kickstarter' : 'Dont KS', 
                'to_give' : 'En excès', 
                'to_get' : 'Manquantes',
                'progress' : st.column_config.ProgressColumn(
                    "Complétion (%)",
                    help="Progression sur l'atteinte du maximum par deck pour cette carte",
                    format="%d",
                    min_value=0,
                    max_value=100
                ),
                'imagePath': st.column_config.ImageColumn(
                    "Image", 
                    help="Aperçut de la carte. Double cliquer pour agrandir.",
                    width = "small"
                    )
                }
        
            
            tab1, tab2 = st.tabs(["Mes cartes", "Toutes les cartes"])

            with tab1: 
                event = st.dataframe(df_my_collection,
            column_config=column_configuration,
            use_container_width=True,
            hide_index=True,
            on_select="rerun",
            selection_mode="multi-row",
            )

            left, right = st.columns(2)

            with left : 
                st.header(f"Filtres : ")
                to_give = st.button("à donner")
                to_get = st.button("à récupérer")

            with right :    
                cards = event.selection.rows
                filtered_df = df_my_collection[['imagePath','name_fr','faction','rarity','type','collectorNumber','to_give', 'to_get']].iloc[cards]

                st.header(f"Cartes sélectionnées : {len(cards)}")

                st.dataframe(
            filtered_df,
            column_config=column_configuration,
            use_container_width=True,
            )

            df_all_cards = df[df['inMyCollection'] <= 0]
            df_all_cards = df_all_cards.drop(['inMyCollection', 'Kickstarter', 'to_give', 'to_get', 'progress', 'id'], axis=1)

            column_configuration_2 = {'name_fr' : 'Nom', 
                'collectorNumber' : 'Numéro',
                'faction' : 'Faction', 
                'rarity' : 'Rareté',
                'type' : 'Type',
                'handCost' : 'Coût de main', 
                'reserveCost' : 'Coût de réserve', 
                'forestPower' : 'Fôret', 
                'mountainPower' : 'Montagne', 
                'waterPower' : 'Eau', 
                'abilities_fr' : 'Capacité',
                'supportAbility_fr' : 'Capacité de soutien',
                'imagePath': st.column_config.ImageColumn(
                    "Image", 
                    help="Aperçut de la carte. Double cliquer pour agrandir.",
                    width = "small"
                    )
                }

            with tab2 :
                event = st.dataframe(df_all_cards,
            column_config=column_configuration_2,
            use_container_width=True,
            hide_index=True,
            on_select="rerun",
            selection_mode="multi-row",
            )

        else :
            st.error("La collection n'est pas créée. Merci d'ajouter votre token via la page 'Home'.")    

### TRADABLE PAGE ###     
    if selected == "Tradable" : 
        st.header("En construction :building_construction:")



if __name__ == "__main__":
    run()
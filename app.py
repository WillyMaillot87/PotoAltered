import streamlit as st
from streamlit_option_menu import option_menu
import pandas as pd


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



def run():
    # MENU 
    selected = option_menu(
        menu_title=None,
        options=["Home", "Collection", "Tradable"],
        icons=["house", "collection", "arrow-left-right"],
        # menu_icon=None,
        orientation="horizontal"
    )

### HOME PAGE ###
    if selected == "Home" : 
        st.image("PotoAltered.png", width=500)

        with st.sidebar:
            if "input_token" not in st.session_state:
                st.session_state["input_token"] = ""
        
            input_token = st.text_input("Coller le token ici pour charger la collection :", st.session_state["input_token"])
            submit = st.button("Charger la collection")
            if submit:
                st.session_state["input_token"] = input_token
                st.write("Téléchargement en cours... BLA BLA BLA ... BIP BIP BOOP BIP...01001110100111010101010")


### COLLECTION PAGE ###
    if selected == "Collection" : 
            st.header("Collection")
 
            st.write("J'ai plein de jolies cartes <3")

            df_my_collection = pd.read_csv("src/data/global_vision.csv")

        # st.image(
        #         "https://s3-us-west-2.amazonaws.com/uw-s3-cdn/wp-content/uploads/sites/6/2017/11/04133712/waterfall.jpg",
        #         width=400, # Manually Adjust the width of the image as per requirement
        #     )

        # df_my_collection[‘URL image’] = df.apply( lambda x: show_image_from_url(x[‘image_url’]), axis = 1 )

            column_configuration = {
            "name": st.column_config.TextColumn(
                "Name", help="The name of the user", max_chars=100, width="medium"
            ),
            "activity": st.column_config.LineChartColumn(
                "Activity (1 year)",
                help="The user's activity over the last 1 year",
                width="large",
                y_min=0,
                y_max=100,
            ),
            "daily_activity": st.column_config.BarChartColumn(
                "Activity (daily)",
                help="The user's activity in the last 25 days",
                width="medium",
                y_min=0,
                y_max=1,
            ),
            }

            event = st.dataframe(df_my_collection,
            column_config=column_configuration,
            use_container_width=True,
            hide_index=True,
            on_select="rerun",
            selection_mode="multi-row",
            )

            st.header("Cartes sélectionnées")
            cards = event.selection.rows
            filtered_df = df_my_collection.iloc[cards]

            st.dataframe(
            filtered_df,
            column_config=column_configuration,
            use_container_width=True,
            )


### TRADABLE PAGE ###     
    if selected == "Tradable" : 
        st.header("Under construction :building_construction:")



if __name__ == "__main__":
    run()
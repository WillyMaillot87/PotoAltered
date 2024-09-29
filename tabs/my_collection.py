import streamlit as st
import pandas as pd

sidebar_name = "Ma collection"

def run():
    st.header("Collection")
    st.write("J'ai plein de jolies cartes <3")

    df_my_collection = pd.read_csv("src/data/global_vision.csv")

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

    ## SEE https://docs.streamlit.io/develop/tutorials/elements/dataframe-row-selections#use-charts-to-visualize-the-activity-comparison
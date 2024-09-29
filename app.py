from collections import OrderedDict
import streamlit as st
from tabs import main_page, all_cards, my_collection


st.set_page_config(
    page_title= "PotoAltered", page_icon="🔥")

# add new and/or renamed tab in this ordered dict by
# passing the name in the sidebar as key and the imported tab
# as value as follow :

TABS = OrderedDict(
    [
        (main_page.sidebar_name, main_page),
        (my_collection.sidebar_name, my_collection),
        (all_cards.sidebar_name, all_cards),
    ]
)

def run():

    tab_name = st.sidebar.radio("", list(TABS.keys()), 0, key="tab_selector")

    tab = TABS[tab_name]

    tab.run()


if __name__ == "__main__":
    run()
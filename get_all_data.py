# Script by Willy MAILLOT
# MIT License

import os
import pandas as pd
import numpy as np

#PARAMETERS
ALL_CARDS_PATH = "data/cards_fr.csv"
MY_COLLECTION_PATH = "data/collection_fr.csv"
CSV_OUTPUT_PATH = "data/global_vision.csv"

def check_KS(id):
    '''Identify the Kickstarter edition'''
    if "CORE_B" in id :
        return 0
    elif "COREKS_B" in id :
        return 1
    else :
        pass

def concat_strings(col):
    '''Join the strings when grouping data'''
    elements_uniques = set(col)
    return ' / '.join(elements_uniques)

def get_dataframes(all_cards_path, my_collection_path):

    if not os.path.exists(ALL_CARDS_PATH):
        print(f"File {ALL_CARDS_PATH} not found. Have you run get_cards_data.py?")
        return
    if not os.path.exists(MY_COLLECTION_PATH):
        print(f"File {MY_COLLECTION_PATH} not found. Have you run get_cards_data.py?")
        return
    
    all_cards = pd.read_csv(all_cards_path)
    print("shape matrix 'all cards' = ", all_cards.shape)

    my_collection = pd.read_csv(my_collection_path)
    print("shape matrix 'my collection' = ", my_collection.shape)

    ## Pre-processing **all_cards** dataframe
    my_collection['Kickstarter'] = my_collection['id'].apply(check_KS)

    cols_to_drop = [
        'handCost',
        'reserveCost',
        'forestPower',
        'mountainPower',
        'waterPower',
        'landmarksSize',
        'reserveSize',
        'abilities_fr',
        'supportAbility_fr']

    my_collection.drop(cols_to_drop, axis=1, inplace=True)

    # Grouping the cards by 'collectorNumber'


    cols_agg_func = {"name_fr" : concat_strings,
                    "faction" : concat_strings, 
                    "rarity" : concat_strings, 
                    "type" : concat_strings, 
                    "inMyCollection" : 'sum', 
                    "Kickstarter" : 'sum'}

    df_collec = my_collection.groupby("collectorNumber").agg(cols_agg_func).reset_index()

    # show max cards allowed in a deck :
    df_collec['max_card'] = df_collec['type'].apply(lambda x: 1 if x == 'Héros' else 3) 

    #show cards to trade :
    df_collec['cards_to_trade'] = df_collec['inMyCollection'] - df_collec['max_card'] 

    df_collec.drop(columns = ['faction', 'rarity', 'type'], axis = 1, inplace = True) # supprimer les colonnes inutiles

    # show number of cards in excess :
    df_collec['to_give'] = 0
    df_collec.loc[df_collec['cards_to_trade'] >= 0, 'to_give'] = df_collec['cards_to_trade'][df_collec['cards_to_trade'] >= 0]

    # show number of missing cards :
    df_collec['to_get'] = 0
    df_collec.loc[df_collec['cards_to_trade'] < 0, 'to_get'] = np.abs(df_collec['cards_to_trade'][df_collec['cards_to_trade'] < 0])


    ## Pre-processing **all_cards** dataframe
    all_cards.drop(columns=['landmarksSize', 'reserveSize'], axis = 1, inplace = True )
    all_cards = all_cards.astype('str')
    list_col_allcards = all_cards.columns.to_list()
    list_col_allcards.pop(0) #remove 'collectorNumber' from the list
    list_col_allcards.pop(-1) #remove 'imagePath' from the list

    cols_agg_func2 = {col : concat_strings for col in list_col_allcards}
    cols_agg_func2['imagePath'] = 'first'

    df_all_cards = all_cards.groupby('collectorNumber').agg(cols_agg_func2).reset_index()


    ## Merging the two dataframes :
    print("merging the dataframes...")

    df = df_all_cards.merge(df_collec[['collectorNumber',
                                    'inMyCollection',
                                    'Kickstarter',
                                    'to_give',
                                    'to_get']], left_on='collectorNumber', right_on='collectorNumber', how='left')

    df = df.fillna(0)

    df.to_csv(CSV_OUTPUT_PATH, index=False)
    print(f"global_vision dataframe {df.shape} is ready ({CSV_OUTPUT_PATH})")

if __name__ == "__main__":
    get_dataframes(ALL_CARDS_PATH, MY_COLLECTION_PATH)
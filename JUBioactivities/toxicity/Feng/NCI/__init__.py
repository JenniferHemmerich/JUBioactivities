import os.path
import pandas as pd
from .... import utils


__data_src__ = [os.path.join(__path__[0], 'activities.csv')]


def read_data(raw=False):
    df = pd.read_csv(__data_src__[0], index_col=1, usecols=['Smiles','Potency'])
    df.columns = ['NCI_AIDS_Pot_Feng']
    df.index = utils.convert_index(df.index)

    if raw:
        return df

    df = utils.drop_rows(df)
    df = utils.handle_duplicates(df, type='mult')
    df = utils.one_hot_encode(df, cols=['NCI_AIDS_Pot_Feng'])
    return df

def read_structures(raw=False):
    df = pd.read_csv(__data_src__[0], usecols=['Smiles'])
    df = df.set_index('Smiles', drop=False)
    df.index = utils.convert_index(df.index)
    if raw:
        return df
    df = utils.drop_rows(df)
    df = utils.handle_duplicates(df, type='str')
    return df
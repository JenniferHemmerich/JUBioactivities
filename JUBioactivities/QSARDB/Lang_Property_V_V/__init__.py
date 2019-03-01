import os.path
import pandas as pd
from ... import utils


__data_src__ = [os.path.join(__path__[0], "V.csv")]


def read_data(raw=False):
    df = pd.read_csv(__data_src__[0], index_col=0, usecols=['SMILES', 'V'])
    df.columns = ["Property_V_Lang"]
    df.index = utils.convert_index(df.index)

    if raw:
        return df

    df = utils.drop_rows(df)
    df = utils.handle_duplicates(df, type='cont')
    return df


def read_structures(raw=False):
    df = pd.read_csv(__data_src__[0], index_col=0, usecols=['SMILES'])
    new_index = utils.convert_index(df.index)
    df.reset_index(inplace=True)
    df.index = new_index

    if raw:
        return df

    df = utils.drop_rows(df)
    df = utils.handle_duplicates(df, type='str')
    df.columns = ['Smiles']

    return df

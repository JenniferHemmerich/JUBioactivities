import os.path
import pandas as pd
from ... import utils


__data_src__ = [os.path.join(__path__[0], "Compounds.csv")]


def read_data(raw=False):
    df = pd.read_csv(__data_src__[0], index_col=0, usecols=['SMILES', "Bioactivity*"])
    df.index = utils.convert_index(df.index)

    if raw:
        return df

    df = utils.drop_rows(df)
    df = utils.handle_duplicates(df, type='bin')
    df.columns = ['DILI_Zhang']
    return df

def read_structures(raw=False):
    df = pd.read_csv(__data_src__[0], usecols=['SMILES'])
    df.columns = ['Smiles']
    df = df.set_index('Smiles', drop=False)
    df.index = utils.convert_index(df.index)

    if raw:
        return df

    df = utils.drop_rows(df)
    df = utils.handle_duplicates(df, type='str')
    return df

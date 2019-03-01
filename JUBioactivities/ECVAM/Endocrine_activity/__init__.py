import os.path
import pandas as pd
from ... import utils


__data_src__ = [os.path.join(__path__[0], "Classes.csv")]

def read_HH(raw=False):
    df = pd.read_csv(__data_src__[0], index_col=0, usecols=['Smiles', 'Class_HH'])

    if raw:
        return df

    df.index = utils.convert_index(df.index)
    df = utils.drop_rows(df)
    df = utils.handle_duplicates(df, type='bin')
    df.columns = ['HH_ED_ECVAM']
    return df


def read_WL(raw=False):
    df = pd.read_csv(__data_src__[0], index_col=0, usecols=['Smiles', 'Class_WL'])
    df.index = utils.convert_index(df.index)

    if raw:
        return df

    df = utils.drop_rows(df)
    df = utils.handle_duplicates(df, type='bin')
    df.columns = ['WL_ED_ECVAM']
    return df

def read_data(raw=False):
    df = pd.concat([read_HH(raw), read_WL(raw)],axis=1)
    return df

def read_structures(raw=False):
    df = pd.read_csv(__data_src__[0], usecols=['Smiles'])
    df.columns = ['Smiles']
    df = df.set_index('Smiles', drop=False)
    df.index = utils.convert_index(df.index)

    if raw:
        return df

    df = utils.drop_rows(df)
    df = utils.handle_duplicates(df, type='str')
    return df

import os.path
import pandas as pd
from ... import utils


__data_src__ = [os.path.join(__path__[0], "solubility.txt")]


def read_data(raw=False):
    df = pd.read_csv(__data_src__[0], delimiter=',', index_col=1,
                     usecols=['SMILES','measured log(solubility:mol/L)'], engine='python')
    df.index = utils.convert_index(df.index, filenames=False)
    if raw:
        return df

    df = utils.drop_rows(df)
    df = utils.handle_duplicates(df,type='cont')
    df.columns = ['solubilityD_QSPR']
    return df


def read_structures(raw=False):
    df = pd.read_csv(__data_src__[0], usecols=['SMILES'], engine='python')
    df = df.set_index('SMILES', drop=False)
    df.index = utils.convert_index(df.index, filenames=False)
    if raw:
        return df

    df = utils.drop_rows(df)
    df = utils.handle_duplicates(df,type='str')
    df.columns = ['Smiles']
    return df
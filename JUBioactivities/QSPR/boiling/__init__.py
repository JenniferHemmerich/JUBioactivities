import os.path
import pandas as pd
from ... import utils


__data_src__ = [os.path.join(__path__[0],f) for f in ["a2_tr.txt"]]


def read_data(raw=False):
    df = pd.read_csv(__data_src__[0], delimiter=',', index_col=0,
                     names=['Smiles','BP_QSPR','drop'], engine='python').drop('drop', axis=1)
    df.index = utils.convert_index(df.index, filenames=False)
    if raw:
        return df

    df = utils.drop_rows(df)
    df = df.apply(pd.to_numeric,errors='coerce')
    df = utils.handle_duplicates(df, type='cont')
    return df

def read_structures(raw=False):
    df = pd.read_csv(__data_src__[0], delimiter=',',
                     names=['Smiles','BP_QSPR','drop'], engine='python').drop(['drop','BP_QSPR'],axis=1)
    df = df.set_index('Smiles', drop=False)
    df.index = utils.convert_index(df.index, filenames=False)
    if raw:
        return df

    df = utils.drop_rows(df)
    df = utils.handle_duplicates(df, type='str')
    return df



import os.path
import pandas as pd
from ... import utils


__data_src__ = [os.path.join(__path__[0], "bbp2.smi")]


def read_data(raw=False):
    df = pd.read_csv(__data_src__[0],sep='    ', index_col=0, names=['SMILES', 'No', 'Name', 'BBB_perm', 'Ref'], engine='python')\
        .drop(['No', 'Name', 'Ref'], axis=1)
    df.index = utils.convert_index(df.index)

    if raw:
        return df

    df = utils.drop_rows(df)
    df = utils.convert_to_classes(df, 'p', 'n')
    df = utils.handle_duplicates(df, type='bin')
    return df


def read_structures(raw=False):
    df = pd.read_csv(__data_src__[0], sep='    ', names=['SMILES', 'No', 'Name', 'BBB_perm', 'Ref'], engine='python').\
        drop(['No', 'Name', 'BBB_perm', 'Ref'], axis=1)
    df.index = df['SMILES']
    df.index = utils.convert_index(df.index)
    df.columns = ['Smiles']

    if raw:
        return df

    df = utils.drop_rows(df)
    df = utils.handle_duplicates(df, type='str')
    return df

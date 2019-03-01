import os.path, glob
import pandas as pd
from ... import utils


__data_src__ = glob.glob(os.path.join(__path__[0], "*.dat"))

def _read_d(file, raw=False):
    df = pd.read_csv(file,names=['Name','_Herg_toxicity','Smiles'],index_col=2).drop('Name',axis=1)
    df.index = utils.convert_index(df.index)
    if raw:
        return df
    df = utils.drop_rows(df)
    df = utils.handle_duplicates(df, type='cont')
    return df

def _read_s(file, raw=False):
    df = pd.read_csv(file, index_col=2, names=['Name', '_Herg_toxicity', 'Smiles']).drop('Name', axis=1)
    new_index = utils.convert_index(df.index)
    df = df.reset_index().drop('_Herg_toxicity', axis=1)
    df = df.set_index(new_index)
    if raw:
        return df
    df = utils.drop_rows(df)
    df = utils.handle_duplicates(df, type='str')
    return df


def read_data(raw=False):
    df = pd.concat([_read_d(f,raw) for f in __data_src__])
    return df

def read_structures(raw=False):
    df = pd.concat([_read_s(f,raw) for f in __data_src__])
    return df



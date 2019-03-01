import os.path, glob
import pandas as pd
from ... import utils


__data_src__ = glob.glob(os.path.join(__path__[0], "*.sdf"))


def read_data(raw=False):
    df = utils.read_labelled_molecules(__data_src__[0], key='Activity')
    if raw:
        return df

    df = utils.drop_rows(df)
    df = df.astype('int')
    df = utils.handle_duplicates(df, type='bin')
    df.columns = ['Ames_Hansen']
    return df

def read_structures(raw=False):
    df = utils.read_labelled_molecules(__data_src__[0], key='Activity', structures=True)
    if raw:
        return df
    df = utils.drop_rows(df)
    df = utils.handle_duplicates(df, type='str')
    return df


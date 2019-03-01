import os.path
import pandas as pd
from .... import utils


__data_src__ = [os.path.join(__path__[0], x) for x in ["toxx2_new.sdf"]]



def read_data(raw=False):
    df = utils.read_labelled_molecules(__data_src__[0], key='LIC50', name='LIC50_Feng_Tox')
    if raw:
        return df

    df = utils.drop_rows(df)
    df = df.apply(pd.to_numeric)
    df = utils.handle_duplicates(df, type='cont')
    return df

def read_structures(raw=False):
    df = utils.read_labelled_molecules(__data_src__[0], key='EXTREG', name='Name', structures=True)
    if raw:
        return df

    df = utils.drop_rows(df)
    df = utils.handle_duplicates(df, type='str')
    return df
import os.path
import pandas as pd
from .... import utils


__data_src__ = [os.path.join(__path__[0], x) for x in ["Mut_all.sdf","bcut_3.txt"]]


def read_data(raw=False):
    df = utils.read_labelled_molecules(__data_src__[0], key='EXTREG', name='Name')
    a = pd.read_csv(__data_src__[1], sep="    ",usecols=['Name','Activity'],engine='python')
    df = df.reset_index().merge(a, how='inner', on=['Name']).set_index('InchiKey').drop('Name',axis=1)
    df.columns = ['Mut_Feng']
    if raw:
        return df

    df = utils.drop_rows(df)
    df = utils.handle_duplicates(df, type='bin')
    return df


def read_structures(raw=False):
    df = utils.read_labelled_molecules(__data_src__[0], key='EXTREG', name='Name', structures=True)
    if raw:
        return df

    df = utils.drop_rows(df)
    df = utils.handle_duplicates(df, type='str')
    return df
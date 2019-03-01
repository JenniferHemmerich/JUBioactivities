import os.path
import pandas as pd
from ... import utils


__data_src__ = [os.path.join(__path__[0], x) for x in ["structures.sdf", "Activity.txt"]]


def read_data(raw=False):
    df = pd.read_csv(__data_src__[1], sep=",", usecols=['permeability'])
    df.index = utils.convert_index([__data_src__[0]] * len(df), filenames=True)
    df.columns = ['Perm_CACO2_Ekins']

    if raw:
        return df

    df = utils.drop_rows(df)
    df = utils.handle_duplicates(df, type='cont')
    return df


def read_structures(raw=False):
    df = utils.read_labelled_molecules(__data_src__[0], key=None, structures=True)
    df.index = utils.convert_index([__data_src__[0]] * len(df), filenames=True)

    if raw:
        return df

    df = utils.drop_rows(df)
    df = utils.handle_duplicates(df, type='str')
    return df
import os.path, glob
import pandas as pd
from ... import utils


__data_src__ = glob.glob(os.path.join(__path__[0], "*.sdf"))


def read_bin(raw=False):
    keys = ["SAL", "Canc"]
    cols = ["Ames_ISSCAN", "Carc_ISSCAN"]

    df = utils.read_labelled_molecules(__data_src__[0], key=keys, name=cols)
    if raw:
        return df

    df = utils.drop_rows(df)
    df = utils.convert_to_classes(df, "3", "1")
    df = utils.handle_duplicates(df, type='bin')
    return df

def read_reg(raw=False):
    keys = ["TD50_Rat", "TD50_Mouse"]
    cols = ["TD50_Rat_ISSCAN", "TD50_Mouse_ISSCAN"]
    df = utils.read_labelled_molecules(__data_src__[0], key=keys, name=cols)
    if raw:
        return df

    df = utils.drop_rows(df)
    df = df.apply(pd.to_numeric, errors='coerce')
    df = utils.handle_duplicates(df, type='cont')

    return df


def read_data(raw=False):
    df = pd.concat([read_bin(raw),read_reg(raw)], axis=1)
    return df


def read_structures(raw=False):
    df = utils.read_labelled_molecules(__data_src__[0], key='', structures=True)
    if raw:
        return df
    df = utils.drop_rows(df)
    df = utils.handle_duplicates(df, type='str')
    return df



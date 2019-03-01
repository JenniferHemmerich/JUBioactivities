import os.path, glob
import pandas as pd
from ... import utils


__data_src__ = sorted(glob.glob(os.path.join(__path__[0], "*.sdf")))

def read_kOH(raw=False):
    df = utils.read_labelled_molecules(__data_src__[0], key='logkOH_EXP', name='LogkOH_Q17_22b_0056')

    if raw:
        return df

    df = utils.drop_rows(df)
    df = df.astype('float')
    df = utils.handle_duplicates(df, type='cont')
    return df


def read_OH(raw=False):
    df = utils.read_labelled_molecules(__data_src__[1], key='logOH_exp', name='LogOH')

    if raw:
        return df

    df = utils.drop_rows(df)
    df = df.astype('float')
    df = utils.handle_duplicates(df, type='cont')
    return df

def read_data(raw=False):
    df = pd.concat([read_OH(raw), read_kOH(raw)], axis=1)

    return df


def read_kOH_structures(raw=False):
    df = utils.read_labelled_molecules(__data_src__[0], key='logkOH_EXP', name='LogkOH', structures=True)

    if raw:
        return df

    df = utils.drop_rows(df)
    df = utils.handle_duplicates(df, type='str')
    return df


def read_OH_structures(raw=False):
    df = utils.read_labelled_molecules(__data_src__[1], key='logOH_exp', name='LogOH', structures=True)

    if raw:
        return df

    df = utils.drop_rows(df)
    df = utils.handle_duplicates(df, type='str')
    return df


def read_structures(raw=False):
    df = pd.concat([read_kOH_structures(raw), read_OH_structures(raw)])

    if raw:
        return df

    df = utils.handle_duplicates(df, type='str')
    return df


import os.path, glob
import pandas as pd
from ... import utils


__data_src__ = glob.glob(os.path.join(__path__[0], "*.sdf"))


def _read_d(file, raw=False):
    df = utils.read_labelled_molecules(file, key='Log Koc Exp', name='LogKOC_Q17_26_0057')
    if raw:
        return df

    df = utils.drop_rows(df)
    df = df.astype('float')
    df = utils.handle_duplicates(df, type='cont')
    return df


def _read_s(file, raw=False):
    df = utils.read_labelled_molecules(file, key='Log Koc Exp', name='LogKOC_Q17_26_0057', structures=True)
    if raw:
        return df
    df = utils.drop_rows(df)
    df = utils.handle_duplicates(df, type='str')
    return df


def read_data(raw=False):
    df = pd.concat([_read_d(f, raw) for f in __data_src__])
    if raw:
        return df
    df = utils.handle_duplicates(df, type='cont')

    return df


def read_structures(raw=False):
    df = pd.concat([_read_s(f, raw) for f in __data_src__])
    if raw:
        return df
    df= utils.handle_duplicates(df, type='str')
    return df

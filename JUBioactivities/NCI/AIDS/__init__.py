import os.path
import pandas as pd
from ... import utils
import glob


__data_src__ = list(sorted(glob.glob(os.path.join(__path__[0], "*.csv"))))


def read_classes(raw=False):
    df = pd.read_csv(__data_src__[0], index_col=0, usecols=['Standard_InChI', 'Class'])
    df = utils.index_from_inchicode(df)

    if raw:
        return df

    df = utils.drop_rows(df)
    df = utils.handle_duplicates(df, type='bin')

    return df


def read_pEC50(raw=False):
    df = pd.read_csv(__data_src__[1], index_col=1, usecols=["Log10EC50", "Standard_InChI"])
    df = utils.index_from_inchicode(df)

    if raw:
        return df

    df = utils.drop_rows(df)
    df = utils.handle_duplicates(df, type='cont')

    return df


def read_data(raw=False):
    df = pd.concat([read_pEC50(raw), read_classes(raw)], axis=1)

    return df


def read_structures_classes(raw=False):
    df = pd.read_csv(__data_src__[0], index_col=0, usecols=["Standard_InChI"])
    df = utils.index_from_inchicode(df, smiles=True)

    if raw:
        return df

    df = utils.drop_rows(df)
    df = utils.handle_duplicates(df, type='str')

    return df


def read_structures_pEC50(raw=False):
    df = pd.read_csv(__data_src__[1], index_col=0, usecols=["Standard_InChI"])
    df = utils.index_from_inchicode(df, smiles=True)

    if raw:
        return df

    df = utils.drop_rows(df)
    df = utils.handle_duplicates(df, type='str')

    return df


def read_structures(raw=False):
    df = pd.concat([read_structures_classes(raw), read_structures_pEC50(raw)])

    if raw:
        return df

    df = utils.drop_rows(df)
    df = utils.handle_duplicates(df, type='str')

    return df

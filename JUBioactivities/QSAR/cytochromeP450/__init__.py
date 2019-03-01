import os.path
import pandas as pd
import numpy as np
from ... import utils


__data_src__ = [os.path.join(__path__[0], f)
                for f in ('CYP2C9_dataset.csv', 'CYP3A4_dataset.csv')]


def read_cyp2c9(raw=False):
    df = pd.read_csv(__data_src__[0], index_col=0, usecols=['SMILES', 'Class'])
    df.rename(columns={'Class': 'CYP2C9_active'}, inplace=True)

    inchi_index = utils.convert_index(df.index)
    df.index = inchi_index

    if raw:
        return df

    df = utils.drop_rows(df)
    df = utils.convert_to_classes(df, 'Active', 'Inactive')
    df = utils.handle_duplicates(df, type='bin')

    return df

def read_cyp3a4(raw=False):
    df = pd.read_csv(__data_src__[1], index_col=0, usecols=['SMILES', 'Class'])
    df.rename(columns={'Class': 'CYP3A4_active'}, inplace=True)
    inchi_index = utils.convert_index(df.index)
    df.index = inchi_index

    if raw:
        return df

    df = utils.drop_rows(df)
    df = utils.convert_to_classes(df, 'Active', 'Inactive')
    df = utils.handle_duplicates(df, type='bin')

    return df


def read_cyp2c9_structures(raw=False):
    df = pd.read_csv(__data_src__[0], index_col=0, usecols=['SMILES'])
    inchi_index = utils.convert_index(df.index)
    df = df.reset_index()
    df.index = inchi_index

    if raw:
        return df

    df = utils.drop_rows(df)
    df = utils.handle_duplicates(df, type='str')
    df.columns = ['Smiles']

    return df


def read_cyp3a4_structures(raw=False):
    df = pd.read_csv(__data_src__[1], index_col=0, usecols=['SMILES'])
    inchi_index = utils.convert_index(df.index)
    df = df.reset_index()
    df.index = inchi_index

    if raw:
        return df

    df = utils.drop_rows(df)
    df = utils.handle_duplicates(df, type='str')
    df.columns = ['Smiles']

    return df


def read_data(raw=False):
    cyp2c9 = read_cyp2c9(raw)
    cyp3a4 = read_cyp3a4(raw)

    return pd.concat([cyp2c9, cyp3a4], axis=1)


def read_structures(raw=False):
    cyp2c9 = read_cyp2c9_structures(raw)
    cyp3a4 = read_cyp3a4_structures(raw)
    df = pd.concat([cyp2c9, cyp3a4])
    if raw:
        return df
    return utils.handle_duplicates(df, type='str')

import os.path
import pandas as pd
import numpy as np
from ... import utils


__data_src__ = [os.path.join(__path__[0], f)
                for f in ('biodeg_train.csv', 'biodeg_test.csv')]


def read_data(raw=False):
    train = pd.read_csv(__data_src__[0], index_col=0, usecols=['Smiles', 'Class'])
    test = pd.read_csv(__data_src__[1], index_col=0, usecols=['Smiles', 'class'])
    train.rename(columns={'Class': 'biodeg_class'}, inplace=True)
    test.rename(columns={'class': 'biodeg_class'}, inplace=True)
    df = pd.concat([train, test], axis=0)
    df.index = utils.convert_index(df.index)

    if raw:
        return df

    df = utils.drop_rows(df)
    df = utils.convert_to_classes(df,'RB','NRB')
    df = utils.handle_duplicates(df, type='bin')

    return df


def read_structures(raw=False):
    train = pd.read_csv(__data_src__[0], index_col=0, usecols=['Smiles'])
    test = pd.read_csv(__data_src__[1], index_col=0, usecols=['Smiles'])
    df = pd.concat([train, test], axis=0)
    inchi_index = utils.convert_index(df.index)
    df = df.reset_index()
    df.index = inchi_index

    if raw:
        return df

    df = utils.drop_rows(df)
    df = utils.handle_duplicates(df, type='str')

    return df

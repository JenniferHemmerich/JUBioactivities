import os.path
import pandas as pd
from ... import utils


__data_src__ = [os.path.join(__path__[0], f)
                for f in ('Training.csv', 'Validation.csv')]


def read_data(raw=False):
    train = pd.read_csv(__data_src__[0], index_col=1, names=['Name', 'Smiles', 'meltingB']).drop('Name', axis=1)
    test = pd.read_csv(__data_src__[1], index_col=1, names=['Name', 'Smiles', 'meltingB']).drop('Name', axis=1)

    df = pd.concat([train, test], axis=0)
    inchi_index = utils.convert_index(df.index)
    df.index = inchi_index

    if raw:
        return df

    df = utils.drop_rows(df)
    df = utils.handle_duplicates(df, type='cont')

    return df

def read_structures(raw=False):
    train = pd.read_csv(__data_src__[0], names=['Name', 'Smiles', 'meltingB']).drop(['Name','meltingB'], axis=1)
    test = pd.read_csv(__data_src__[1], names=['Name', 'Smiles', 'meltingB']).drop(['Name','meltingB'], axis=1)

    df = pd.concat([train, test], axis=0)
    df = df.set_index('Smiles', drop=False)
    df.index = utils.convert_index(df.index)

    if raw:
        return df
    df = utils.drop_rows(df)
    df = utils.handle_duplicates(df, type='str')

    return df
import os.path
import pandas as pd
from ... import utils


__data_src__ = [os.path.join(__path__[0], "mutagen.tab")]


def read_data(raw=False):
    df = pd.read_csv(__data_src__[0], sep="\t", index_col=1, names=["Cas", 'Smiles', "Mutagen_helma"]).drop('Cas', axis=1)
    df.index = utils.convert_index(df.index)

    if raw:
        return df

    df = utils.drop_rows(df)
    df = utils.handle_duplicates(df, type='bin')
    return df

def read_structures(raw=False):
    df = pd.read_csv(__data_src__[0],sep="\t", index_col=1, names=["Cas", 'Smiles', "Mutagen_helma"]).drop(['Cas','Mutagen_helma'],axis=1)
    inchi_index = utils.convert_index(df.index)
    df = df.reset_index()
    df.index = inchi_index

    if raw:
        return df

    df = utils.drop_rows(df)
    df = utils.handle_duplicates(df, type='str')
    return df

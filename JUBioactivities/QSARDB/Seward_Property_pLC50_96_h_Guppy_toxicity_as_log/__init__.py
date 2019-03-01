import os.path
import pandas as pd
from ... import utils
import glob


__data_src__ = [os.path.join(__path__[0], "compounds/InChI_from_XML.csv")]
__data_src__ += list(sorted(glob.glob(os.path.join(__path__[0], "properties/*.txt"))))

def read_moa(raw=False):
    dat = pd.read_csv(__data_src__[0], index_col=0)
    prop = pd.read_csv(__data_src__[1], index_col=0, sep="\t")
    prop.columns = ['MOA_96_Seward']

    df = pd.concat([dat, prop], axis=1)
    df = df.set_index('InchiCode')
    df = utils.index_from_inchicode(df)

    if raw:
        return df

    df = utils.drop_rows(df)
    df = utils.handle_duplicates(df, type='mult')
    df = utils.one_hot_encode(df, cols=['MOA_96_Seward'])


    return df


def read_pIGC50(raw=False):
    dat = pd.read_csv(__data_src__[0], index_col=0)
    prop = pd.read_csv(__data_src__[2], index_col=0, sep="\t")
    prop.columns = ['pIGC50_96_Seward']

    df = pd.concat([dat, prop], axis=1)
    df = df.set_index('InchiCode')
    df = utils.index_from_inchicode(df)

    if raw:
        return df

    df = utils.drop_rows(df)
    df = utils.handle_duplicates(df, type='cont')

    return df

def read_pLC50(raw=False):
    dat = pd.read_csv(__data_src__[0], index_col=0)
    prop = pd.read_csv(__data_src__[3], index_col=0, sep="\t")
    prop.columns = ['pLC50_96_Seward']

    df = pd.concat([dat, prop], axis=1)
    df = df.set_index('InchiCode')
    df = utils.index_from_inchicode(df)

    if raw:
        return df

    df = utils.drop_rows(df)
    df = utils.handle_duplicates(df, type='cont')

    return df


def read_data(raw=False):

    df = pd.concat([read_moa(raw), read_pIGC50(raw), read_pLC50(raw)],axis=1)
    return df


def read_structures(raw=False):
    df = pd.read_csv(__data_src__[0], index_col=1).drop('ID', axis=1)
    df = utils.index_from_inchicode(df, smiles=True)

    if raw:
        return df

    df = utils.drop_rows(df)
    df = utils.handle_duplicates(df, type='str')

    return df




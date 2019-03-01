import os.path
import glob
import pandas as pd
import numpy as np
from ... import utils


__data_src__ = list(sorted(glob.glob(os.path.join(__path__[0], "compounds/*[0-9].txt"))))
__data_src__ += list(sorted(glob.glob(os.path.join(__path__[0], "properties/[CO]*.txt"))))


def read_osf(raw=False):

    smiles = [np.loadtxt(f, dtype='str').item() for f in __data_src__[:-2]]
    df = pd.DataFrame({'OSF_Kar': np.loadtxt(__data_src__[-1], usecols=1, skiprows=1, delimiter=',')})
    df = df.set_index(pd.Index(smiles))
    inchi_index = utils.convert_index(df.index)
    df.index = inchi_index
    if raw:
        return df

    df = utils.drop_rows(df)
    df = utils.handle_duplicates(df, type='cont')

    return df


def read_carc(raw=False):

    smiles = [np.loadtxt(f, dtype='str').item() for f in __data_src__[:-2]]
    df = pd.DataFrame({'Carc_Kar': np.loadtxt(__data_src__[-2], usecols=1, skiprows=1, delimiter=',', dtype='str')})
    df = df.set_index(pd.Index(smiles))
    inchi_index = utils.convert_index(df.index)
    df.index = inchi_index
    if raw:
        return df

    df = utils.drop_rows(df)
    df = utils.convert_to_classes(df,'P','N')
    df = utils.handle_duplicates(df, type='bin')


    return df

def read_data(raw=False):
    carc = read_carc(raw)
    osf = read_osf()

    return pd.concat([carc,osf],axis=1)




def read_structures(raw=False):
    smiles = [np.loadtxt(f, dtype='str').item() for f in __data_src__[:-2]]
    df = pd.DataFrame({'Smiles': smiles}, index=pd.Index(smiles))

    if raw:
        return df

    inchi_index = utils.convert_index(df.index)
    df.index = inchi_index
    df = utils.drop_rows(df)
    df = utils.handle_duplicates(df, type='str')

    return df

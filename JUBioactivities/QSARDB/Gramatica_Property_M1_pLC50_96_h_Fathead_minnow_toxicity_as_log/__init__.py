import os.path
import glob
import pandas as pd
import numpy as np
from ... import utils


__data_src__ = list(sorted(glob.glob(os.path.join(__path__[0], "compounds/*[0-9].txt"))))
__data_src__ += list(sorted(glob.glob(os.path.join(__path__[0], "properties/*.txt"))))


def read_data(raw=False):

    smiles = [np.loadtxt(f, dtype='str').item() for f in __data_src__[:-23]]
    props = __data_src__[-23:]

    df = pd.concat([pd.read_csv(f, index_col=0) for f in props], axis=1)
    df.columns = ['_'.join([x,str(i),'M1_Gramatica']) for i,x in enumerate(df.columns)]
    df = pd.concat([pd.DataFrame({'Smiles': smiles}), df], axis=1)
    df = df.set_index(['Smiles'])
    df = df[df.index.notnull()]
    inchi_index = utils.convert_index(df.index)
    df.index = inchi_index
    if raw:
        return df
    df = utils.drop_rows(df)
    df = utils.handle_duplicates(df, type='cont')

    return df


def read_structures(raw=False):
    smiles = [np.loadtxt(f, dtype='str').item() for f in __data_src__[:-23]]
    df = pd.DataFrame({'Smiles': smiles}, index=pd.Index(smiles))
    inchi_index = utils.convert_index(df.index)
    df.index = inchi_index

    if raw:
        return df

    df = utils.drop_rows(df)
    df = utils.handle_duplicates(df, type='str')

    return df

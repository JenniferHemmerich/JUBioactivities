import os.path
import glob
import pandas as pd
import numpy as np
from ... import utils


__data_src__ = list(sorted(glob.glob(os.path.join(__path__[0], "compounds/*[0-9].txt"))))
__data_src__ += list(sorted(glob.glob(os.path.join(__path__[0], "properties/*.txt"))))


def read_data(raw=False):

    smiles = [np.loadtxt(f, dtype='str').item() for f in __data_src__[:-6]]
    props = __data_src__[-6:]

    df = pd.concat([pd.read_csv(f, index_col=0, sep='\t') for f in props], axis=1)
    df = pd.concat([pd.DataFrame({'Smiles': smiles}), df], axis=1)
    df = df.set_index(['Smiles'])
    df = df.rename(columns=lambda x: '_'.join([x, "MlogP_Ran"]))
    df = df[df.index.notnull()]
    df.index = utils.convert_index(df.index)
    if raw:
        return df
    df = utils.drop_rows(df)
    df = utils.handle_duplicates(df, type='cont')

    return df


def read_structures(raw=False):
    smiles = [np.loadtxt(f, dtype='str').item() for f in __data_src__[:-6]]
    df = pd.DataFrame({'Smiles': smiles}, index=pd.Index(smiles))
    df.index = utils.convert_index(df.index)

    if raw:
        return df

    df = utils.drop_rows(df)
    df = utils.handle_duplicates(df, type='str')

    return df

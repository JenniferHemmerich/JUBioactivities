import os.path
import glob
import pandas as pd
import numpy as np
from ... import utils


__data_src__ = list(sorted(glob.glob(os.path.join(__path__[0], "compounds/0*.txt"))))
__data_src__ += [os.path.join(__path__[0], "properties/logBB.txt")]


def read_data(raw=False):
    smiles = [np.loadtxt(f, dtype='str').item() for f in __data_src__[:-1]]
    df = pd.DataFrame({'LogBB_Abraham': np.loadtxt(__data_src__[-1], usecols=1, delimiter=',')})
    df = df.set_index(pd.Index(smiles))
    inchi_index = utils.convert_index(df.index)
    df.index = inchi_index

    if raw:
        return df

    df = utils.drop_rows(df)
    df = utils.handle_duplicates(df, type='cont')

    return df


def read_structures(raw=False):
    smiles = [np.loadtxt(f, dtype='str').item() for f in __data_src__[:-1]]
    df = pd.DataFrame({'Smiles': smiles}, index=pd.Index(smiles))
    inchi_index = utils.convert_index(df.index)
    df.index = inchi_index

    if raw:
        return df

    df = utils.drop_rows(df)
    df = utils.handle_duplicates(df, type='str')

    return df

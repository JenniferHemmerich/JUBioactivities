import os.path
import glob
import pandas as pd
import numpy as np
from ... import utils


__data_src__ = list(sorted(glob.glob(os.path.join(__path__[0], "compounds/*[0-9].txt"))))
__data_src__ += list(sorted(glob.glob(os.path.join(__path__[0], "properties/*.txt"))))


def read_data(raw=False):
    smiles = [np.loadtxt(f, dtype='str').item() for f in __data_src__[:-2]]
    df = pd.DataFrame({'BP_Tb_Tetteh': np.loadtxt(__data_src__[-2], usecols=1, skiprows=1, delimiter='\t'),
                       'FP_Tb_Tetteh': np.loadtxt(__data_src__[-1], usecols=1, skiprows=1, delimiter='\t')})
    df = df.set_index(pd.Index(smiles))
    df = utils.index_from_inchicode(df)
    if raw:
        return df

    df = utils.drop_rows(df)
    df = utils.handle_duplicates(df, type='cont')

    return df


def read_structures(raw=False):
    smiles = [np.loadtxt(f, dtype='str').item() for f in __data_src__[:-2]]
    df = pd.DataFrame({'Smiles': smiles}, index=pd.Index(smiles))
    df = utils.index_from_inchicode(df, smiles=True)

    if raw:
        return df

    df = utils.drop_rows(df)
    df = utils.handle_duplicates(df, type='str')

    return df

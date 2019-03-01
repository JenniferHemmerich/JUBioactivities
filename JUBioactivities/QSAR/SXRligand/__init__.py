import os.path, glob
import pandas as pd
import numpy as np
from ... import utils


__data_src__ = [os.path.join(__path__[0], f)
                for f in ("SXR.ismsmi", "SXR.target")]


def read_data(raw=False):
    df = pd.read_csv(__data_src__[1], index_col=False, names=['sxr_ligand'])
    smiles = np.loadtxt(__data_src__[0], dtype='str')
    df.index = utils.convert_index(smiles)

    if raw:
        return df

    df = utils.drop_rows(df)
    df = utils.handle_duplicates(df, type='cont')
    return df


def read_structures(raw=False):
    df = pd.read_csv(__data_src__[0])
    df.columns = ['Smiles']
    df = df.set_index('Smiles', drop=False)
    df.index = utils.convert_index(df.index)

    if raw:
        return df

    df = utils.drop_rows(df)
    df = utils.handle_duplicates(df, type='str')
    return df


import os.path
import glob
import pandas as pd
import numpy as np
from ... import utils


__data_src__ = list(sorted(glob.glob(os.path.join(__path__[0], "compounds/*[0-9].mol"))))
__data_src__ += list(sorted(glob.glob(os.path.join(__path__[0], "properties/*.txt"))))

def read_logBCF(raw=False):
    df = pd.DataFrame(
        {'logBCF_bioacc_Piir': np.loadtxt(__data_src__[-1], usecols=1, skiprows=1, delimiter='\t')})
    df = df.set_index(pd.Index(__data_src__[:-2]))
    inchi_index = utils.convert_index(df.index, filenames=True)
    df.index = inchi_index
    if raw:
        return df

    df = utils.drop_rows(df)
    df = utils.handle_duplicates(df,type='cont')
    return df


def read_BCF(raw=False):
    df = pd.DataFrame(
        {'BCF_class_bioacc_Piir': np.loadtxt(__data_src__[-2], usecols=1, skiprows=1, delimiter='\t', dtype='str')})
    df = df.set_index(pd.Index(__data_src__[:-2]))
    inchi_index = utils.convert_index(df.index, filenames=True)
    df.index = inchi_index
    if raw:
        return df

    df = utils.drop_rows(df)
    df = utils.convert_to_classes(df, 'B', 'nB')
    df = utils.handle_duplicates(df, type='bin')

    return df

def read_data(raw=False):

    df = pd.concat([read_BCF(raw),read_logBCF(raw)],axis=1)
    return df


def read_structures(raw=False):
    df = pd.DataFrame(index=pd.Index(__data_src__[:-2]))
    df = utils.get_smiles_from_index(df)
    df.index = utils.convert_index(df.index, filenames=True)

    if raw:
        return df

    df = utils.drop_rows(df)
    df = utils.handle_duplicates(df, type='str')

    return df

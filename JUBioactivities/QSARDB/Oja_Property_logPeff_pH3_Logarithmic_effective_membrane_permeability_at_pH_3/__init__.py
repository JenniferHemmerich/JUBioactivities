import os.path
import glob
import pandas as pd
import numpy as np
from ... import utils


__data_src__ = list(sorted(glob.glob(os.path.join(__path__[0], "compounds/*[0-9].mol"))))
__data_src__ += list(sorted(glob.glob(os.path.join(__path__[0], "properties/*.txt"))))


def read_data(raw=False):

    smiles = sorted(__data_src__[:-4])
    props = __data_src__[-4:]

    df = pd.concat([pd.read_csv(f, index_col=0, sep="\t") for f in props], axis=1).sort_index()
    df = df.set_index(pd.Index(smiles))
    df = df.rename(columns=lambda x: '_'.join([x, "pH_Oja"]))
    df = df[df.index.notnull()]
    inchi_index = utils.convert_index(df.index, filenames=True)
    df.index = inchi_index
    if raw:
        return df
    df = utils.drop_rows(df)
    df = utils.handle_duplicates(df, type='cont')

    return df


def read_structures(raw=False):
    smiles = sorted(__data_src__[:-4])
    df = pd.DataFrame({'Smiles': smiles}, index=pd.Index(smiles))
    inchi_index = utils.convert_index(df.index, filenames=True)
    df = utils.get_smiles_from_index(df)
    df.index = inchi_index

    if raw:
        return df

    df = utils.drop_rows(df)
    df = utils.handle_duplicates(df, type='str')

    return df
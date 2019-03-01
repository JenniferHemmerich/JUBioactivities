import os.path
import glob
import pandas as pd
import numpy as np
from ... import utils


__data_src__ = list(sorted(glob.glob(os.path.join(__path__[0], "compounds/*.mol"))))
__data_src__ += list(sorted(glob.glob(os.path.join(__path__[0], "properties/*.txt"))))


def read_data(raw=False):

    props = __data_src__[-2:]

    df = pd.concat([pd.read_csv(f, index_col=0, sep="\t") for f in props], axis=1)
    df = df.reset_index()
    df = pd.concat([pd.DataFrame({'Mols': __data_src__[:-2]}), df], axis=1).drop('index',axis=1)
    df = df.set_index('Mols')

    df = df.rename(columns=lambda x: '_'.join([x,"Martin"]))
    df = df[df.index.notnull()]
    inchi_index = utils.convert_index(df.index, filenames=True)
    df.index = inchi_index
    if raw:
        return df
    df = utils.drop_rows(df)
    df = utils.handle_duplicates(df, type='cont')

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

import os.path
import glob
import pandas as pd
import numpy as np
from ... import utils


__data_src__ = list(sorted(glob.glob(os.path.join(__path__[0], "compounds/*[0-9].mol"))))
__data_src__ += list(sorted(glob.glob(os.path.join(__path__[0], "properties/*.txt"))))


def read_data(raw=False):

    mols =  __data_src__[:-6]
    props = __data_src__[-6:]

    df = pd.concat([pd.read_csv(f, index_col=0, sep='\t') for f in props], axis=1)
    df = pd.concat([pd.DataFrame({'mols': mols}), df], axis=1)
    df = df.set_index(['mols'])
    df = df.rename(columns=lambda x: '_'.join([x, "logH_Papa"]))
    df = df[df.index.notnull()]
    inchi_index = utils.convert_index(df.index, filenames=True)
    df.index = inchi_index
    if raw:
        return df
    df = utils.drop_rows(df)
    df = utils.handle_duplicates(df, type='cont')

    return df


def read_structures(raw=False):
    mols =  __data_src__[:-6]
    df = pd.DataFrame(index=pd.Index(mols))
    df = utils.get_smiles_from_index(df)
    inchi_index = utils.convert_index(df.index, filenames=True)
    df.index = inchi_index

    if raw:
        return df
    df = utils.drop_rows(df)
    df = utils.handle_duplicates(df, type='str')

    return df

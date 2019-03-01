import os.path, glob
import pandas as pd
import numpy as np
from ... import utils


__data_src__ = list(sorted(glob.glob(os.path.join(__path__[0], "dan*.mol"))))
__data_src__ += [os.path.join(__path__[0], "depv.txt")]


def read_data(raw=False):
    df = pd.DataFrame({'logRA_artemisin': np.loadtxt(__data_src__[-1])},
                      index=__data_src__[:-1])
    df.index = utils.convert_index(df.index, filenames=True)

    if raw:
        return df

    df = utils.drop_rows(df)
    df = utils.handle_duplicates(df,type='cont')

    return df


def read_structures(raw=False):
    df = pd.DataFrame(index=__data_src__[:-1])
    df = utils.get_smiles_from_index(df)
    df.index = utils.convert_index(df.index, filenames=True)

    if raw:
        return df

    df = utils.drop_rows(df)
    df = utils.handle_duplicates(df, type='str')

    return df
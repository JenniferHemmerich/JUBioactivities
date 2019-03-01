import os.path, glob
import pandas as pd
import numpy as np
from ... import utils


__data_src__ = list(sorted(glob.glob(os.path.join(__path__[0], "compounds/0*.mol"))))
__data_src__ += [os.path.join(__path__[0], "properties/pEC50.txt")]


def read_data(raw=False):

    df = pd.DataFrame({'pEC50_Aruoja': np.loadtxt(__data_src__[-1],usecols=1, skiprows =1, delimiter=',')}, index=__data_src__[:-1])
    inchi_index = utils.convert_index(df.index, filenames=True)
    df.index = inchi_index

    if raw:
        return df

    df = utils.drop_rows(df)
    df = utils.handle_duplicates(df,type='cont')

    return df

def read_structures(raw=False):
    df = pd.DataFrame(index=__data_src__[:-1])
    df = utils.get_smiles_from_index(df, filenames=True)
    inchi_index = utils.convert_index(df.index, filenames=True)
    df.index = inchi_index

    if raw:
        return df

    df = utils.drop_rows(df)
    df = utils.handle_duplicates(df,type='str')

    return df
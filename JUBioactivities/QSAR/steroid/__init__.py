import os.path
import pandas as pd
from ... import utils


__data_src__ = [os.path.join(__path__[0], f)
                for f in ("steroids.sdf", "activity.txt")]


def read_data(raw=False):
    df = pd.read_csv(__data_src__[1], delimiter='  ', index_col=False,
                     names=['pK_steroid'], skiprows=14, engine='python')
    df.index = utils.convert_index([__data_src__[0]] * len(df), filenames=True)

    if raw:
        return df

    df = utils.drop_rows(df)
    df = utils.handle_duplicates(df,type='cont')
    return df


def read_structures(raw=False):

    df = pd.DataFrame(index=[__data_src__[0]] * 31)
    df = utils.get_smiles_from_index(df)
    df.index = utils.convert_index(df.index, filenames=True)

    if raw:
        return df

    df = utils.drop_rows(df)
    df = utils.handle_duplicates(df, type='str')
    return df
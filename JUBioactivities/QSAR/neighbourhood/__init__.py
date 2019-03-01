import os.path, glob
import pandas as pd
from ... import utils


__data_src__ = glob.glob(os.path.join(__path__[0], "*.sdf"))

#TODO use raw? datasets are different

def _read(name, raw=False):
    fname = os.path.join(__path__[0], "{}.sdf".format(name))
    df = utils.read_labelled_molecules(fname, key='BIO')
    df = utils.drop_rows(df)
    df = df.apply(pd.to_numeric,errors='coerce')
    df = utils.handle_duplicates(df, type='cont')
    return df

def read_data(raw=False):
    return pd.concat([_read(n) for n in (
        'chang', 'cristalli', 'depreux', 'doherty', 'garratt', 'garratt2',
        'heyl', 'krystek', 'lewis', 'penning', 'rosowsky', 'siddiqi',
        'stevenson', 'strupcz', 'svensson', 'thompson', 'tsutumi',
        'uehling', 'yokoyama1', 'yokoyama2')], axis=1)

def _read_structure(name, raw=False):
    fname = os.path.join(__path__[0], "{}.sdf".format(name))
    df = utils.read_labelled_molecules(fname, key='BIO', structures=True)
    df = utils.drop_rows(df)
    df = utils.handle_duplicates(df, type='str')
    return df

def read_structures(raw=False):
    df = pd.concat([_read_structure(n) for n in (
        'chang', 'cristalli', 'depreux', 'doherty', 'garratt', 'garratt2',
        'heyl', 'krystek', 'lewis', 'penning', 'rosowsky', 'siddiqi',
        'stevenson', 'strupcz', 'svensson', 'thompson', 'tsutumi',
        'uehling', 'yokoyama1', 'yokoyama2')])
    if raw:
        return df

    return utils.handle_duplicates(df,type='str')
import os.path
import pandas as pd
#from ... import utils
from ... import utils


__data_src__ = [os.path.join(__path__[0], "{}_3d.sdf".format(f))
                for f in ("bzr", "cox2", "dhfr", "er_lit", "er_tox")]


def read_bzr(raw=False):
    df = utils.read_labelled_molecules(__data_src__[0], key='IC50_uM', name='BZR_sutherland')
    if raw:
        return df
    df = utils.drop_rows(df)
    df = df.apply(pd.to_numeric, errors='coerce')
    df = utils.handle_duplicates(df, type='cont')
    return df


def read_cox2(raw=False):
    df = utils.read_labelled_molecules(__data_src__[1], key='IC50_uM', name='COX2_sutherland')
    if raw:
        return df
    df = utils.drop_rows(df)
    df = df.apply(pd.to_numeric, errors='coerce')
    df = utils.handle_duplicates(df, type='cont')

    return df


def read_dhfr(raw=False):
    df = utils.read_labelled_molecules(__data_src__[2], key=['PC_uM', 'TG_uM', 'RL_uM'],
                                       name=['PC_uM_DHFR_sutherland', 'TG_uM_DHFR_sutherland', 'RL_uM_DHFR_sutherland'])
    if raw:
        return df
    df = utils.drop_rows(df)
    df = df.apply(pd.to_numeric, errors='coerce')
    df = utils.handle_duplicates(df, type='cont')

    return df


def read_er_lit(raw=False):
    df = utils.read_labelled_molecules(__data_src__[3], key='RBA_avg', name='ER_LIT_sutherland')
    if raw:
        return df
    df = utils.drop_rows(df)
    df = df.apply(pd.to_numeric, errors='coerce')
    df = utils.handle_duplicates(df, type='cont')

    return df


def read_er_tox(raw=False):
    df = utils.read_labelled_molecules(__data_src__[4], key='RBA', name='ER_TOX_sutherland')
    if raw:
        return df
    df = utils.drop_rows(df)
    df = df.apply(pd.to_numeric, errors='coerce')
    df = utils.handle_duplicates(df, type='cont')

    return df


def read_data(raw=False):
    dfs = [read_bzr(raw), read_cox2(raw), read_dhfr(raw), read_er_lit(raw), read_er_tox(raw)]
    return pd.concat(dfs, axis=1)


def read_bzr_structures(raw=False):
    df = utils.read_labelled_molecules(__data_src__[0], key='IC50_uM', name='BZR_sutherland', structures=True)
    if raw:
        return df
    df = utils.drop_rows(df)
    df = utils.handle_duplicates(df, type='str')
    return df


def read_cox2_structures(raw=False):
    df = utils.read_labelled_molecules(__data_src__[1], key='IC50_uM', name='COX2_sutherland', structures=True)
    if raw:
        return df
    df = utils.drop_rows(df)
    df = utils.handle_duplicates(df, type='str')
    return df


def read_dhfr_structures(raw=False):
    df = utils.read_labelled_molecules(__data_src__[2], key='IC50_uM', name='DHFR_sutherland', structures=True)
    if raw:
        return df
    df = utils.drop_rows(df)
    df = utils.handle_duplicates(df, type='str')
    return df


def read_er_lit_structures(raw=False):
    df = utils.read_labelled_molecules(__data_src__[3], key='IC50_uM', name='ER_LIT_sutherland', structures=True)
    if raw:
        return df
    df = utils.drop_rows(df)
    df = utils.handle_duplicates(df, type='str')
    return df


def read_er_tox_structures(raw=False):
    df = utils.read_labelled_molecules(__data_src__[4], key='IC50_uM', name='ER_TOX_sutherland', structures=True)
    if raw:
        return df
    df = utils.drop_rows(df)
    df = utils.handle_duplicates(df, type='str')
    return df


def read_structures(raw=False):
    dfs = [read_bzr_structures(raw), read_cox2_structures(raw), read_dhfr_structures(raw), read_er_lit_structures(raw),
           read_er_tox_structures(raw)]
    df = pd.concat(dfs)
    if raw:
        return df
    df = utils.handle_duplicates(df, type='str')
    return df


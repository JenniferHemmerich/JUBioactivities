import os.path
import pandas as pd
from ... import utils


__data_src__ = [os.path.join(__path__[0], "{}_3dqsar.sdf".format(f))
                for f in ("ace", "ache", "bzr", "cox2", "dhfr", "gpb", "therm", "thr")]


def read_ace(raw=False):
    df = utils.read_labelled_molecules(__data_src__[0], key='ACTIVITY', name='ACE_sutherland4')

    if raw:
        return df

    df = utils.drop_rows(df)
    df = df.apply(pd.to_numeric, errors='coerce')
    df = utils.handle_duplicates(df, type='cont')

    return df


def read_ache(raw=False):
    df = utils.read_labelled_molecules(__data_src__[1], key='ACTIVITY', name='ACHE_sutherland4')

    if raw:
        return df

    df = utils.drop_rows(df)
    df = df.apply(pd.to_numeric, errors='coerce')
    df = utils.handle_duplicates(df, type='cont')

    return df


def read_bzr(raw=False):
    df = utils.read_labelled_molecules(__data_src__[2], key='ACTIVITY', name='BZR_4_sutherland4')

    if raw:
        return df

    df = utils.drop_rows(df)
    df = df.apply(pd.to_numeric, errors='coerce')
    df = utils.handle_duplicates(df, type='cont')

    return df


def read_cox2(raw=False):
    df = utils.read_labelled_molecules(__data_src__[3], key='ACTIVITY', name='COX2_4_sutherland4')

    if raw:
        return df

    df = utils.drop_rows(df)
    df = df.apply(pd.to_numeric, errors='coerce')
    df = utils.handle_duplicates(df, type='cont')

    return df


def read_dhfr(raw=False):
    df= utils.read_labelled_molecules(__data_src__[4], key='ACTIVITY', name='DHFR_4_sutherland4')

    if raw:
        return df

    df = utils.drop_rows(df)
    df = df.apply(pd.to_numeric, errors='coerce')
    df = utils.handle_duplicates(df, type='cont')

    return df


def read_gpb(raw=False):
    df = utils.read_labelled_molecules(__data_src__[5], key='ACTIVITY', name='GPB_sutherland4')

    if raw:
        return df

    df = utils.drop_rows(df)
    df = df.apply(pd.to_numeric, errors='coerce')
    df = utils.handle_duplicates(df, type='cont')

    return df


def read_therm(raw=False):
    df = utils.read_labelled_molecules(__data_src__[6], key='ACTIVITY', name='THERM_sutherland4')

    if raw:
        return df

    df = utils.drop_rows(df)
    df = df.apply(pd.to_numeric, errors='coerce')
    df = utils.handle_duplicates(df, type='cont')

    return df


def read_thr(raw=False):
    df = utils.read_labelled_molecules(__data_src__[7], key='ACTIVITY', name='THR_sutherland4')

    if raw:
        return df

    df = utils.drop_rows(df)
    df = df.apply(pd.to_numeric, errors='coerce')
    df = utils.handle_duplicates(df, type='cont')

    return df


def read_data(raw=False):
    return pd.concat([read_ace(raw), read_ache(raw), read_bzr(raw), read_cox2(raw),
                      read_dhfr(raw), read_gpb(raw), read_therm(raw), read_thr(raw)],
                     axis=1)


def read_ace_structures(raw=False):
    df = utils.read_labelled_molecules(__data_src__[0], key='ACTIVITY', name='ACE_sutherland4', structures=True)

    if raw:
        return df

    df = utils.drop_rows(df)
    df = utils.handle_duplicates(df, type='str')

    return df


def read_ache_structures(raw=False):
    df = utils.read_labelled_molecules(__data_src__[1], key='ACTIVITY', name='ACHE_sutherland4', structures=True)

    if raw:
        return df

    df = utils.drop_rows(df)
    df = utils.handle_duplicates(df, type='str')

    return df


def read_bzr_structures(raw=False):
    df = utils.read_labelled_molecules(__data_src__[2], key='ACTIVITY', name='BZR_4_sutherland4', structures=True)

    if raw:
        return df

    df = utils.drop_rows(df)
    df = utils.handle_duplicates(df, type='str')

    return df


def read_cox2_structures(raw=False):
    df = utils.read_labelled_molecules(__data_src__[3], key='ACTIVITY', name='COX2_4_sutherland4', structures=True)

    if raw:
        return df

    df = utils.drop_rows(df)
    df = utils.handle_duplicates(df, type='str')

    return df


def read_dhfr_structures(raw=False):
    df= utils.read_labelled_molecules(__data_src__[4], key='ACTIVITY', name='DHFR_4_sutherland4', structures=True)

    if raw:
        return df

    df = utils.drop_rows(df)
    df = utils.handle_duplicates(df, type='str')

    return df


def read_gpb_structures(raw=False):
    df = utils.read_labelled_molecules(__data_src__[5], key='ACTIVITY', name='GPB_sutherland4', structures=True)

    if raw:
        return df

    df = utils.drop_rows(df)
    df = utils.handle_duplicates(df, type='str')

    return df


def read_therm_structures(raw=False):
    df = utils.read_labelled_molecules(__data_src__[6], key='ACTIVITY', name='THERM_sutherland4', structures=True)

    if raw:
        return df

    df = utils.drop_rows(df)
    df = utils.handle_duplicates(df, type='str')

    return df


def read_thr_structures(raw=False):
    df = utils.read_labelled_molecules(__data_src__[7], key='ACTIVITY', name='THR_sutherland4', structures=True)

    if raw:
        return df

    df = utils.drop_rows(df)
    df = utils.handle_duplicates(df, type='str')

    return df


def read_structures(raw=False):
    df = pd.concat([read_ace_structures(raw), read_ache_structures(raw), read_bzr_structures(raw),
                      read_cox2_structures(raw), read_dhfr_structures(raw), read_gpb_structures(raw),
                      read_therm_structures(raw), read_thr_structures(raw)])
    if raw:
        return df
    return utils.handle_duplicates(df, type='str')

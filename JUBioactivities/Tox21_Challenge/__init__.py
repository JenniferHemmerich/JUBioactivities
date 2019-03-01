import os.path, glob
import pandas as pd
import importlib
from .. import utils



__all__ = ["JUBioactivities.Tox21_Challenge.AHR",
 "JUBioactivities.Tox21_Challenge.AR",
 "JUBioactivities.Tox21_Challenge.AR_LBD",
"JUBioactivities.Tox21_Challenge.ARE",
"JUBioactivities.Tox21_Challenge.aromatase",
"JUBioactivities.Tox21_Challenge.atad5",
"JUBioactivities.Tox21_Challenge.ER",
"JUBioactivities.Tox21_Challenge.ER_LBD",
"JUBioactivities.Tox21_Challenge.HSE",
"JUBioactivities.Tox21_Challenge.MMP",
"JUBioactivities.Tox21_Challenge.p53",
"JUBioactivities.Tox21_Challenge.PPAR"
]


def read_data(raw=False):
    mods = [importlib.import_module(m) for m in __all__]
    df = pd.concat([f.read_data(raw) for f in mods], axis=1)
    return df


def read_structures(raw=False):
    mods = [importlib.import_module(m) for m in __all__]
    df = pd.concat([f.read_structures(raw) for f in mods])
    df = utils.handle_duplicates(df,type='str')
    return df



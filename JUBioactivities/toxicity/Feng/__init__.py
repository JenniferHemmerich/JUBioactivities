
from . import Mut
from . import NCI
from . import Tox
from . import Yeast
from ... import utils

import pandas


def read_data(raw=False):
    df = pandas.concat([Mut.read_data(raw),
                        NCI.read_data(raw),
                        Tox.read_data(raw),
                        Yeast.read_data(raw)
                        ], axis=1)
    return df

def read_structures(raw=False):
    df = pandas.concat([Mut.read_structures(raw),
                        NCI.read_structures(raw),
                        Tox.read_structures(raw),
                        Yeast.read_structures(raw)
                        ])
    df = utils.handle_duplicates(df, type='str')
    return df





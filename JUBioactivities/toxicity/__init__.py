from . import _herg
from .import amicbase
from .import bursi
from .import fda
from .Feng import Mut
from .Feng import NCI
from .Feng import Tox
from .Feng import Yeast
from .import Hansen_Ames
from .import helma
from .import ISSCAN
from .import mutagenDebnath
from .import ntp

# import importlib
# import pkgutil
import pandas

#
# __path__ = pkgutil.extend_path(__path__, __name__)
# for importer, modname, ispkg in pkgutil.walk_packages(path=__path__, prefix=__name__+'.'):
#     importlib.import_module(modname)

def read_data(raw = False):
    df = pandas.concat([_herg.read_data(raw),
                        amicbase.read_data(raw),
                        bursi.read_data(raw),
                        fda.read_data(raw),
                        Mut.read_data(raw),
                        NCI.read_data(raw),
                        Tox.read_data(raw),
                        Yeast.read_data(raw),
                        Hansen_Ames.read_data(raw),
                        helma.read_data(raw),
                        ISSCAN.read_data(raw),
                        mutagenDebnath.read_data(raw),
                        ntp.read_data(raw)
                        ], axis=1)
    return df

def read_structures(raw = False):
    df = pandas.concat([_herg.read_structures(raw),
                        amicbase.read_structures(raw),
                        bursi.read_structures(raw),
                        fda.read_structures(raw),
                        Mut.read_structures(raw),
                        NCI.read_structures(raw),
                        Tox.read_structures(raw),
                        Yeast.read_structures(raw),
                        Hansen_Ames.read_structures(raw),
                        helma.read_structures(raw),
                        ISSCAN.read_structures(raw),
                        mutagenDebnath.read_structures(raw),
                        ntp.read_structures(raw)
                        ], axis=1)
    return df







## JUNet
===================

This library helps in easily loading datasets into python for further use in machine learning.

### A) Install in a conda environment

The library can be installed by downloading the latest release and installing it in a conda environment (note: rdkit has to be installed manually)

For this: 
1. navigate into the unzipped folder and activate the environment

2. Installation then can be done via 

```
pip install .
```

The library will be installed in the site-packages.

### B) Without installation: 

Just add the libraries directory to the PYTHONPATH and use it without installation
Dependencies are pandas, standardiser, scikit-learn and rdkit

 
## Use of the library

Each datasource contains an init file which (in most cases) provides two functions:

read_data() function:
imports the results with the InchiKey as Index and the activity/assay result as a column with the according name

read_structure() function:
imports the structures (as rdkit molecules) in a table with the InchiKey as Index
(Note although for the InChI Key generation structures are standardised, the read_structure() call returns non standardised structures so the user is able to apply their custom procedures)

To use a dataset import the read_structures() or the read_data() function from the respective folder and use the dataset. An example notebook can be found undes docs/examples

An overview of the available datasets or endpoints can be found in Helpers/Datasets_Endpoints.csv
In there all available datasets with the respective endpoint are stored. Additional information is given about the number of compounds per endpoint and dataset (if a dataset contains more than one endpoint).

## Internal File processing

The processing of the original files is done as follows:

1.The Matrix of Assay results
For the assay results the assay data is read in and converted to a standard format:
Continuous values are kept as given, binary values are converted to 1 if the assay outcome
is positive, 0 if negative and NA if not available. Multiclass assays are encoded as one
hot labels. Standardised InChI Keys are used as index to be able to match the structures
from the structure matrix with the respective labels.

2. The chemical structures
For the table the structures are read in and converted to an RDKit Molecule. This
molecule is standardised via the Aktinson standardiser(https://github.com/flatkinson/standardiser).
Afterwards a standardised inchi key is generated to serve as Index. The Smiles are either
used directly from the data source or are generated via RDKit from the available (non-
smiles) structure type (note: given smiles are not standardised).To keep the structure file
aligned with the Assay results file Molecules where the structure cannot be imported to
RDKit were kept (currently 1212 structures) these have to be filtered via preprocessing.


Future changes:
Instead of standardiser use RDKit standardisation
Use custom one hot encoder (remove scikit-learn dependency) 
Get stream redirection to work with Notebooks


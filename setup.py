import os
from setuptools import setup, find_packages

desc = ''' JUBioactivities is a library containing datasets for over 400 endpoints related to toxicity. 
This library facilitates the retrieval of data for specific endpoints, and makes it easy to merge the datasets.
'''

setup(
    name='JUBioactivities',
    version='0.0.1',
    author='Jennifer Hemmerich',
    author_email='jennifer.hemmerich@outlook.de',
    license='MIT',
    url='',
    description='Datasets for Toxicity Prediction',
    long_description=desc,
    zip_safe=False,
    install_requires=['standardiser','pandas', 'scikit-learn'],
    packages = find_packages(),
    include_package_data = True
)

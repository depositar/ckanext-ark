# -*- coding: utf-8 -*-
# Always prefer setuptools over distutils
from setuptools import setup, find_namespace_packages
from codecs import open  # To use a consistent encoding
from os import path

here = path.abspath(path.dirname(__file__))

# Get the long description from the relevant file
with open(path.join(here, 'README.md'), encoding='utf-8') as f:
    long_description = f.read()

setup(
    name='ckanext-ark',
    version='1.0.1',
    description='A CKAN extension for assigning Archival Resource Key '
                '(ARK) identifiers to datasets.',
    long_description=long_description,
    long_description_content_type='text/markdown',
    url='https://github.com/depositar/ckanext-ark',
    author='Cheng-Jen Lee',
    author_email='u103133.u103135@gmail.com',
    license='MIT',
    classifiers=[
        'License :: OSI Approved :: MIT License',
        'Programming Language :: Python :: 3.7',
        'Programming Language :: Python :: 3.8',
    ],
    keywords='CKAN ARK',
    packages=find_namespace_packages(exclude=['ckanext.ark.tests']),
    namespace_packages=['ckanext'],
    install_requires=[
        'noid-mint'
    ],
    include_package_data=True,
    entry_points='''
        [ckan.plugins]
        ark=ckanext.ark.plugin:ArkPlugin

        [babel.extractors]
        ckan = ckan.lib.extract:extract_ckan
    ''',
    message_extractors={
        'ckanext': [
            ('**.py', 'python', None),
            ('**.js', 'javascript', None),
            ('**/templates/**.html', 'ckan', None),
        ],
    }
)

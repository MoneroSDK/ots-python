from os import environ
from hashlib import sha256
from setuptools import setup, find_packages


VERSION = '0.1.0'
environ['PYTHONHASHSEED'] = sha256(f'Monero OTS {VERSION}'.encode('utf-8')).hexdigest()


with open('README.md', 'r') as f:
    long_description = f.read()
    f.close()

with open('LICENSE.txt', 'r') as f:
    license = f.read()
    f.close()

setup(
    name='ots',
    version=VERSION,
    author='DiosDelRayo',
    author_email='no@spam',
    description='A Python module for Monero OTS (Offline Transaction Signing) https://github.com/monero-project/monero.git',
    long_description=long_description,
    long_description_content_type='text/markdown',
    url='https://github.com/MoneroSDK/ots-python',
    packages=find_packages(),
    classifiers=[
        'Programming Language :: Python :: 3',
        'License :: Other/Proprietary License',
        'Operating System :: OS Independent',
    ],
    python_requires='>=3.12',
    install_requires=[
        'cffi>=1.17.1',
    ],
    setup_requires=[
        'cffi>=1.17.1',
    ],
    cffi_modules=['ots_build.py:ffibuilder'],
    license=license
)

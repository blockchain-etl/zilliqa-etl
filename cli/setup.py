import os

from setuptools import setup, find_packages


def read(fname):
    return open(os.path.join(os.path.dirname(__file__), fname)).read()


long_description = read('README.md') if os.path.isfile("README.md") else ""

setup(
    name='zilliqa-etl',
    version='1.0.8',
    author='Evgeny Medvedev',
    author_email='evge.medvedev@gmail.com',
    description='Tools for exporting Zilliqa blockchain data to JSON',
    long_description=long_description,
    long_description_content_type='text/markdown',
    url='https://github.com/blockchain-etl/zilliqa-etl',
    packages=find_packages(exclude=['tests']),
    classifiers=[
        'Development Status :: 5 - Production/Stable',
        'Intended Audience :: Developers',
        'License :: OSI Approved :: MIT License',
        'Programming Language :: Python :: 3',
        'Programming Language :: Python :: 3.6',
        'Programming Language :: Python :: 3.7'
    ],
    keywords='Zilliqa',
    python_requires='>=3.6.0,<3.8.0',
    install_requires=[
        'blockchain-etl-common==1.3.0',
        'click==7.1.2',
        'python-dateutil==2.8.0',
        'pyzil==1.5.22',
        'jsonrpcclient==3.3.6'
    ],
    extras_require={
        'dev': [
            'pytest~=4.3.0',
            'pytest-timeout~=1.3.3'
        ],
    },
    entry_points={
        'console_scripts': [
            'zilliqaetl=zilliqaetl.cli:cli',
        ],
    },
    project_urls={
        'Bug Reports': 'https://github.com/blockchain-etl/zilliqa-etl/issues',
        'Source': 'https://github.com/blockchain-etl/zilliqa-etl',
    },
)

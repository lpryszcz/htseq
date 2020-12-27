import os
import pytest


@pytest.fixture(scope="module")
def data_folder():
    cwd = os.getcwd().rstrip('/')
    if cwd.endswith('example_data'):
        return cwd+'/'
    else:
        return cwd+'/example_data/'


@pytest.fixture(scope="module")
def docs_folder():
    cwd = os.getcwd().rstrip('/')
    if cwd.endswith('doc'):
        return cwd+'/'
    elif cwd.endswith('example_data'):
        return cwd[:-len('example_data')]+'doc/'
    else:
        return cwd+'/doc/'


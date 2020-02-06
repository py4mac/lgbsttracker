import os


def get_env(variable_name, default=None):
    return os.environ.get(variable_name, default)


def unset_variable(variable_name):
    if variable_name in os.environ:
        del os.environ[variable_name]

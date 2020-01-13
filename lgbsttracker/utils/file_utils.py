import posixpath
from six.moves.urllib.request import pathname2url


def path_to_local_file_uri(path):
    """
    Convert local filesystem path to local file uri.
    """
    path = pathname2url(path)
    if path == posixpath.abspath(path):
        return "file://{path}".format(path=path)
    else:
        return "file:{path}".format(path=path)

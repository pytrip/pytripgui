# find specification of the pytripgui module
from importlib import util
import os

# get location of __init__.py file (the one you see now) in the filesystem

spec = util.find_spec('pytripgui')
init_location = spec.origin

# VERSION should sit next to __init__.py in the directory structure
version_file = os.path.join(os.path.dirname(init_location), 'VERSION')

try:
    # read first line of the file (removing newline character)
    with open(version_file, 'r') as f:
        __version__ = f.readline().strip()
except FileNotFoundError:
    # backup solution - read the version from git
    from pytripgui.version import git_version
    __version__ = git_version()

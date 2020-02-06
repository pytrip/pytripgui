try:
    # find specification of the pytripgui module
    import importlib
    import os
    spec = importlib.util.find_spec('pytripgui')
    init_location = spec.origin  # location of __init__.py file (the one you see now) in the filesystem
    version_file = os.path.join(os.path.dirname(init_location), 'VERSION')  # VERSION should sit next to __init__.py in the directory structure
    with open(version_file, 'r') as f:
        __version__ = f.readline(1)
except FileNotFoundError:
    from pytripgui.version import git_version
    __version__ = git_version()

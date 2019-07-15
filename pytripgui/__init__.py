try:
    with open('VERSION', 'r') as f:
        __version__ = f.readline(1)
except FileNotFoundError:
    from version import git_version
    __version__ = git_version()

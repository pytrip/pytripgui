import setuptools
import subprocess


def git_version():
    """
    Inspired by https://github.com/numpy/numpy/blob/master/setup.py
    :return: the git revision as a string
    """
    def _minimal_ext_cmd(cmd):
        # construct minimal environment
        env = {}
        for k in ['SYSTEMROOT', 'PATH', 'HOME']:
            v = os.environ.get(k)
            if v is not None:
                env[k] = v
        # LANGUAGE is used on win32
        env['LANGUAGE'] = 'C'
        env['LANG'] = 'C'
        env['LC_ALL'] = 'C'
        out = subprocess.Popen(cmd, stdout=subprocess.PIPE, env=env).communicate()[0]
        return out

    try:
        out = _minimal_ext_cmd(['git', 'describe', '--tags', '--long'])
        GIT_REVISION = out.strip().decode('ascii')
        print('GIT_REVISION', GIT_REVISION)
        if GIT_REVISION:
            no_of_commits_since_last_tag = int(GIT_REVISION.split('-')[1])
            tag_name = GIT_REVISION.split('-')[0][1:]
            if no_of_commits_since_last_tag == 0:
                version = tag_name
            else:
                version = '{}+rev{}'.format(tag_name, no_of_commits_since_last_tag)
        else:
            version = "Unknown"
    except OSError:
        version = "Unknown"

    return version

def write_version_py(filename='pytripgui/__init__.py'):
    cnt = """
__version__ = '%(version)s'
"""

    GIT_REVISION = git_version()
    a = open(filename, 'a')
    try:
        a.write(cnt % {'version': GIT_REVISION})
    finally:
        a.close()


write_version_py()


with open('README.rst') as readme_file:
    readme = readme_file.read()

setuptools.setup(
    name='pytrip98gui',
    version=get_version(),
    packages=setuptools.find_packages(exclude="tests"),
    url='https://github.com/pytrip/pytripgui',
    license='GPL',
    author='Jakob Toftegaard, Niels Bassler, Leszek Grzanka',
    author_email='leszek.grzanka@gmail.com',
    description='PyTRiP GUI',
    long_description=readme + '\n',
    classifiers=[
        # How mature is this project? Common values are
        #   3 - Alpha
        #   4 - Beta
        #   5 - Production/Stable
        'Development Status :: 3 - Alpha',

        # Indicate who your project is intended for
        'Intended Audience :: Developers',
        'Intended Audience :: Science/Research',
        'Topic :: Software Development :: Libraries :: Python Modules',
        'Topic :: Scientific/Engineering :: Medical Science Apps.',
        'Topic :: Scientific/Engineering :: Physics',
        'Operating System :: POSIX :: Linux',

        'License :: OSI Approved :: GNU General Public License v3 (GPLv3)',

        # Specify the Python versions you support here. In particular, ensure
        # that you indicate whether you support Python 2, Python 3 or both.
        'Programming Language :: Python :: 2.7',
    ],
    package_data={'pytripgui': ['res/*']},
    install_requires=[
        'numpy', 'scipy', 'pytrip98'
    ],
    entry_points={
        'console_scripts': [
            'pytripgui=pytripgui.main:start',
        ],
    },
    cmdclass=get_cmdclass(),

)

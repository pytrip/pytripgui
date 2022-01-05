import os
import setuptools

from pytripgui.version import git_version


def write_version_py(filename=os.path.join('pytripgui', 'VERSION')):
    cnt = """%(version)s
"""

    GIT_REVISION = git_version()
    a = open(filename, 'w')
    try:
        a.write(cnt % {'version': GIT_REVISION})
    finally:
        a.close()


write_version_py()

with open('README.rst') as readme_file:
    readme = readme_file.read()

# install_requires is list of dependencies needed by pip when running `pip install`
install_requires = [
    "matplotlib==3.4.3 ; python_version>='3.7'",
    'pytrip98[remote]~=3.7',
    'anytree~=2.8',
    'Events~=0.4',
    "PyQt5<5.10 ; python_version<'3.8'",
    "PyQt5>=5.15 ; python_version>='3.8'",
    "PyQtChart<5.10 ; python_version<'3.8'",
    "PyQtChart>=5.15 ; python_version>='3.8'",
]

setuptools.setup(
    name='pytrip98gui',
    version=git_version(),
    packages=setuptools.find_packages(exclude=["tests", "tests.*"]),
    url='https://github.com/pytrip/pytripgui',
    license='GPL',
    author='Niels Bassler et al.',
    author_email='bassler@clin.au.dk',
    maintainer='Leszek Grzanka et al.',
    maintainer_email='grzanka@agh.edu.pl',
    description='PyTRiP GUI',
    long_description=readme + '\n',
    classifiers=[
        # How mature is this project? Common values are
        #   3 - Alpha
        #   4 - Beta
        #   5 - Production/Stable
        'Development Status :: 3 - Alpha',

        # Indicate who your project is intended for
        'Intended Audience :: End Users/Desktop',
        'Intended Audience :: Science/Research',
        'Topic :: Software Development :: Libraries :: Python Modules',
        'Topic :: Scientific/Engineering :: Medical Science Apps.',
        'Topic :: Scientific/Engineering :: Physics',
        'Operating System :: MacOS :: MacOS X',
        'Operating System :: POSIX :: Linux',
        'Operating System :: Microsoft :: Windows :: Windows 10',
        'License :: OSI Approved :: GNU General Public License v3 (GPLv3)',

        # Specify the Python versions you support here. In particular, ensure
        # that you indicate whether you support Python 2, Python 3 or both.
        'Programming Language :: Python :: 3.6',
        'Programming Language :: Python :: 3.7',
        'Programming Language :: Python :: 3.8',
        'Programming Language :: Python :: 3.9',
        'Programming Language :: Python :: 3.10'
    ],
    package_data={'pytripgui': ['res/*', 'view/*.ui', 'VERSION']},
    install_requires=install_requires,
    entry_points={
        'console_scripts': [
            'pytripgui=pytripgui.main:main',
        ],
    })

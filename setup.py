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
    'pytrip98~=3.4',
    'anytree~=2.8',
    'paramiko~=2.7',
    'Events~=0.4',
    "PyQt5<5.10 ; python_version<'3.8'",
    "PyQt5>=5.15 ; python_version>='3.8'",
    "PyQtChart<5.10 ; python_version<'3.8'",
    "PyQtChart>=5.15 ; python_version>='3.8'",
]

setuptools.setup(
    name='pytrip98gui',
    version=git_version(),
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
        'Programming Language :: Python :: 3.5',
        'Programming Language :: Python :: 3.6',
        'Programming Language :: Python :: 3.7',
        'Programming Language :: Python :: 3.8',
        'Programming Language :: Python :: 3.9'
    ],
    package_data={'pytripgui': ['res/*', 'view/*.ui', 'VERSION']},
    install_requires=install_requires,
    entry_points={
        'console_scripts': [
            'pytripgui=pytripgui.main:main',
        ],
    })

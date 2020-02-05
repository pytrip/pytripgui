import setuptools

from pytripgui.version import git_version


def write_version_py(filename='VERSION'):
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
        'Programming Language :: Python :: 3.7'
    ],
    package_data={'pytripgui': ['res/*', 'view/*.ui']},
    install_requires=[
        'pytrip98>=2.5.6', 'PyQt5<5.10'
    ],
    entry_points={
        'console_scripts': [
            'pytripgui=pytripgui.main:main',
        ],
    }
)

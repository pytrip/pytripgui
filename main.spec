# -*- mode: python -*-

# one directory installation:
# might be useful when combined with installer generator such as http://www.innosetup.com/isinfo.php

# following https://github.com/FCS-analysis/PyCorrFit/blob/master/freeze_pyinstaller/PyCorrFit_win7.spec
# patch matplotlib rc file to include only one backend which results in smaller size of generated files
import matplotlib
mplrc = matplotlib.matplotlib_fname()
print(mplrc)
with open(mplrc) as fd:
    data = fd.readlines()
for ii, l in enumerate(data):
    if l.strip().startswith("backend "):
        data[ii] = "backend : Qt5Agg\n"
with open(mplrc, "w") as fd:
    fd.writelines(data)


# following https://github.com/FCS-analysis/PyCorrFit/blob/master/freeze_pyinstaller/PyCorrFit_win7.spec
# add current dir to PYTHONPATH, to enable importing pytripgui package
import sys
DIR = os.path.realpath(".")
sys.path.append(DIR)
import pytripgui
# get version string
version = pytripgui.__version__

# following https://github.com/FCS-analysis/PyCorrFit/blob/master/freeze_pyinstaller/PyCorrFit_win7.spec
# replace
## Create inno setup .iss file
import codecs
import platform
filename = "win_innosetup.iss"
issfile = codecs.open(filename, 'r', "utf-8")
iss = issfile.readlines()
issfile.close()
for i,item in enumerate(iss):
    if item.strip().startswith("#define MyAppVersion"):
        iss[i] = '#define MyAppVersion "{:s}"\n'.format(version)
    if item.strip().startswith("#define MyAppPlatform"):
        # sys.maxint returns the same for windows 64bit verions
        iss[i] = '#define MyAppPlatform "win_{}"\n'.format(platform.architecture()[0])
nissfile = codecs.open(filename, 'wb', "utf-8")
nissfile.writelines(iss)
nissfile.close()

exclude_modules = [
    "_asyncio",
    "_bz2",
    "_decimal",
    "_elementtree",
    "_hashlib",
    "_lzma",
    "_overlapped",
    "_queue",
    "_tkinter",

    'pywin.debugger',
    'IPython'
]
exclude = [
    "d3dcompiler_47.dll",
    "libcrypto-1_1-x64.dll",
    "libcrypto-1_1.dll",
    "libEGL.dll",
    "libGLESv2.dll",
    "libssl-1_1-x64.dll",
    "libssl-1_1.dll",
    "opengl32sw.dll",
    "Qt5DBus.dll",
    "Qt5Network.dll",
    "Qt5Qml.dll",
    "Qt5QmlModels.dll",
    "Qt5Quick.dll",
    "Qt5Svg.dll",
    "Qt5WebSockets.dll",
    "tcl86t.dll",
    "tk86t.dll",
    "ucrtbase.dll"
]
exclude_startswith = [
    "api-ms-win",
    "PyQt5\\Qt5\\plugins\\imageformats",
    "PyQt5\\Qt5\\plugins\\iconengines"
]

a = Analysis(['pytripgui\\main.py'],
             pathex=['.'],
             binaries=[],
             datas=[('pytripgui/res/*', 'pytripgui/res'),
                    ('pytripgui/view/*.ui', 'pytripgui/view'),
                    ('pytripgui/VERSION', '.')],
             hiddenimports=[],
             hookspath=[],
             runtime_hooks=[],
             excludes=exclude_modules,
             win_no_prefer_redirects=False,
             win_private_assemblies=False,
             cipher=None)


a.binaries = TOC([b for b in a.binaries if b[0] not in exclude])
for e in exclude_startswith:
    a.binaries = TOC([b for b in a.binaries if not b[0].startswith(e)])

print("=======================================================================")
print("Binaries:")
for bin in a.binaries:
    print(bin)
print("=======================================================================")

pyz = PYZ(a.pure, a.zipped_data, cipher=None)
exe = EXE(pyz,
          a.scripts,
          exclude_binaries=True,
          name='pytripgui',
          debug=False,
          strip=False,
          upx=False,
          console=False,
          icon='pytripgui/res/icon.ico')
coll = COLLECT(exe,
               a.binaries,
               a.zipfiles,
               a.datas,
               strip=False,
               upx=False,
               name='pytripgui')


# one file installation, nice but application has a slow start as each execution is related to unpacking of ~100MB archive
#a = Analysis(['pytripgui\\main.py'],
#             pathex=['.'],
#             binaries=[],
#             datas=[('pytripgui/res/*', 'res')],
#             hiddenimports=[],
#             hookspath=[],
#             runtime_hooks=[],
#             excludes=exclude_modules,
#             win_no_prefer_redirects=False,
#             win_private_assemblies=False,
#             cipher=None)
#
# a.binaries = TOC([b for b in a.binaries if b[0] not in exclude])
# for e in exclude_startswith:
#     a.binaries = TOC([b for b in a.binaries if not b[0].startswith(e)])
#
#pyz = PYZ(a.pure)
#exe = EXE(pyz,
#          a.scripts,
#          a.binaries,
#          a.zipfiles,
#          a.datas,
#          name='pytripgui',
#          debug=False,
#          strip=False,
#          upx=True,
#          console=False)

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
filename = "win10_innosetup.iss"
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

a = Analysis(['pytripgui\\main.py'],
             pathex=['.'],
             binaries=[],
             datas=[ ('pytripgui/res/*', 'res'), ('pytripgui/VERSION', '.' ), ('pytripgui/view/*.ui', 'view')],
             hiddenimports=['appdirs', 'packaging', 'packaging', 'packaging.version', 'packaging.specifiers', 'packaging.requirements'],
             hookspath=[],
             runtime_hooks=[],
             excludes=['pywin.debugger', 'tcl', 'IPython', 'tornado'],
             win_no_prefer_redirects=False,
             win_private_assemblies=False,
             cipher=None)

a.binaries = [x for x in a.binaries if not x[0].startswith("IPython")]
a.binaries = [x for x in a.binaries if not x[0].startswith("zmq")]

a.binaries = a.binaries - TOC([
 ('sqlite3.dll', None, None),
 ('_sqlite3', None, None),
 ('_ssl', None, None)])

pyz = PYZ(a.pure, a.zipped_data,
             cipher=None)
exe = EXE(pyz,
          a.scripts,
          exclude_binaries=True,
          name='pytripgui',
          debug=False,
          strip=False,
          upx=False,
          console=True )
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
#             datas=[ ('pytripgui/res/*', 'res' )],
#             hiddenimports=['appdirs', 'packaging', 'packaging', 'packaging.version', 'packaging.specifiers', 'packaging.requirements'],
#             hookspath=[],
#             runtime_hooks=[],
#             excludes=['pywin.debugger', 'tcl', 'IPython', 'tornado'],
#             win_no_prefer_redirects=False,
#             win_private_assemblies=False,
#             cipher=None)
#
#a.binaries = [x for x in a.binaries if not x[0].startswith("IPython")]
#a.binaries = [x for x in a.binaries if not x[0].startswith("zmq")]
#
#a.binaries = a.binaries - TOC([
# ('sqlite3.dll', None, None),
# ('_sqlite3', None, None),
# ('_ssl', None, None)])
#
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
#          console=False )

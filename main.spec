# -*- mode: python -*-

block_cipher = None

# one directory installation:
# might be useful when combined with installer generator such as http://www.innosetup.com/isinfo.php
# check get_main_dir() method in pytripgui/util.py before uncommenting this one
# -*- mode: python -*-
#a = Analysis(['pytripgui\\main.py'],
#             pathex=['.'],
#             binaries=[],
#             datas=[ ('pytripgui/res/*', 'res' )],
#             hiddenimports=['wx', 'wx._xml', 'matplotlib', 'FileDialog', 'wx.lib.pubsub', 'wx.lib.pubsub.core.arg1', 'appdirs', 'packaging', 'packaging', 'packaging.version', 'packaging.specifiers', 'packaging.requirements'],
#             hookspath=[],
#             runtime_hooks=[],
#             excludes=['pywin.debugger', 'tcl', 'PyQt5', 'IPython', 'tornado'],
#             win_no_prefer_redirects=False,
#             win_private_assemblies=False,
#             cipher=block_cipher)
#
#a.binaries = [x for x in a.binaries if not x[0].startswith("IPython")]
#a.binaries = [x for x in a.binaries if not x[0].startswith("zmq")]
#
#a.binaries = a.binaries - TOC([
# ('sqlite3.dll', None, None),
# ('_sqlite3', None, None),
# ('_ssl', None, None)])
#
#pyz = PYZ(a.pure, a.zipped_data,
#             cipher=block_cipher)
#exe = EXE(pyz,
#          a.scripts,
#          exclude_binaries=True,
#          name='main',
#          debug=False,
#          strip=False,
#          upx=False,
#          console=True )
#coll = COLLECT(exe,
#               a.binaries,
#               a.zipfiles,
#               a.datas,
#               strip=False,
#               upx=False,
#               name='main')


# one file installation, nice but application has a slow start as each execution is related to unpacking of ~100MB archive
a = Analysis(['pytripgui\\main.py'],
             pathex=['.'],
             binaries=[],
             datas=[ ('pytripgui/res/*', 'res' )],
             # TODO add wx.lib.pubsub.core.kwargs if pubsub API v3 is going to be used
             hiddenimports=['wx', 'wx._xml', 'matplotlib', 'FileDialog', 'wx.lib.pubsub', 'wx.lib.pubsub.core.arg1', 'appdirs', 'packaging', 'packaging', 'packaging.version', 'packaging.specifiers', 'packaging.requirements'],
             hookspath=[],
             runtime_hooks=[],
             excludes=['pywin.debugger', 'tcl', 'PyQt5', 'IPython', 'tornado'],
             win_no_prefer_redirects=False,
             win_private_assemblies=False,
             cipher=block_cipher)

a.binaries = [x for x in a.binaries if not x[0].startswith("IPython")]
a.binaries = [x for x in a.binaries if not x[0].startswith("zmq")]

a.binaries = a.binaries - TOC([
 ('sqlite3.dll', None, None),
 ('_sqlite3', None, None),
 ('_ssl', None, None)])


pyz = PYZ(a.pure)
exe = EXE(pyz,
          a.scripts,
          a.binaries,
          a.zipfiles,
          a.datas,
          name='pytripgui',
          debug=False,
          strip=False,
          upx=True,
          console=False )

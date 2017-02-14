# -*- mode: python -*-

block_cipher = None

a = Analysis(['pytripgui\\main.py'],
             pathex=['.'],
             binaries=[],
             datas=[ ('pytripgui/res/*', 'res' )],
             # TODO add wx.lib.pubsub.core.kwargs if pubsub API v3 is going to be used
             hiddenimports=['wx', 'wx._xml', 'matplotlib', 'FileDialog', 'wx.lib.pubsub', 'wx.lib.pubsub.core.arg1', 'appdirs', 'packaging', 'packaging', 'packaging.version', 'packaging.specifiers', 'packaging.requirements'],
             hookspath=[],
             runtime_hooks=[],
             excludes=['pywin.debugger', 'tcl', 'PyQt5', 'IPython'],
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
          console=True )

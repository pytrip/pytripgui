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
             excludes=[],
             win_no_prefer_redirects=False,
             win_private_assemblies=False,
             cipher=block_cipher)

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

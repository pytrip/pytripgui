# -*- mode: python -*-

block_cipher = None

a = Analysis(['pytripgui\\main.py'],
             pathex=['.'],
             binaries=[],
             datas=[ ('pytripgui/res/*', 'pyinstaller' )],
             # TODO add wx.lib.pubsub.core.kwargs if pubsub API v3 is going to be used
             hiddenimports=['wx', 'wx._xml', 'matplotlib', 'FileDialog', 'wx.lib.pubsub', 'wx.lib.pubsub.core.arg1', 'appdirs', 'packaging', 'packaging', 'packaging.version', 'packaging.specifiers', 'packaging.requirements'],
             hookspath=[],
             runtime_hooks=[],
             excludes=[],
             win_no_prefer_redirects=False,
             win_private_assemblies=False,
             cipher=block_cipher)

print(a)

pyz = PYZ(a.pure, a.zipped_data,
             cipher=block_cipher)
exe = EXE(pyz,
          a.scripts,
          exclude_binaries=True,
          name='main',
          debug=True,
          strip=False,
          upx=True,
          console=True )
coll = COLLECT(exe,
               a.binaries,
               a.zipfiles,
               a.datas,
               strip=False,
               upx=True,
               name='main')
print(coll)
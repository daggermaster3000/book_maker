# -*- mode: python ; coding: utf-8 -*-


a = Analysis(
    ['/Users/quillan/Documents/Gadgets/Books/booklet-maker/booklet_maker.py'],
    pathex=[],
    binaries=[],
    datas=[],
    hiddenimports=[],
    hookspath=[],
    hooksconfig={},
    runtime_hooks=[],
    excludes=[],
    noarchive=False,
)
pyz = PYZ(a.pure)

exe = EXE(
    pyz,
    a.scripts,
    a.binaries,
    a.datas,
    [],
    name='booklet_maker',
    debug=False,
    bootloader_ignore_signals=False,
    strip=False,
    upx=True,
    upx_exclude=[],
    runtime_tmpdir=None,
    console=False,
    disable_windowed_traceback=False,
    argv_emulation=False,
    target_arch=None,
    codesign_identity=None,
    entitlements_file=None,
    icon=['/Users/quillan/Downloads/read_book_study_icon-icons.com_51077.ico'],
)
app = BUNDLE(
    exe,
    name='booklet_maker.app',
    icon='/Users/quillan/Downloads/read_book_study_icon-icons.com_51077.ico',
    bundle_identifier=None,
)

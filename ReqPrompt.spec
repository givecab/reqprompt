# -*- mode: python ; coding: utf-8 -*-

from pathlib import Path
import sys

ROOT_DIR = Path(SPECPATH)
MACOS_ICON = ROOT_DIR / 'build' / 'ReqPrompt.icns'
WINDOWS_ICON = ROOT_DIR / 'assets' / 'icono.ico'

a = Analysis(
    ['main.py'],
    pathex=[],
    binaries=[],
    datas=[('assets', 'assets')],
    hiddenimports=[],
    hookspath=[],
    hooksconfig={},
    runtime_hooks=[],
    excludes=[],
    noarchive=False,
    optimize=0,
)
pyz = PYZ(a.pure)

exe = EXE(
    pyz,
    a.scripts,
    [],
    exclude_binaries=True,
    name='ReqPrompt',
    icon=str(WINDOWS_ICON) if sys.platform == 'win32' and WINDOWS_ICON.exists() else None,
    debug=False,
    bootloader_ignore_signals=False,
    strip=False,
    upx=True,
    console=False,
    disable_windowed_traceback=False,
    argv_emulation=False,
    target_arch=None,
    codesign_identity=None,
    entitlements_file=None,
)
coll = COLLECT(
    exe,
    a.binaries,
    a.datas,
    strip=False,
    upx=True,
    upx_exclude=[],
    name='ReqPrompt',
)
app = BUNDLE(
    coll,
    name='ReqPrompt.app',
    icon=str(MACOS_ICON) if MACOS_ICON.exists() else None,
    bundle_identifier='com.reqprompt.desktop',
)

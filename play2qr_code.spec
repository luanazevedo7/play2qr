# Play2Qr_code.spec

# -*- mode: python ; coding: utf-8 -*-

# IMPORTAÇÕES
import os
from PyInstaller.utils.hooks import collect_data_files

# DEFINIÇÕES
block_cipher = None

a = Analysis(
    ['play2qr_code.py'],
    pathex=['.'],
    binaries=[],
    datas=[],
    hiddenimports=[],
    hookspath=[],
    hooksconfig={},
    runtime_hooks=[],
    excludes=[],
    win_no_prefer_redirects=False,
    win_private_assemblies=False,
    cipher=block_cipher,
    noarchive=False,
)

pyz = PYZ(a.pure, a.zipped_data, cipher=block_cipher)

exe = EXE(
    pyz,
    a.scripts,
    [],
    exclude_binaries=True,
    name='Play2QR',
    debug=False,
    bootloader_ignore_signals=False,
    strip=False,
    upx=True,
    console=True,
    icon='play2qr_icon.ico'  # Ícone do app
)

coll = COLLECT(
    exe,
    a.binaries,
    a.zipfiles,
    a.datas,
    strip=False,
    upx=True,
    upx_exclude=[],
    name='Play2QR'
)
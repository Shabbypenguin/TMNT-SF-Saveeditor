# -*- mode: python ; coding: utf-8 -*-
# Run with: pyinstaller TMNTSF_SaveEditor.spec (from any directory)
# Requires: pip install flask pywebview pyinstaller

import os
HERE      = os.path.dirname(os.path.abspath(SPEC))
REPO_ROOT = os.path.dirname(HERE)

block_cipher = None

a = Analysis(
    [os.path.join(HERE, 'app.py')],
    pathex=[HERE],
    binaries=[],
    datas=[
        (os.path.join(REPO_ROOT, 'index.html'), '.'),
        (os.path.join(REPO_ROOT, 'media'),       'media'),
    ],
    hiddenimports=[
        'flask', 'werkzeug', 'jinja2', 'click',
        'webview', 'webview.platforms.winforms',
        'clr', 'System', 'System.Windows.Forms',
    ],
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
    a.binaries,
    a.zipfiles,
    a.datas,
    [],
    name='TMNTSF_SaveEditor',
    debug=False,
    bootloader_ignore_signals=False,
    strip=False,
    upx=True,
    upx_exclude=[],
    runtime_tmpdir=None,
    console=False,
    disable_windowed_traceback=False,
    target_arch=None,
    codesign_identity=None,
    entitlements_file=None,
    # icon='icon.ico',
)

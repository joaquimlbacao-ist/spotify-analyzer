from PyInstaller.utils.hooks import collect_submodules
import os

project_root = os.getcwd()

src_path = os.path.join(project_root, "src")
frontend_build = os.path.join(project_root, "spotify-frontend", "build")

hiddenimports = collect_submodules("src")

a = Analysis(
    ["app.py"],
    pathex=[project_root],
    binaries=[],
    datas=[
        (frontend_build, "spotify-frontend/build"),
    ],
    hiddenimports=hiddenimports,
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
    name="SpotifyAnalyzer",
    debug=False,
    bootloader_ignore_signals=False,
    strip=False,
    upx=False,
    console=False,
)

app = BUNDLE(
    exe,
    name="Spotify Analyzer.app",
    icon=None,
)
#!/usr/bin/env python3
"""
Build JARVIS-Setup.exe aus dem Tkinter Installer.
Auf Windows ausführen:
    pip install -r requirements.txt
    python installer/build/build_exe.py

Erzeugt: installer/dist/JARVIS-Setup.exe (ca. 30-45 MB)
"""
import subprocess, sys, os, pathlib, shutil
ROOT = pathlib.Path(__file__).resolve().parents[2]
SRC = ROOT / "installer" / "src" / "main.py"
DIST = ROOT / "installer" / "dist"
WORK = ROOT / "installer" / "build" / "work"
SPEC = ROOT / "installer" / "build" / "JarvisSetup.spec"

def main():
    DIST.mkdir(parents=True, exist_ok=True)
    (ROOT / "installer" / "build" / "work").mkdir(parents=True, exist_ok=True)

    # Fallback: wenn PyInstaller fehlt, installiere
    try:
        import PyInstaller
    except ImportError:
        subprocess.check_call([sys.executable, "-m", "pip", "install", "pyinstaller"])

    # Icon erzeugen (falls nicht vorhanden)
    icon_path = ROOT / "installer" / "build" / "arc.ico"
    if not icon_path.exists():
        try:
            from PIL import Image, ImageDraw
            img = Image.new("RGBA", (256,256), (0,0,0,0))
            d = ImageDraw.Draw(img)
            d.ellipse([20,20,236,236], outline=(0,217,255,255), width=8)
            d.ellipse([80,80,176,176], fill=(0,217,255,255))
            d.ellipse([100,100,156,156], fill=(232,253,255,255))
            img.save(icon_path)
            print(f"Icon erzeugt: {icon_path}")
        except: pass

    cmd = [
        sys.executable, "-m", "PyInstaller",
        "--noconfirm",
        "--windowed",
        "--name", "JARVIS-Setup",
        "--distpath", str(DIST),
        "--workpath", str(WORK),
        "--specpath", str(SPEC.parent),
        "--add-data", f"{ROOT / 'installer' / 'src' / 'questionnaire.py'};.",
    ]
    if icon_path.exists():
        cmd += ["--icon", str(icon_path)]
    # onefile für einfachen Download
    cmd += ["--onefile", str(SRC)]

    print(">> Baue:", " ".join(cmd))
    subprocess.check_call(cmd)
    print(f"\n✓ Fertig: {DIST / 'JARVIS-Setup.exe'}  (auf Windows testen: Doppelklick)")
    print(f"  Größe: { (DIST / 'JARVIS-Setup.exe').stat().st_size / 1024/1024:.1f} MB")

if __name__ == "__main__":
    main()

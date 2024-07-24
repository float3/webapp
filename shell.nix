{pkgs ? import <nixpkgs> {}}:
pkgs.mkShell {
  buildInputs = with pkgs; [
    exiftool
    ffmpeg
    python312Full
    python312Packages.gunicorn
    python312Packages.flask
    python312Packages.watchdog
    python312Packages.setuptools
    python312Packages.pillow
    python312Packages.python-magic
  ];
}

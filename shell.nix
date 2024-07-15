{pkgs ? import <nixpkgs> {}}:
pkgs.mkShell {
  buildInputs = with pkgs; [
    python312Full
    python312Packages.gunicorn
    python312Packages.flask
    python312Packages.watchdog
    python312Packages.pyexiftool
    python312Packages.ffmpeg-python
    python312Packages.setuptools
  ];
}

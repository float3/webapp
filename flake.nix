{
  description = "trolley";

  inputs = {
    nixpkgs.url = "github:nixos/nixpkgs/nixos-unstable";
  };

  outputs = {
    self,
    nixpkgs,
  }: {
    packages = {
      default = nixpkgs.lib.buildPythonApplication {
        pname = "trolley";
        version = "1.0";
        src = ./.;
        propagatedBuildInputs = with nixpkgs.python312Packages; [
          gunicorn
          flask
          watchdog
          pyexiftool
          ffmpeg-python
          pillow
        ];
      };
    };

    devShell = {
      default = nixpkgs.mkShell {
        buildInputs = with nixpkgs.pkgs; [
          python312Full
          python312Packages.gunicorn
          python312Packages.flask
          python312Packages.watchdog
          python312Packages.pyexiftool
          python312Packages.ffmpeg-python
          python312Packages.setuptools
          python312Packages.pillow
        ];
      };
    };
  };
}

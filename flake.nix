{
  description = "trolley";

  inputs = {
    nixpkgs.url = "github:nixos/nixpkgs/nixos-unstable";
  };

  outputs = {
    self,
    nixpkgs,
  }: {
    packages.x86_64-linux.trolley = nixpkgs.lib.buildPythonApplication {
      pname = "trolley";
      version = "1.0";
      src = ./.;
      propagatedBuildInputs = with nixpkgs.python312Packages; [flask gunicorn watchdog pyexiftool ffmpeg-python setuptools];
    };

    devShells.x86_64-linux = nixpkgs.mkShell {
      buildInputs = with nixpkgs.python312Packages; [flask gunicorn watchdog pyexiftool ffmpeg-python setuptools];
    };
  };
}

{
  description = "My Application";

  inputs = {
    nixpkgs.url = "github:NixOS/nixpkgs/nixos-unstable";
    flake-utils.url = "github:numtide/flake-utils";
  };

  outputs = {
    self,
    nixpkgs,
    flake-utils,
  }:
    flake-utils.lib.eachSystem ["x86_64-linux"] (
      system: let
        pkgs = import nixpkgs {inherit system;};
      in {
        packages.myapp = pkgs.mkShell {
          buildInputs = with pkgs; [
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

        devShell = self.packages.${system}.myapp;

        nixosModules.myapp = {
          imports = [pkgs.nixosModules.trolley];

          config = {
            services.trolleyserver = {
              enable = true;
              package = self.packages.${system}.myapp;
              serviceConfig = {
                ExecStarht = "${self.packages.${system}.myapp}/bin/gunicorn -c gunicorn_config.py app:app";
                Restart = "always";
              };
            };
          };
        };
      }
    );
}

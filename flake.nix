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
          buildInputs = [
            pkgs.python312Full
            pkgs.python312Packages.flask
            pkgs.python312Packages.watchdog
            pkgs.python312Packages.pillow
            pkgs.python312Packages.ffmpeg-python
            pkgs.python312Packages.pyexiftool
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
                ExecStart = "${self.packages.${system}.myapp}/bin/python myapp.py";
                Restart = "always";
              };
            };
          };
        };
      }
    );
}

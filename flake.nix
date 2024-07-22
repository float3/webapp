{
  description = "source for problem.traeumerei.dev";

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
        packages.webapp = pkgs.mkShell {
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

        devShell = self.packages.${system}.webapp;

        nixosModules.webapp = {
          config = {
            config,
            pkgs,
            ...
          }: {
            users.users.trolley = {
              isSystemUser = true;
              createHome = true;
            };

            services.trolleyserver = {
              enable = true;
              package = self.packages.${system}.webapp;
              serviceConfig = {
                ExecStart = "${self.packages.${system}.webapp}/bin/gunicorn -c gunicorn_config.py app:app";
                Restart = "always";
                User = "trolley";
                Group = "trolley";
              };
            };
          };
        };
      }
    );
}

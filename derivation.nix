{
  lib,
  python312Packages,
}:
with python312Packages;
  buildPythonApplication {
    pname = "trolley";
    version = "1.0";

    propagatedBuildInputs = [flask gunicorn watchdog pillow setuptools python-magic];

    src = ./.;
  }

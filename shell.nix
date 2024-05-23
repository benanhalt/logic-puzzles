{ pkgs ? import <nixpkgs> {} }:
pkgs.mkShell {
  buildInputs = with pkgs; [ python3 python3Packages.z3 python3Packages.setuptools];
}

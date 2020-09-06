with import <nixpkgs> { };
with python3Packages;

let
  motor = callPackage ./motor.nix { };
  makefun = callPackage ./makefun.nix { inherit fetchPypi; };
in (python3.withPackages
  (ps: with ps; [ fastapi pyjwt makefun motor passlib uvicorn ])).env

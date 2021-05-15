{ pkgs ? import <nixpkgs> {} }:

with pkgs;

let

interpreter = (import ./requirements.nix rec {
  python3 = pkgs.python3;
  buildPythonPackage = python3.pkgs.buildPythonPackage;
  fetchFromGitHub = pkgs.fetchFromGitHub;
  lib = pkgs.lib;
  fetchPypi = python3.pkgs.fetchPypi;
  lxml = python3.pkgs.lxml;
  requests = python3.pkgs.requests;
  pytz = python3.pkgs.pytz;
  dateutil = python3.pkgs.dateutil;
  future = python3.pkgs.future;
  starlette = python3.pkgs.starlette;
  pydantic = python3.pkgs.pydantic;
  graphene = pkgs.graphene;
});

in

{
  simplepodcast = stdenv.mkDerivation {
    name = "simplepodcast";
    src = ./.;
    unpackPhase = ":";
    installPhase = ''
      mkdir -p $out/bin

      ln -s $src $out/lib

      echo '#!${pkgs.bash}/bin/bash' >> $out/bin/simplepodcast
      echo export PYTHONPATH="$out/lib" >> $out/bin/simplepodcast
      echo ${interpreter}/bin/uvicorn --host \$LISTEN_HOST --port \$LISTEN_PORT simplepodcast:app >> $out/bin/simplepodcast
      chmod +x $out/bin/simplepodcast
    '';
    buildInputs = [
      interpreter
    ];
  };
  interpreter = interpreter;
}
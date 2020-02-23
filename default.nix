{ pkgs ? import <nixpkgs> {} }:

with pkgs;

let

interpreter = (import ./requirements.nix { inherit pkgs; }).interpreter;

in

stdenv.mkDerivation {
    name = "simplepodcast";
    src = ./.;
    unpackPhase = ":";
    installPhase = ''
        mkdir -p $out/bin

        ln -s $src $out/lib

        echo '#!${pkgs.bash}/bin/bash' >> $out/bin/simplepodcast
        echo export PYTHONPATH="$out/lib" >> $out/bin/simplepodcast
        echo ${interpreter}/bin/uvicorn simplepodcast:app >> $out/bin/simplepodcast
        chmod +x $out/bin/simplepodcast
    '';
    buildInputs = [ interpreter ];
}

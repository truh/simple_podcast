{ pkgs ? import <nixpkgs> {} }:

with pkgs;

let

interpreter = (import ./requirements.nix { inherit pkgs; }).interpreter;

in

stdenv.mkDerivation {
    name = "simplepodcast";
    src = ./.;
    unpackPhase = ''
    ls $src
    '';
    installPhase = ''
        mkdir -p $out/bin
        mkdir -p $out/lib
        echo 'ls $src'
        ls $src
        echo 'echo $src/*py'
        echo $src/*py
        cp $src/*py $out/lib

        echo '#!${pkgs.bash}/bin/bash' >> $out/bin/simplepodcast
        echo export PYTHONPATH="$out/lib" >> $out/bin/simplepodcast
        echo ${interpreter}/bin/uvicorn simplepodcast:app >> $out/bin/simplepodcast
        chmod +x $out/bin/simplepodcast
    '';
    buildInputs = [ interpreter ];
}

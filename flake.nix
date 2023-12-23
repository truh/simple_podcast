{
  description = "Application packaged using poetry2nix";

  inputs = {
    nixpkgs.url = "github:NixOS/nixpkgs/nixos-unstable";
    flake-utils.url = "github:numtide/flake-utils";
    poetry2nix = {
      url = "github:nix-community/poetry2nix";
      inputs.nixpkgs.follows = "nixpkgs";
      inputs.flake-utils.follows = "flake-utils";
      inputs.systems.follows = "flake-utils/systems";
    };
  };

  outputs = {
    self,
    nixpkgs,
    flake-utils,
    poetry2nix,
  }:
    flake-utils.lib.eachDefaultSystem (system: let
      pkgs = nixpkgs.legacyPackages.${system};
      inherit (poetry2nix.lib.mkPoetry2Nix {inherit pkgs;}) mkPoetryApplication mkPoetryEnv defaultPoetryOverrides overrides;
    in {
      formatter = pkgs.alejandra;

      packages = {
        simplepodcast = mkPoetryApplication {
          projectDir = self;
          overrides = overrides.withDefaults (self: super: {
            tinytag = super.tinytag.overridePythonAttrs (old: {
              buildInputs = (old.buildInputs or []) ++ [super.setuptools];
            });
            podgen = super.podgen.overridePythonAttrs (old: {
              buildInputs = (old.buildInputs or []) ++ [super.setuptools];
            });
          });
        };
        default = self.packages.${system}.simplepodcast;
      };

      devShells.default = pkgs.mkShell {
        inputsFrom = [self.packages.${system}.simplepodcast];
        packages = [
          pkgs.poetry
          pkgs.pre-commit
        ];
      };
    });
}

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
    })
    // {
      nixosModules.default = {
        config,
        lib,
        stdenv,
        pkgs,
        ...
      }:
        with lib; {
          options.services.simplepodcast = {
            enable = mkEnableOption "Enable Simple Podcast service";
            package = mkOption {
              default = self.packages.${pkgs.system}.simplepodcast;
              type = types.package;
            };
            publicUrl = mkOption {
              type = types.str;
            };
            listenHost = mkOption {
              default = "127.0.0.1";
              type = types.str;
            };
            listenPort = mkOption {
              default = 8000;
              type = types.port;
            };
            sqlalchemyDatabaseUrl = mkOption {
              default = "sqlite:///var/lib/simplepodcast/simplepodcast.sqlite3";
              type = types.str;
            };
            uploadDir = mkOption {
              default = "/var/lib/simplepodcast/uploads";
              type = types.str;
            };
          };

          config = mkIf config.services.simplepodcast.enable {
            environment.etc."simplepodcast.conf".text = with config.services.simplepodcast; ''
              PUBLIC_URL=${publicUrl}
              SQLALCHEMY_DATABASE_URL=${sqlalchemyDatabaseUrl}
              UPLOAD_DIR=${uploadDir}
            '';

            systemd.services.simplepodcast = {
              description = "Simple Podcast";
              after = ["network-online.target"];
              wantedBy = ["multi-user.target"];
              path = [config.services.simplepodcast.package];
              serviceConfig = {
                ExecStart = "start-simplepodcast";
                ExecReload = "${pkgs.coreutils}/bin/kill -HUP $MAINPID";
                User = "simplepodcast";
                Group = "simplepodcast";
              };
              environment = {
                SIMPLEPODCAST_CONFIG = "/etc/simplepodcast.conf";
                LISTEN_HOST = config.services.simplepodcast.listenHost;
                LISTEN_PORT = toString config.services.simplepodcast.listenPort;
              };
            };

            users.users.simplepodcast = {
              createHome = true;
              home = "/var/lib/simplepodcast";
              isSystemUser = true;
              group = "simplepodcast";
            };
            users.groups.simplepodcast = {
              members = ["simplepodcast"];
            };
          };
        };
    };
}

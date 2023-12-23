{
  config,
  lib,
  stdenv,
  pkgs,
  ...
}: let
  simplepodcast = (pkgs.callPackage ./default.nix {}).simplepodcast;
in
  with lib; {
    options.services.simplepodcast = {
      enable = mkEnableOption "Enable Simple Podcast service";
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
        serviceConfig = {
          ExecStart = "${simplepodcast}/bin/simplepodcast";
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
  }

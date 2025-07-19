{ config, lib, utils, pkgs, ... }:

let
  cfg = config.services.tasks;
in
{
  options.services.tasks = {
    enable = lib.mkEnableOption "Tasks web app service";

    user = lib.mkOption {
      type = lib.types.str;
      default = "tasks";
      description = ''
        User account under which TASKS runs.
      '';
    };

    group = lib.mkOption {
      type = lib.types.str;
      default = "tasks";
      description = ''
        Group under which TASKS runs.
      '';
    };

    dbPath = lib.mkOption {
      type = lib.types.path;
      description = ''
        Folder in which the SQLite DB will be stored.
      '';
    };

    package = lib.mkPackageOption pkgs "tasks" {
      nullable = true;
      default = null;
    };

    bindIp = lib.mkOption {
      type = lib.types.str;
      default = "127.0.0.1";
      description = "IP to bind the Gunicorn server to";
    };

    bindPort = lib.mkOption {
      type = lib.types.port;
      default = 8000;
      description = "Port to bind the Gunicorn server to";
    };

    workers = lib.mkOption {
      type = lib.types.int;
      default = 2;
      description = "Number of Gunicorn workers to run";
    };
  };

  config = lib.mkIf cfg.enable {
    systemd.services.tasks = {
      description = "TASKS App";
      after = [ "network.target" ];
      wantedBy = [ "multi-user.target" ];
      serviceConfig = {
        Type = "simple";
        User = cfg.user;
        Group = cfg.group;

        Environment = "PYTHONUNBUFFERED=1";
        WorkingDirectory = cfg.dbPath; 

        ExecStart = utils.escapeSystemdExecArgs [
          (lib.getExe cfg.package)
          "-w ${toString cfg.workers}"
          "-b ${cfg.bindIp}:${toString cfg.bindPort}"
        ];

        # systemd hardening. Use command below to check.
        # systemd-analyze --no-pager security tasks.service
        CapabilityBoundingSet = null;
        PrivateDevices = true;
        PrivateTmp = true;
        PrivateUsers = true;
        ProtectHome = true;
        RestrictNamespaces = true;
        SystemCallFilter = "@system-service";
      };
    };
  };
}


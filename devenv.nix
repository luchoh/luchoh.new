{ pkgs, lib, config, inputs, ... }:

{
  # https://devenv.sh/basics/
  env.GREET = "luchoh.com";

  # https://devenv.sh/packages/
  packages = [ pkgs.git pkgs.poetry pkgs.pkg-config ];

  # https://devenv.sh/scripts/
  scripts.hello.exec = "echo hello from $GREET";

  enterShell = ''
    hello
    git --version
  '';

  # https://devenv.sh/tests/
  enterTest = ''
    echo "Running tests"
    git --version | grep "2.42.0"
  '';

  # https://devenv.sh/languages/
  languages.python = {
    enable = true;
    version = "3.11";
    poetry = {
      enable = true;
      activate.enable = true;
      install.enable = true;
    };
  };

  # MySQL service configuration
  services.mysql = {
    enable = true;
    package = pkgs.mysql;
    initialDatabases = [{ name = "luchoh_photography"; }];
    ensureUsers = [{
      name = "luchoh";
      ensurePermissions = { "luchoh_photography.*" = "ALL PRIVILEGES"; };
    }];
    settings = {
      mysqld = {
        bind-address = "127.0.0.1";
        port = 3306;
      };
    };
  };

  # Environment variables for database connection
  env.DATABASE_URL = "mysql+pymysql://luchoh@127.0.0.1:3306/luchoh_photography";

  # https://devenv.sh/processes/
  # processes.ping.exec = "ping example.com";

  # See full reference at https://devenv.sh/reference/options/
}

{ pkgs, lib, config, inputs, ... }:

{
  # https://devenv.sh/basics/
  env.GREET = "luchoh-front";

  # https://devenv.sh/packages/
  packages = [ pkgs.git pkgs.process-compose ];

  # https://devenv.sh/scripts/
  scripts.hello.exec = "echo hello from $GREET";

  enterShell = ''
    hello
    git --version
    npm start
  '';

  # https://devenv.sh/tests/
  enterTest = ''
    echo "Running tests"
    git --version | grep "2.42.0"
  '';

  # https://devenv.sh/services/
  # services.postgres.enable = true;

  # https://devenv.sh/languages/
  languages = {
    javascript = {
      enable = true;
      npm = {
        enable = true;
        install = { enable = true; };
      };
    };
  };

  # https://devenv.sh/pre-commit-hooks/
  # pre-commit.hooks.shellcheck.enable = true;

  # https://devenv.sh/processes/
  # processes.ping.exec = "ping example.com";
  # processes = { npm = { exec = "npm start"; }; };

  # See full reference at https://devenv.sh/reference/options/
}

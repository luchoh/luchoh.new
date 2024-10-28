{ pkgs, lib, config, inputs, ... }: {
  packages = [
    pkgs.git
    pkgs.poetry
    pkgs.pkg-config
    pkgs.postgresql # This adds psql and other PostgreSQL client tools
  ];

  scripts.hello.exec = "echo hello from $GREET";

  languages = {
    python = {
      enable = true;
      version = "3.11";
      poetry = {
        enable = true;
        activate.enable = true;
        install.enable = true;
      };
    };
  };

  processes.postgres = {
    exec =
      "${pkgs.postgresql}/bin/postgres -D $DEVENV_ROOT/postgres-data -k $DEVENV_ROOT/postgres-data -p 5445";
  };

  env = {
    GREET = "luchoh-backend";
    DATABASE_URL =
      "postgresql://luchoh:luchoh.com@127.0.0.1:5445/luchoh_photography";
  };

  enterShell = ''
    hello
    git --version
    if [ ! -d "$DEVENV_ROOT/postgres-data" ]; then
      mkdir -p "$DEVENV_ROOT/postgres-data"
      ${pkgs.postgresql}/bin/initdb \
        --auth=trust \
        --no-locale \
        --encoding=UTF8 \
        -D "$DEVENV_ROOT/postgres-data"
      
      ${pkgs.postgresql}/bin/pg_ctl -D "$DEVENV_ROOT/postgres-data" -l "$DEVENV_ROOT/postgres-data/postgresql.log" -o "-p 5433" start
      ${pkgs.postgresql}/bin/createdb -p 5433 luchoh_photography
      ${pkgs.postgresql}/bin/psql -p 5433 -d luchoh_photography -c "CREATE USER luchoh WITH PASSWORD 'luchoh.com' SUPERUSER;"
      ${pkgs.postgresql}/bin/pg_ctl -D "$DEVENV_ROOT/postgres-data" stop
    fi
  '';
}

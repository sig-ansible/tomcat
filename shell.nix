let
  nixpkgs = import <nixpkgs> { };
  # nix-dev = builtins.getFlake (toString ../nix-dev);
  nix-dev = builtins.getFlake "github:sigdba/nix-dev";
in nixpkgs.mkShell
(nix-dev.shell.${builtins.currentSystem} { name = "sig-ansible/tomcat"; })

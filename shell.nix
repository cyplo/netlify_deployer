let
  pkgs = import <nixpkgs> {};
in
pkgs.mkShell {
  buildInputs = with pkgs; with pkgs.python38Packages; [
      git
      setuptools
      wheel
      pbr
      cacert
      requests
      pip
      virtualenv
  ];
}

{
  inputs = {
    nixpkgs.url = "github:nixos/nixpkgs/nixos-25.05";
  };

  outputs = inputs: 
  let 
    system = "x86_64-linux";
    pkgs = import inputs.nixpkgs {inherit system;};
    py = pkgs.python311.withPackages(p: with p;[
        django
        flask
        requests
        textual
        mariadb
        pyyaml
        mypy
    ]
  );
  in {
    devShells.${system}.default = pkgs.mkShell {
        buildInputs = [
          py 
          pkgs.sqlite
          pkgs.git
        ];
        shellHook = ''
          export FLAKE_DIR=$(pwd)
          export PYTHONPATH=$PYTHONPATH:$(echo ${py}/lib/python*/site-packages)
        '';
      };
  };
}

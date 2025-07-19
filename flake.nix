{
  description = "TASKS - A basic task list";

  nixConfig.bash-prompt-prefix = "(tasks) ";

  inputs = {
    nixpkgs.url = "github:nixos/nixpkgs/nixos-unstable";
    flake-utils.url = "github:numtide/flake-utils";
  };

  outputs = { self, nixpkgs, flake-utils }:
    flake-utils.lib.eachDefaultSystem (system:
      let
        # Define propagatedBuildInputs here to avoid variable declaration error
        pbi = [
            pkgs.python3Packages.flask
            pkgs.python3Packages.sqlalchemy
            pkgs.python3Packages.gunicorn
        ];

        pkgs = import nixpkgs { inherit system; };
      
        pyproject = builtins.fromTOML (builtins.readFile ./pyproject.toml);
        project = pyproject.project;

        tasks = pkgs.python3Packages.buildPythonPackage {
          pname = project.name;
          inherit (project) version; 
          format = "pyproject";
          src = ./.;
          build-system = with pkgs.python3Packages; [
            hatchling
          ];
          
          nativeCheckInputs = with pkgs.python3Packages; [
            pytest
            ruff
          ];

          checkPhase = ''
            runHook preCheck
            pytest
            runHook postCheck
          '';

          propagatedBuildInputs = pbi;

          # Idea of using postFixup to create the wrapper came from [3]. I couldn't get the
          # application to find the dependencies correctly until I setup this wrapper.
          # The creation of the bash script itself could probably be replaced with
          # writeShellScriptBin.
          postFixup =
            ''
              mkdir -p $out/bin/
	      echo "${pkgs.python3Packages.gunicorn}/bin/gunicorn \"\$@\" \"tasks:create_app()\"" >> $out/bin/tasks
              chmod +x $out/bin/tasks
            ''
            + ''
              wrapProgram $out/bin/tasks \
            ''
            + ''
              --set PYTHONPATH "${pkgs.python3.pkgs.makePythonPath pbi}:$out/${pkgs.python3.sitePackages}"
            '';

          meta.mainProgram = "tasks";
        };

        editablePackage = pkgs.python3.pkgs.mkPythonEditablePackage {
          pname = project.name;
          inherit (project) version;
          root = "$PWD";
        };

      in
      {
        packages = {
          ${project.name} = tasks;
          default = self.packages.${system}.${project.name}; 
        };

        devShells = {
          default = pkgs.mkShell {
            inputsFrom = [
               tasks
            ]; 
            
            buildInputs = [
              editablePackage
            ];
          };
        };
      }) // {
        nixosModules.tasks = import ./module.nix;
      };
}

# [1]:https://github.com/vst/nix-flake-templates/blob/main/templates/python-package/flake.nix
# [2]:https://github.com/NixOS/nixpkgs/blob/master/doc/languages-frameworks/python.section.md
# [3]:https://github.com/NixOS/nixpkgs/blob/955cd97f6f3c9fc3068706ffc5a492cc28bc71f5/pkgs/by-name/az/azure-cli/package.nix

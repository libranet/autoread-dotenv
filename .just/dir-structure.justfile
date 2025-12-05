# See ../justfile
#
# - justfile_directory() is the directory of the toplevel justfile


# prepend local bin-directory to $PATH
venv_bin_dir := if os_family() == "windows" { justfile_directory() / ".venv/Scripts" } else { justfile_directory() / ".venv/bin" }
export PATH := if os_family() == "windows" { venv_bin_dir + x";${PATH}" } else { venv_bin_dir + x":${PATH}" }


# initialize dir-structure, create dirs
[group: 'dir-structure']
[unix]
create-dirs:
    # vscode does not create cache-dirs, so we need to create it
    @ echo -e "In current working dir: ${PWD}"
    @ echo -e "Creating project directory-structure:"
    mkdir -p var
    mkdir -p var/cache
    mkdir -p var/cache/mypy
    mkdir -p var/cache/vscode
    mkdir -p var/coverage
    mkdir -p var/log
    mkdir -p var/run
    mkdir -p var/tmp
    @ echo -e ""

# initialize dir-structure, create dirs
[group: 'dir-structure']
[windows]
create-dirs:
    #!pwsh.exe
    Write-Host "In current working dir: $(Get-Location)"
    Write-Host "Creating project directory-structure:"
    New-Item -ItemType Directory -Path var -Force | Out-Null
    New-Item -ItemType Directory -Path var/cache -Force | Out-Null
    New-Item -ItemType Directory -Path var/cache/mypy -Force | Out-Null
    New-Item -ItemType Directory -Path var/cache/vscode -Force | Out-Null
    New-Item -ItemType Directory -Path var/coverage -Force | Out-Null
    New-Item -ItemType Directory -Path var/log -Force | Out-Null
    New-Item -ItemType Directory -Path var/run -Force | Out-Null
    New-Item -ItemType Directory -Path var/tmp -Force | Out-Null
    Write-Host ""


# symlinks to venv-dirs to make bin/python work
[group: 'dir-structure']
[unix]
symlink-venv-dirs:
    @ echo -e "Creating .venv-symlinks:"
    ln -sf .venv/bin
    ln -sf .venv/lib
    ln -sf .venv/lib64
    ln -sf .venv/pyvenv.cfg
    @ echo -e ""

# symlinks to venv-dirs to make bin/python work
[group: 'dir-structure']
[windows]
symlink-venv-dirs:
    #!pwsh
    Write-Host "Creating .venv-symlinks"
    New-Item -ItemType SymbolicLink -Name "bin" -Target ".venv/Scripts" -Force | Out-Null
    New-Item -ItemType SymbolicLink -Name "lib" -Target ".venv/Lib" -Force | Out-Null
    # New-Item -ItemType SymbolicLink -Name "lib64" -Target ".venv/Lib" -Force | Out-Null
    New-Item -ItemType SymbolicLink -Name "pyvenv.cfg" -Target ".venv/pyvenv.cfg" -Force | Out-Null
    Write-Host ""

# remove venv-symlinks
[group: 'dir-structure']
clean-symlinks:
    rm -f bin
    rm -f lib
    rm -f lib64
    rm -f pyvenv.cfg

alias clear-symlinks := clean-symlinks


# remove .venv-directory
[group: 'dir-structure']
clean-venv:
    rm -fr .venv

alias clear-venv := clean-venv


# remove all __pycache__-folders
[group: 'dir-structure']
clean-pyhon-cache-files:
    find . -type d -name "__pycache__" -exec rm -rf {} +


# clean up all generated files
[group: 'dir-structure']
clean: clean-symlinks clean-venv clean-pyhon-cache-files
    rm -fr var/cache
    rm -fr var/log

alias clear := clean

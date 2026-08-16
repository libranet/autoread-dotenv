# See ../makefile
#
# Benchmarks for the startup-time cost autoread-dotenv adds via the sitecustomize hook.
# See docs/performance.md for the methodology, current numbers, and how to read them.
#
# Requires `hyperfine` (https://github.com/sharkdp/hyperfine) on PATH for benchmark-startup.
# That is a Rust CLI binary, NOT the PyPI package of the same name (`pip install hyperfine` /
# `uv add hyperfine` installs an unrelated scientific-fitting library that pulls in numpy,
# jax, scipy, pandas, iminuit). Install hyperfine via your system package manager instead,
# e.g. `apt install hyperfine`, `brew install hyperfine`, or `cargo install hyperfine`.


# check that the real (Rust) hyperfine is on PATH, not the unrelated PyPI package
[group: 'benchmark']
benchmark-check-hyperfine:
	@command -v hyperfine >/dev/null || { \
		echo "hyperfine not found on PATH."; \
		echo "Install: https://github.com/sharkdp/hyperfine#installation"; \
		echo "(NOT 'pip install hyperfine' / 'uv add hyperfine' - that installs an unrelated PyPI package)."; \
		exit 1; \
	}


# compare python startup time: bare venv vs sitecustomize-entrypoints vs autoread-dotenv
[group: 'benchmark']
benchmark-startup: benchmark-check-hyperfine
	#!/usr/bin/env bash
	# Builds throwaway venvs in a tempdir (no side-effects on this project's own .venv):
	# bare / sitecustomize-entrypoints-only / autoread-dotenv-without-.env /
	# autoread-dotenv-with-.env. Prints a markdown table - copy the numbers you want to
	# keep into docs/performance.md, noting the date, `uv --version`, `python --version`,
	# and how many packages were installed in the compared venvs.
	set -euo pipefail
	workdir="$(mktemp -d)"
	trap 'rm -rf "$workdir"' EXIT

	echo "Building throwaway venvs in $workdir ..." >&2
	uv venv --python 3.14 "$workdir/bare" -q
	uv venv --python 3.14 "$workdir/ste-only" -q
	uv pip install --python "$workdir/ste-only/bin/python" sitecustomize-entrypoints -q
	uv venv --python 3.14 "$workdir/autoread" -q
	uv pip install --python "$workdir/autoread/bin/python" . -q
	echo "FOO=bar" > "$workdir/dotenv-fixture.env"

	hyperfine --warmup 10 --min-runs 50 \
		-n "bare venv (no sitecustomize hooks)" \
			"$workdir/bare/bin/python -c pass" \
		-n "sitecustomize-entrypoints only (no entries registered)" \
			"$workdir/ste-only/bin/python -c pass" \
		-n "autoread-dotenv installed, no .env found" \
			"$workdir/autoread/bin/python -c pass" \
		-n "autoread-dotenv installed, .env loaded" \
			"env AUTOREAD_DOTENV_PATH=$workdir/dotenv-fixture.env $workdir/autoread/bin/python -c pass"


# show which imports the sitecustomize hook pulls in and what they cost
[group: 'benchmark']
benchmark-importtime:
	# Complements benchmark-startup (total end-to-end cost) with an attribution breakdown:
	# which specific imports the hook triggers. Uses this project's own dev .venv, so the
	# numbers include however many dev-dependencies happen to be installed there - see
	# docs/performance.md for why that matters (entry-point discovery scans every
	# installed distribution, not just autoread-dotenv's own dependencies).
	uv run python -X importtime -c pass 2>&1 | grep -E \
		"dotenv|autoread_dotenv|importlib_metadata$|importlib\.metadata$|sitecustomize$|\\| site$"

# Performance

`autoread-dotenv` hooks into `sitecustomize`, which runs on the start of *every* Python
process in the venv - short-lived CLI invocations, `pytest`, `pip`/`uv` themselves, and so
on. That makes its startup-time cost worth measuring and tracking explicitly, rather than
assuming it away.

## Summary

Measured with `hyperfine` (see "Methodology" section below), comparing four scenarios in
throwaway venvs:

| Scenario                                                     |             Mean | vs. bare venv |
| ------------------------------------------------------------ | ---------------: | ------------: |
| Bare venv, no sitecustomize hooks at all                     | 12.3 ms ± 0.5 ms |         1.00x |
| `sitecustomize-entrypoints` installed, no entries registered | 36.5 ms ± 1.8 ms |         2.97x |
| `autoread-dotenv` installed, no `.env` found                 | 38.7 ms ± 3.7 ms |         3.14x |
| `autoread-dotenv` installed, `.env` loaded                   | 58.0 ms ± 2.5 ms |         4.71x |

Measured 2026-08-16, uv 0.12.3, hyperfine 1.20.0, Python 3.14.7, Linux x86_64. Each venv had
only the packages named above installed (see "Methodology" section for why that matters).
Re-run `just benchmark-startup` to reproduce/update these numbers - they are a point-in-time
snapshot, not a guarantee.

**Reading these numbers:**

- The jump from "bare venv" to "`sitecustomize-entrypoints` only" (+24.2 ms) is the cost of
  the entry-point *discovery* mechanism itself - scanning every installed distribution's
  metadata for a registered `sitecustomize` entry point - and happens regardless of whether
  autoread-dotenv is one of the packages found. This is not something autoread-dotenv
  controls or can optimize away; it is the fixed cost of opting into
  `sitecustomize-entrypoints` at all.
- **"No `.env` found" now costs essentially nothing beyond that floor** (38.7 ms vs. 36.5 ms
  for the bare hook mechanism - within noise). This is the result of the fix described
  below; it used to cost 60.4 ms, +~24 ms over the same floor. See "What was fixed".
- "`.env` loaded" still costs +~21 ms over the floor (58.0 ms), because actually loading a
  `.env` requires importing `python-dotenv` - that part of the cost is real, unavoidable
  work, not overhead.
- All of these numbers scale with **how many packages are installed in the venv**, because
  the entry-point discovery scan has to check all of them, not just autoread-dotenv's own
  dependencies. A real project's venv (with its own dependencies, dev tools, etc.) will see
  a larger absolute number than the minimal venvs used here. `just benchmark-importtime`
  (below) uses this project's own ~95-package dev venv for that reason, and shows
  proportionally larger absolute numbers for the same relative breakdown.

## What was fixed

Measuring this surfaced two things that were costing every process a lookup or an import it
usually didn't need, regardless of whether there was a `.env` to load:

1. **`import dotenv` was eager.** [`src/autoread_dotenv/__init__.py`](../src/autoread_dotenv/__init__.py)
   used to `import dotenv` (python-dotenv) unconditionally at module level, before
   `entrypoint()` even checked whether a `.env` file exists. Fixed: `entrypoint()` now
   checks `get_dotenv_path()` *first*, and only imports `dotenv` once it knows there's an
   actual file to hand to `dotenv.load_dotenv()`. No `.env` found -> `dotenv` is never
   imported.

1. **`autoread_dotenv.about`'s metadata lookup was eager, and pulled in unconditionally.**
   `about.py` called `importlib.metadata.metadata()` at module level purely to populate
   `__version__`/`__author__`/`__license__` on the `autoread_dotenv` package - and
   `__init__.py` re-exported those three names, which forced `about.py` to be imported (and
   its metadata lookup to run) on every process start via the sitecustomize hook, whether or
   not anything ever read them. Fixed by removing that re-export: `__init__.py` no longer
   imports `about.py` at all, so its cost is paid only if something explicitly does
   `from autoread_dotenv.about import version` (as the test-suite does) - never as a side
   effect of the sitecustomize hook firing.

   **This is a breaking change to the public API:** `autoread_dotenv.__version__`,
   `__author__`, and `__license__` no longer exist. Use
   `autoread_dotenv.about.version`/`.license_`/`.authors` directly if you need them (see
   `about.py` - unchanged, still eager, but now only runs when you actually import it).

Net effect: the "no `.env` found" scenario dropped from 60.4 ms to 38.7 ms - it now sits
right at the `sitecustomize-entrypoints`-only floor, meaning autoread-dotenv itself adds
essentially nothing in that case anymore. The "`.env` loaded" scenario only dropped slightly
(59.6 ms -> 58.0 ms), because it still needs to import `dotenv` to actually do its job - see
"Where the remaining cost goes" below for confirmation neither `dotenv` nor
`autoread_dotenv.about` show up in the "no `.env`" import tree anymore.

## Where the remaining cost goes

`python -X importtime` breaks down import cost per module. Filtered to the relevant lines
(via `just benchmark-importtime`, run against this project's own dev venv, which has a real
`.env`):

```text
import time:      2223 |      38934 |     sitecustomize._vendor.importlib_metadata
import time:       358 |        358 |     autoread_dotenv.utils
import time:       464 |        464 |     autoread_dotenv.warnings
import time:      1149 |       1149 |         dotenv.parser
import time:       585 |        585 |         dotenv.variables
import time:      1063 |      23467 |       dotenv.main
import time:       508 |      23975 |     dotenv
import time:     12760 |      81876 |   sitecustomize
import time:      2745 |      94071 | site
```

(First column is self-time in µs, second is cumulative including sub-imports, both in
`site`'s subtree.) Note `autoread_dotenv.about` no longer appears in this tree at all - only
`utils` and `warnings`, both negligible. `dotenv` still does, because a `.env` was actually
found and loaded here; re-running against a venv with no `.env` drops the `dotenv` lines too,
leaving only `autoread_dotenv.utils`/`warnings` under `sitecustomize`.

What's left is `sitecustomize-entrypoints`'s own entry-point discovery scan (not
autoread-dotenv's to optimize) and, when a `.env` is actually found, the real cost of
importing `python-dotenv` to load it.

## Conclusions

1. **autoread-dotenv no longer meaningfully adds to the hook-mechanism tax when there's no
   `.env` to load.** Before the fix, autoread-dotenv doubled the cost of opting into
   `sitecustomize-entrypoints` at all (+~24 ms on top of the +~24 ms discovery-scan floor).
   After: the "no `.env`" case sits within noise of that floor.

1. **The remaining cost, when a `.env` *is* found, is real work - not overhead.** Loading a
   `.env` requires importing `python-dotenv` (~21 ms of the +~21 ms over the floor); that's
   the package doing its actual job, not something left on the table. **Caveat:** the `.env`
   fixture used here is a single line. This isolates the import-cost floor for that path, not
   necessarily the ceiling for a much larger, real-world `.env` (dozens of vars, `${VAR}`
   interpolation) - that's an open question this benchmark doesn't answer yet.

1. **The cost scales with venv size, so these numbers aren't fixed constants.** The discovery
   scan checks every installed distribution, not just autoread-dotenv's own dependencies - a
   lean production venv pays less than a kitchen-sink dev venv. This project's own
   ~95-package dev venv (used for the `importtime` breakdown above) shows proportionally
   larger absolute numbers for the same relative shape.

1. **Practical takeaway:** the "no `.env`" case - which covers `pip`/`uv`/utility scripts run
   from outside a project root, or any venv where autoread-dotenv is installed but unused -
   now costs essentially nothing beyond opting into `sitecustomize-entrypoints` itself. The
   "`.env` found and loaded" case still carries `python-dotenv`'s own import cost, which
   compounds for anything that spawns Python repeatedly (CI matrices, per-test subprocess
   isolation, cold-start-sensitive environments) - but that's now the honest floor for doing
   the job, not accidental overhead.

## Methodology

Two complementary tools, both wrapped in `justfile` recipes so they're reproducible rather
than one-off measurements:

- **[`hyperfine`](https://github.com/sharkdp/hyperfine)** (`just benchmark-startup`) for
  end-to-end wall-clock comparisons, with proper warmup runs and statistical variance - a
  single-shot `time python -c pass` is not trustworthy enough to publish. Builds throwaway
  venvs in a tempdir (no side-effects on this project's own `.venv`) for four scenarios:
  bare / `sitecustomize-entrypoints`-only / autoread-dotenv-without-`.env` /
  autoread-dotenv-with-`.env`.

  > `hyperfine` is a Rust CLI binary, install via your system package manager (`apt install hyperfine`, `brew install hyperfine`, `cargo install hyperfine`, ...). **Not** `pip install hyperfine` / `uv add hyperfine` - that installs an unrelated PyPI package (a
  > scientific curve-fitting library depending on `numpy`, `jax`, `scipy`, `pandas`,
  > `iminuit`) that happens to share the name.

- **`python -X importtime`** (stdlib, `just benchmark-importtime`) for *attributing* cost to
  specific imports, to see where the wall-clock difference actually goes rather than just
  how big it is.

Tracking approach: doc-only, re-run manually (e.g. before releases, or when touching
`entrypoint()`/`about.py`/dependencies). No CI job or third-party benchmarking service for
now - revisit if regressions start slipping through unnoticed.

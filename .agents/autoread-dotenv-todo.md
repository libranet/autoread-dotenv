# TODO: `autoread-dotenv` — Improvement List

Based on review of source (`__init__.py`, `utils.py`, `warnings.py`), `pyproject.toml`, and `docs/changes.md`.

______________________________________________________________________

## High priority (cheap, high signal)

- [x] **Narrow the broad `except OSError` in `get_dotenv_path()`**
  Done. `PermissionError` from `is_file()` keeps the assume-exists / defer-to-`load_dotenv()`
  behavior; any other `OSError` now warns naming the errno subtype before deferring, so a
  pathological path (`ENAMETOOLONG`, `ELOOP`, ...) isn't silently mis-reported as a
  permissions issue. Covered by `test_get_dotenv_path_other_oserror_on_stat_warns`.

- [x] **Confirm/fill in `SECURITY.md` content**
  Confirmed: `docs/security.md` is a real, maintained policy (supported versions, 90-day
  disclosure, 3-working-day ack), and GitHub picks it up from `docs/`. Added: a
  `security` entry in `[project.urls]` so it surfaces on PyPI, plus GitHub private
  vulnerability reporting as an explicit intake channel alongside the mailbox.

______________________________________________________________________

## Medium priority (robustness / testability)

- [x] **Add a return value or queryable status from `entrypoint()`**
  Done. `entrypoint()` returns a `LoadStatus` enum and records it in
  `autoread_dotenv.last_load_status` (`NOT_RUN` until it runs). New `autoread_dotenv.status`
  module; "warn, don't crash" philosophy unchanged. Covered per exit path in
  `tests/test_autoread.py` (incl. new `test_entrypoint_missing_dotenv_reports_status`).

- [x] **Document the threat model for `AUTOREAD_DOTENV_PATH` explicitly**
  Done. New "Threat model" section in `docs/security.md`: developer/operator-set config,
  used verbatim by design → path traversal / unexpected-file-load out of scope (setting it
  needs the same access as setting any env var on the process). States what *is* in scope
  (never crash the host interpreter; never leak `.env` contents into warnings).
  Cross-referenced from `utils.py`.

- [x] **Verify Trusted Publishing is applied consistently across all releases**
  Verified. OIDC Trusted Publishing landed 2026-08-16 (commit `3cad963`); no release
  workflow existed before. Releases 1.0–1.0.4 predate it (published manually with a token).
  1.0.5 and 1.0.6 use Trusted Publishing **and** carry valid PEP 740 attestations —
  confirmed via `https://pypi.org/integrity/autoread-dotenv/<ver>/<file>/provenance` (200
  for 1.0.5/1.0.6, 404 for 1.0.4). The legacy `/pypi/<project>/json` API just doesn't
  surface the `provenance` field; the integrity API does. Nothing to fix; consistent from
  1.0.5 on, not retroactively fixable for older versions.

______________________________________________________________________

## Lower priority (polish / rigor)

- [ ] **Add property-based tests (Hypothesis) for `str_to_bool()` and path-resolution functions**
  Both are small, pure, and cheap to fuzz. Low urgency given the low-risk input surface (developer-controlled, not external/untrusted input), but a natural next step past the existing 90% coverage floor.

- [ ] **Add mutation testing (mutmut) to CI**
  Confirms the test suite catches logic bugs, not just executes lines — a proportionate next step given the project already enforces coverage and has subprocess-boundary integration tests.

______________________________________________________________________

## Process (not code, but worth tracking)

- [ ] **Invite/encourage external review**
  No visible external contributors, issues, or PR discussion. Solo-maintained so far — no design decision (e.g. the breaking `about.py` change) has had outside pushback before shipping. Not a defect, but worth opening up if this project is meant to be adopted more broadly.

______________________________________________________________________

## Out of scope / not fixable

- **Small, single-purpose scope.** Nothing here demonstrates concurrency handling, a larger API surface, or performance at scale under load. Not an actionable item — just a reminder that a next-level demonstration of expertise would need a larger canvas, not a better version of this repo.

______________________________________________________________________

### Suggested order of attack

1. ~~Narrow `OSError` handling~~ ✅
1. ~~Fill in `SECURITY.md`~~ ✅
1. ~~Document `AUTOREAD_DOTENV_PATH` threat model~~ ✅
1. ~~Add `entrypoint()` status signal~~ ✅
1. ~~Verify Trusted Publishing consistency~~ ✅
1. Hypothesis tests
1. Mutmut in CI
1. Open the project up for outside review

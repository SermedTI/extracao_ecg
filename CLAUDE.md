# Repository Guidelines

## Project Structure & Module Organization

- `src/ecg_pdf_ingest/`: Python application code. Main modules are `cli.py`, `monitor.py`, `xml_receiver.py`, `database.py`, and `config.py`.
- `tests/`: unit tests for SMB/PDF intake, XML HTTP intake, duplicate handling, and coexistence in the shared index.
- `scripts/`: Windows PowerShell helpers for SMB share setup, scheduled task installation, and service startup wrappers.
- `config/`: runtime configuration templates and local settings such as `settings.example.json` and `settings.json`.
- Runtime data is stored outside the repo in `D:\ECG_PDF_*` directories; do not commit generated data, logs, or credentials.

## Build, Test, and Development Commands

- `py -3.13 -m venv .venv`: create the local virtual environment.
- `.\\.venv\\Scripts\\Activate.ps1`: activate the environment in PowerShell.
- `python -m pip install -e .`: install the package in editable mode.
- `python -m ecg_pdf_ingest bootstrap --config .\\config\\settings.json`: create runtime folders and initialize SQLite.
- `python -m ecg_pdf_ingest watch --config .\\config\\settings.json`: run the intake monitor locally.
- `python -m ecg_pdf_ingest serve-xml --config .\\config\\settings.json`: run the XML receiver locally.
- `python -m unittest discover -s tests -v`: run the test suite.

## Coding Style & Naming Conventions

- Use 4-space indentation in Python and standard PowerShell formatting in `.ps1` files.
- Prefer ASCII in source files unless an existing file already uses another charset.
- Keep modules small and single-purpose. Add short comments only where the behavior is not obvious.
- Python naming: `snake_case` for functions and variables, `PascalCase` for classes, descriptive filenames such as `monitor.py`.
- PowerShell scripts should use verb-noun function names like `Ensure-SmbShare`.

## Testing Guidelines

- Tests use Python `unittest`.
- Name test files `test_*.py` and test methods `test_*`.
- Cover file intake, duplicate detection, archive moves, HTTP receiver behavior, and error/quarantine paths when changing ingestion logic.
- Run tests before editing provisioning scripts and again after any behavior change.

## Commit & Pull Request Guidelines

- No Git history is available in this workspace, so use Conventional Commit style by default: `feat:`, `fix:`, `docs:`, `chore:`.
- Keep commits focused and reversible.
- PRs should include a short summary, config or security impact, test evidence, and screenshots only when UI is involved.

## Security & Configuration Tips

- Never commit real Windows passwords, domain credentials, or production hostnames.
- Treat `config/settings.json` as environment-specific.
- SMB1 is enabled only for TC10 compatibility; document that risk in any production handoff.
- The XML receiver defaults to internal HTTP without auth; document any TLS or authentication changes before rollout.

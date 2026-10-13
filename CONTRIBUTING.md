# Contributing to ai-infographic-studio

Thanks for wanting to help build the desktop AI infographic generator.
This repo targets Windows 10/11, Python 3.11+, and ships via PyInstaller.

## Repo layout

```
ai_infographic_studio/
  app/            entry point + Qt window bootstrap
  pipeline/       ingest -> process -> render job graph
  ingest/         source handlers (csv, json, markdown, xlsx, url)
  processors/     layout planners, palette, chart selectors, LLM adapters
  drivers/        output drivers (png, svg, pdf, pptx)
  models/         dataclasses + pydantic schemas for jobs and specs
  services/       model registry, render queue, telemetry (opt-in)
  utils/          logging, paths, image helpers, text metrics
  config/         default + user config loaders
tests/            pytest suites
docs/             architecture notes
```

## Dev setup

```powershell
py -3.11 -m venv .venv
.\.venv\Scripts\Activate.ps1
pip install -r requirements.txt
pip install -r requirements-dev.txt
python -m ai_infographic_studio.app.main
```

## Workflow

1. Fork, branch off `main` (`feat/`, `fix/`, `chore/` prefixes).
2. Add tests under `tests/` covering the new handler or processor.
3. Run `pytest -q` and `ruff check .` before opening a PR.
4. Keep PRs scoped — one handler, one processor, or one driver per PR.

## Adding an ingest handler

Subclass `ingest.base.IngestHandler`, register it in
`ingest.registry.HANDLER_REGISTRY`, and add a fixture under
`tests/fixtures/`. Handlers must be pure: bytes/text in, normalized
`Dataset` out.

## Adding an output driver

Subclass `drivers.base.OutputDriver`, implement `render(job, canvas)`,
and register in `drivers.registry.DRIVER_REGISTRY`. Drivers must not
mutate the canvas.

## Style

- Ruff + black, line length 100.
- Type hints on all public functions.
- No global mutable state outside registries.
- Logging via `utils.log.get_logger(__name__)`.

## Reporting bugs

Open an issue with: OS build, Python version, model backend (local /
OpenAI / Anthropic / Ollama), the input file (redacted if needed), and
the full trace from `%LOCALAPPDATA%\ai-infographic-studio\logs\`.
# Architecture — pipeline / worker layout

The generator is a job graph. Every request becomes a `RenderJob`
that flows through three stages:

```
ingest -> processors -> drivers
```

## Stages

**Ingest.** A source handler normalizes a file, URL, or inline blob
into a `Dataset` (columns, rows, inferred types, summary stats).
Handlers are registered in `ingest.registry.HANDLER_REGISTRY`.

**Processors.** A chain of processors turns `Dataset` + `InfographicSpec`
into a `Canvas` (abstract layout tree). Processors include:

- `layout_planner` — picks a layout template from the spec + data shape
- `chart_selector` — picks chart type per panel
- `palette` — derives a color scheme from brand or content
- `llm_caption` — optional LLM pass for headlines and captions

**Drivers.** A driver serializes the `Canvas` to a concrete format:
PNG, SVG, PDF, PPTX. Drivers are pure and registered in
`drivers.registry.DRIVER_REGISTRY`.

## Concurrency

Jobs run on a `RenderQueue` backed by a thread pool. The Qt UI never
blocks; progress events are pushed to the main thread via signals.

## Extending

Add a handler, processor, or driver — no core changes required.
See CONTRIBUTING.md.
# Security Policy

## Supported versions

| Version | Supported |
|---------|-----------|
| 0.6.x   | yes       |
| 0.5.x   | security only |
| < 0.5   | no        |

## Reporting a vulnerability

Email `security@ai-infographic-studio.dev` with:
- affected version and OS build,
- a minimal reproduction (input dataset + config + command),
- whether the issue is exploitable without user interaction.

We aim to acknowledge within 72 hours and ship a patch within 14 days
for high-severity issues.

## Threat model (desktop tool)

`ai-infographic-studio` is a local Windows desktop app. It:

- reads user-selected files and datasets,
- optionally calls remote LLM APIs using a user-supplied key,
- writes rendered outputs to a user-selected folder,
- loads fonts and templates from disk.

Out of scope: OS-level compromise, malicious fonts the user installed
themselves, and issues that require the user to run untrusted Python
inside the app's plugin folder.

In scope: path traversal in the ingest handlers, SSRF via the URL
ingest handler, template injection in the SVG/PDF drivers, and key
exfiltration from the config store.

## Hardening notes

- The URL ingest handler blocks private IP ranges and `file://`.
- SVG driver runs a tag/attribute allowlist before serializing.
- API keys are stored in Windows Credential Manager, not on disk.
- Telemetry is opt-in and off by default.
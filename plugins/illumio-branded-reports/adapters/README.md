# Platform Adapters for illumio-branded-reports

This directory contains notes on how to adapt this skill for non-Claude platforms.

## Portability Assessment

This skill is **moderately portable**. The core knowledge (branding tokens, document structure, component catalog) transfers to any platform. However, the PDF generation workflow depends on:

- WeasyPrint (Python library) — requires code execution capability
- File system access — reading/writing HTML and PDF files
- CSS Paged Media — platform-specific rendering engine

### Platform Suitability

| Platform | Feasibility | Notes |
|----------|------------|-------|
| Claude Code | Full support | Native format, all features work |
| Gemini + Code Interpreter | High | Can run Python, generate files |
| ChatGPT + Code Interpreter | High | Same — Python execution available |
| Codex (CLI) | High | Full terminal access |
| Local LLMs + shell | Medium | Needs Python/WeasyPrint installed locally |
| Perplexity | Low | No code execution |
| Pi / Hermes | Low | No code execution |

Create one file per platform as you adapt:
- `gemini.md` — Google Gemini / Antigravity
- `codex.md` — OpenAI Codex
- `local-llm.md` — Ollama, LM Studio, etc.

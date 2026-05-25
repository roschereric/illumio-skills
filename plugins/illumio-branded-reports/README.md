# illumio-branded-reports

An AI skill that generates professional, print-ready PDF and HTML documents using Illumio's visual identity. Give it a topic — a deployment guide, a technical brief, a runbook — and it produces a polished A4 document with branded cover pages, running headers, architecture diagrams, code blocks, callout boxes, and structured deployment phases.

Built for pre-sales engineers and technical teams who need to deliver customer-facing documentation that looks like it came from a design team, not a markdown renderer.

## What This Is For

When you're working with an AI assistant and you say something like "create a deployment guide for VEN installation via GPO" or "build me a branded technical brief on Illumio CloudSecure," this skill takes over. Instead of getting a plain markdown file or a generic PDF, you get a document that:

- Matches Illumio's brand identity (colors, typography, logo placement)
- Prints cleanly on A4 with proper page breaks, running headers, and no orphaned headings
- Includes architecture diagrams as inline SVGs (no external image dependencies)
- Has syntax-highlighted code blocks, numbered step sequences, and callout boxes
- Works as both a standalone HTML file and a PDF

The skill is designed around the Illumio brand but is **parameterizable** — you can swap the color tokens, logos, and cover gradient to adapt it for any brand. The structural CSS (running headers, page breaks, component layout) stays the same regardless of branding.

## Design Decisions

A few choices that shaped how this skill works and why:

**WeasyPrint over Chrome print.** The running header system uses CSS Paged Media (`position: running()`), which Chrome's print engine ignores entirely. WeasyPrint is the only Python-accessible renderer that supports this properly. This is a hard requirement, not a preference.

**Lightweight HTML template with external assets.** The CSS and structural HTML live in a single `template.html` (~18KB), while logo images are stored as separate PNGs in `assets/`. This keeps the template small enough that AI assistants don't burn context tokens on base64 blobs. The `assets/` directory must travel alongside the HTML for WeasyPrint to resolve the image paths.

**Sections as the unit of organization.** Each `<div class="section">` gets its own running header and page break. Phases, steps, and sub-content live *inside* sections, never as standalone sections. This keeps the running header meaningful (it always shows the parent section name, not a sub-phase).

**Inline SVG for diagrams.** Rather than generating images with external tools and embedding them, diagrams are hand-coded SVG or converted from Excalidraw. This keeps everything self-contained, scalable, and editable without leaving the HTML file.

**AI speech pattern avoidance.** The skill explicitly instructs the AI to avoid words like "leverages," "utilize," and "in order to." Customer-facing documents should read like a human wrote them.

## Repository Structure

```
illumio-branded-reports/
├── SKILL.md                              ← Main skill instructions (the AI reads this)
├── template.html                         ← HTML template with all CSS (~18KB, no base64)
├── assets/                               ← Logo images referenced by template.html
│   ├── logo-white.png                    ← White logo for cover page (dark backgrounds)
│   └── logo-dark.png                     ← Dark logo for section running headers
├── references/
│   ├── branding-tokens.md                ← Full color palette, typography, spacing
│   ├── css-print-architecture.md         ← Page margins, running headers, break rules
│   ├── component-catalog.md              ← Callouts, code blocks, tables, steps, SVGs
│   └── diagrams-guide.md                 ← Excalidraw workflow, hand-coded SVG, Mermaid
├── adapters/                             ← Platform-specific adaptation notes
│   └── README.md
├── .gitignore
└── README.md                             ← You are here
```

The skill loads in three stages, from cheapest to most expensive:

1. **Metadata** — The `name` and `description` in SKILL.md frontmatter. This is all the AI reads to decide whether to activate the skill.
2. **SKILL.md body** — The full instruction set: workflow, branding overview, document architecture, pitfalls.
3. **References** — Deep-dive files loaded only when needed (e.g., the component catalog is read only when the AI is assembling content).

## How to Use

### With Claude Cowork (Desktop App)

Cowork discovers skills from the `.claude/skills/` directory inside your mounted workspace folder.

**Option A — Symlink (recommended):**
Clone this repo into your skills workspace, then symlink it:

```bash
cd ~/Projects/Illumio\ Skills
git clone https://github.com/roschereric/illumio-branded-reports.git
mkdir -p .claude/skills
ln -sf ../../illumio-branded-reports .claude/skills/illumio-branded-reports
```

Then mount `Illumio Skills/` in Cowork. The skill appears automatically.

**Option B — Direct placement:**
Clone directly into the `.claude/skills/` directory of whatever folder you mount in Cowork.

Once installed, just ask naturally: *"Create a deployment guide for Illumio VEN installation via GPO"* — the skill triggers from the description and handles the rest.

### With Claude Code (CLI)

Claude Code reads skills from `.claude/skills/` in the project root or `~/.claude/skills/` globally.

**Per-project install:**
```bash
cd /path/to/your/project
mkdir -p .claude/skills
ln -sf /path/to/illumio-branded-reports .claude/skills/illumio-branded-reports
```

**Global install (available in all projects):**
```bash
ln -sf /path/to/illumio-branded-reports ~/.claude/skills/illumio-branded-reports
```

The skill format is identical for Cowork and Claude Code — no changes needed. The only difference is that Claude Code has full terminal access, so PDF generation via WeasyPrint runs directly in the CLI.

### With Other Platforms

This skill is portable to any AI platform that accepts system prompts or custom instructions. The core idea: **SKILL.md is a structured prompt, and the reference files are supporting context**. Adapting to another platform means reformatting that content for the target's prompt injection mechanism.

See the `adapters/` directory for platform-specific notes. The general approach:

1. Flatten SKILL.md + the relevant reference files into a single document
2. Remove Claude-specific references (tool names, file paths)
3. Add platform-specific framing ("You are an assistant that...")
4. Test with a few representative prompts

Platforms with code execution (Gemini, ChatGPT, Codex) can run the full WeasyPrint workflow. Platforms without code execution can still generate the HTML — the user just needs to convert to PDF locally.

For the full cross-platform guide, see `_guides/platform-adaptation.md` in the [Skills Lab](https://github.com/roschereric) workspace.

## Dependencies

The skill itself has no dependencies — it's just markdown files and an HTML template. PDF generation requires:

- **Python 3.8+**
- **WeasyPrint**: `pip install weasyprint`

WeasyPrint needs some system libraries (Cairo, Pango, GDK-PixBuf). On macOS: `brew install cairo pango gdk-pixbuf libffi`. On Ubuntu: `apt install libcairo2 libpango-1.0-0 libgdk-pixbuf2.0-0`.

## Adapting for Another Brand

The template is built around Illumio's identity but designed to be re-skinned:

1. Replace CSS custom properties in `:root` with the target brand's colors
2. Replace the logo files in `assets/` (`logo-white.png` and `logo-dark.png`) with the target brand's logos
3. Adjust the cover gradient in `.cover { background: linear-gradient(...) }`
4. Update geometric shapes (`.geo-1`, `.geo-2`, `.geo-3`) or remove them
5. Update the footer copyright text

The structural CSS — running headers, page breaks, component layout — stays unchanged. You're changing the paint, not the architecture.

## License

Private. For authorized use only.

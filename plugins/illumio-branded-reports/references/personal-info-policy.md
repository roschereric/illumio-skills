# Personal Information & Sensitive Data Policy

> **When to read this:** **MANDATORY — at the start of EVERY report generation
> run.** Before producing any text, scan the user's request against the
> categories in §1. If the report would include any of them and the values
> are not in the prompt, follow the protocol in §2 before generating
> anything.

This policy exists because reports produced by this skill are seen by
**partners, customers, and internal Illumio leadership**. Hallucinated names,
contact details, or sensitive identifiers cause real-world damage: they
embarrass the author, mislead the reader, and in the worst case fabricate
attributions or claims that look authoritative.

The rule is simple: **never invent personal or sensitive information. Ask
or omit. Default to placeholders.**

---

## §1 — Categories the skill MUST NOT hallucinate

If the report would naturally include any value in these categories and
the value is not explicit in the user's prompt or supplied references, you
MUST follow §2 before writing it.

### People
- First names, last names, full names of any individual (customer
  contacts, partner contacts, internal Illumio colleagues, executives,
  the document author themselves)
- Job titles when paired with a named individual
- Email addresses (corporate, personal, group aliases)
- Phone numbers
- Social media handles, LinkedIn URLs
- Pronouns when attached to a real person

### Organizations
- Customer company names when used in a confidential / pre-sales /
  POC context
- Partner organization names in deal-specific contexts
- Internal Illumio team names, squad names, or project codenames not
  publicly documented

### Network & technical specifics
- IP addresses, CIDR ranges, VLAN IDs
- Hostnames, FQDNs, server names
- Asset tags, workload labels, environment labels (if customer-specific)
- PCE tenant names, organization names inside Illumio Core
- Internal URLs (intranet, ticketing, knowledge base)

### Commercial & contractual
- Deal sizes, license counts, pricing
- Contract terms, renewal dates
- Discount levels, special terms
- Account executive names paired with deal context

### Document metadata
- Author name (if not the user)
- Reviewer names, approver names
- Distribution list members
- Internal classification labels (Confidential, Internal Only, etc.) if
  not specified

---

## §2 — Protocol (run this before generating any content)

When you encounter the start of a report-generation task, perform these
steps **in order**, before any HTML/PDF is produced:

### Step 2.1 — Inventory required information

Read the user's prompt and any attached materials. Build a mental list
of every value the report will need that falls into a §1 category.

### Step 2.2 — Classify each required value

For each item, classify as one of:

- **Provided** — value appears explicitly in the prompt or attached files
- **Derivable** — value can be inferred safely (e.g., today's date, the
  user's own name from session context, public information about Illumio
  products)
- **Missing — critical** — without this value, the report cannot be
  produced accurately (e.g., the partner the document is *about*)
- **Missing — substitutable** — the report can use a placeholder or
  omit the field with no loss of meaning (e.g., a recipient email when
  the document is generic)

### Step 2.3 — Surface what's missing, before writing

If any value is **Missing — critical** or **Missing — substitutable**, do
NOT start generating content. Instead, present the user with a single,
structured prompt:

```
Before I produce this report, I need to confirm a few things to avoid
guessing at personal or sensitive information.

CRITICAL — please provide:
  • <field>: …
  • <field>: …

OPTIONAL — I can use a placeholder or omit if you prefer:
  • <field>: provide / use placeholder / omit
  • <field>: provide / use placeholder / omit
```

Wait for the user's response. Do not proceed until you have either
explicit values, placeholders, or omit instructions for every
**Missing — critical** field. **Missing — substitutable** fields default
to the placeholder convention in §3 if the user does not respond.

### Step 2.4 — Document author attribution

If the report has an author byline:
- Default to **"Prepared by Eric Roscher — Illumio LATAM Pre-Sales
  Engineering"** unless the user specifies otherwise.
- NEVER invent co-authors, reviewers, approvers, or distribution lists.
- If "Reviewed by" / "Approved by" is requested, ask for the names —
  do not guess them based on org charts or common patterns.

### Step 2.5 — Hard stops

Even if the user is pushing for fast output, refuse to generate any of
the following without an explicit value from them:

- A specific named individual at a customer or partner organization
- An email address for any named person
- A phone number for any named person
- A direct quote attributed to a real person
- A specific deal value or license count

These are the items most likely to embarrass or mislead. There is no
"reasonable default" — only a value the user supplied or a refusal.

---

## §3 — Placeholder convention

When a value is missing-substitutable or the user explicitly chooses
"use placeholder," use these forms. They are scannable for find-and-
replace later and unambiguous to a human reader:

| Category | Placeholder |
|---|---|
| Customer org name | `<CUSTOMER>` |
| Partner org name | `<PARTNER>` |
| Customer contact name | `<CUSTOMER_CONTACT>` |
| Partner contact name | `<PARTNER_CONTACT>` |
| Internal colleague name | `<INTERNAL_NAME>` |
| Email address | `<EMAIL>` or `name@<CUSTOMER>.com` if context demands a domain |
| Phone number | `<PHONE>` |
| IP address | `10.0.0.0/24` or `<IP_PLACEHOLDER>` |
| Hostname | `<HOST>` or `host01.<CUSTOMER>.internal` |
| PCE tenant | `<TENANT>` |
| Deal size / license count | `<LICENSE_COUNT>` |
| Date (if not today) | `<DATE>` |

Wrap placeholders in angle brackets and SCREAMING_SNAKE_CASE so they're
obviously placeholders, not real values. A reader skimming the rendered
PDF should instantly spot them.

---

## §4 — Examples

### Example A — User asks for a deployment guide, no contact details

> *"Build a deployment guide for the Containment Switch POC at the
> customer."*

Inventory: customer name (missing — placeholder OK if generic), POC
contact names (missing — substitutable), reviewer (missing —
substitutable).

Action: produce the report with `<CUSTOMER>`, `<CUSTOMER_CONTACT>`, and
no reviewer byline. Tell the user at the top of the response:
"I've used placeholders for the customer name and contact. Replace
`<CUSTOMER>` and `<CUSTOMER_CONTACT>` before sharing."

### Example B — User asks for a partner-specific document with a recipient

> *"Build a partner-enablement brief for [Partner Co]. Recipient is the
> partner's solutions architect, give it a personal tone."*

Inventory: partner name (provided), partner contact name (missing —
**critical**, because the brief is addressed to them), partner contact
email (missing — critical if the document includes a "Reply to:" header).

Action: STOP. Ask before writing.
"Before I build this brief, I need: (1) the name of the solutions
architect at [Partner Co], (2) whether the brief should include their
email or a placeholder. I won't guess these."

### Example C — User asks for an internal report to be sent to SVP

> *"Generate a status report on the Banco Acme POC for SVP review."*

Inventory: SVP name (missing — substitutable if the doc says "for
executive review"; critical if it names them in salutation), Banco
Acme contact roster (missing — depends on report content).

Action: ask. "Two questions before I write: (1) Should the report be
addressed to a specific SVP by name, or generically 'for executive
review'? (2) Should I include the Banco Acme contact roster, or skip
that section?"

---

## §5 — One-liner the SKILL.md workflow should reference

> *"Step 0 of every run: read `references/personal-info-policy.md` and
> apply the §2 protocol. Do not generate any content until missing-
> critical fields are resolved."*

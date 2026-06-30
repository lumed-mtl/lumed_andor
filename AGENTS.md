# Caveman

Applies when user asks for caveman mode, brief mode, or token-efficient replies.

Respond terse like smart caveman. All technical substance stay. Only fluff die.

Default: **full**. Switch: `/caveman lite|full|ultra`.

## Rules

Drop: articles (a/an/the), filler (just/really/basically/actually/simply), pleasantries (sure/certainly/of course/happy to), hedging. Fragments OK. Short synonyms (big not extensive, fix not "implement a solution for"). Technical terms exact. Code blocks unchanged. Errors quoted exact.

Pattern: `[thing] [action] [reason]. [next step].`

Not: "Sure! I'd be happy to help you with that. The issue you're experiencing is likely caused by..."
Yes: "Bug in auth middleware. Token expiry check use `<` not `<=`. Fix:"

## Intensity

| Level     | What change                                                                                                                   |
| --------- | ----------------------------------------------------------------------------------------------------------------------------- |
| **lite**  | No filler/hedging. Keep articles + full sentences. Professional but tight                                                     |
| **full**  | Drop articles, fragments OK, short synonyms. Classic caveman                                                                  |
| **ultra** | Abbreviate (DB/auth/config/req/res/fn/impl), strip conjunctions, arrows for causality (X -> Y), one word when one word enough |

Example - "Why React component re-render?"

- lite: "Your component re-renders because you create a new object reference each render. Wrap it in `useMemo`."
- full: "New object ref each render. Inline object prop = new ref = re-render. Wrap in `useMemo`."
- ultra: "Inline obj prop -> new ref -> re-render. `useMemo`."

Example - "Explain database connection pooling."

- lite: "Connection pooling reuses open connections instead of creating new ones per request. Avoids repeated handshake overhead."
- full: "Pool reuse open DB connections. No new connection per request. Skip handshake overhead."
- ultra: "Pool = reuse DB conn. Skip handshake -> fast under load."

## Auto-Clarity

Drop caveman for: security warnings, irreversible action confirmations, multi-step sequences where fragment order risks misread, user confused. Resume caveman after clear part done.

Example - destructive op:

> **Warning:** This will permanently delete all rows in the `users` table and cannot be undone.
>
> ```sql
> DROP TABLE users;
> ```
>
> Caveman resume. Verify backup exist first.

## Boundaries

Code/commits/PRs: write normal. "stop caveman" or "normal mode": revert. Level persist until changed or session end.

# LLM Zettelkasten

A personal knowledge base maintained by LLM. Inspired by Andrej Karpathy's LLM Wiki pattern, adapted for a modern zettelkasten workflow.

## Folder structure

```
sources/                           -- source `.md` files only; lives alongside `Zettelkasten/`
Zettelkasten/                      -- root note system maintained by LLM
Zettelkasten/Fleeting Notes/       -- temporary working notes maintained by user; LLM Zettelkasten may assist here only when user explicitly asks, never by default and never as part of ingest or audit workflows
Zettelkasten/Literature Notes/     -- source-based summary notes derived from `sources/`
Zettelkasten/Permanent Notes/      -- concept and idea notes synthesized from literature notes
Zettelkasten/index.md              -- table of contents for all notes
Zettelkasten/log.md                -- append-only record of LLM Zettelkasten operations only
```

## Ingest workflow

When the user adds a new source to `sources/` (as a single `.md` file, e.g. from Mathpix) and asks you to ingest it:

1. Read the full source document
2. Before writing anything, present a framing check to the user that includes:
    - proposed reference type
    - proposed core thesis
    - 5-15 key concepts
    - any ambiguity, quality issue, or scope concern
3. Ask user whether framing is right and what to emphasize, ignore, or treat cautiously
4. Create a literature note in `Zettelkasten/Literature Notes/` named after the source using the exact literature note structure defined below
5. Suggest permanent notes to the user based on the literature note, grouping them into:
    - foundational notes
    - relational notes
    - synthesis notes
6. Present note suggestions as a dependency-aware graph or ordered list, not a flat list
7. Ask the user which foundational notes should be created or updated automatically during ingest, and which relational or synthesis notes should be deferred for guided work with the user
8. Automatically create or update only the approved foundational notes in `Zettelkasten/Permanent Notes/`; do not automatically create relational, comparison, or higher-level synthesis notes during ingest
9. If relational or synthesis notes seem valuable, suggest them explicitly as follow-up work to be done with user guidance after foundational notes exist
10. Add wiki-links ([[note-name]]) to connect related notes
11. Update `Zettelkasten/index.md` with new notes and one-line descriptions
12. Append an entry to `Zettelkasten/log.md` with the date in `YYYY-MM-DD` format, source name, and what changed

Ingest workflow should not create or modify notes in `Zettelkasten/Fleeting Notes/`.

A single source may touch 10-15 notes. That is normal.

## Note formats

### Literature Notes

Literature notes are structured extraction records for a single source, not freeform summaries. They should make source claims, concepts, methods, evidence, and note candidates easy to compare across repeated ingests and across different fields.

Every literature note should follow this structure exactly:

```markdown
#llm_gen

# Note Title

**Summary**: One to two sentences describing the ingested source.

**Source**: [[wiki-link]] to single ingested `.md` file from the `sources/` directory that this note summarizes.

**Reference type**: empirical study | review | textbook | lecture notes | essay | technical report | reference entry | unknown

**Domain**: Short field or topic label.

**Last updated**: Date of most recent update in `YYYY-MM-DD` format.

## 1. Source Snapshot

- Authors or attribution: ...
- Venue / publisher: ...
- Year: ...
- Reference type: ...
- Central topic: ...
- Source quality notes: ...

Use `Not stated` for missing metadata.

## 2. Core Thesis

- 1 to 3 bullets only.
- Each bullet should state one central claim from the source.
- Each bullet must end with `(source: filename.md)`.

## 3. Key Concepts

- One bullet per concept.
- Format: `Concept — one-sentence definition, distinction, or role in this source. (source: filename.md)`
- Include aliases or alternate names when useful.

## 4. Claims and Arguments

- Use a numbered list.
- Each item should contain:
    - claim
    - support, evidence, or reasoning given by the source
    - qualifier if the source limits the claim
    - citation `(source: filename.md)`

## 5. Methods / Mechanisms / Formalism

- Capture procedures, mechanisms, models, derivations, algorithms, or formal structure when present.
- If absent, write `Not applicable for this source type`.

## 6. Evidence / Examples

- Capture experiments, data, examples, case studies, worked examples, or historical evidence when present.
- If absent, write `No explicit evidence or examples stated`.

## 7. Definitions and Quantities

- Capture symbols, variables, parameters, metrics, units, and equations when present.
- Preserve notation from the source when possible.
- If absent, write `No special quantities or formal definitions stated`.

## 8. Limits, Assumptions, and Open Questions

- Capture stated assumptions, scope limits, ambiguities, contradictions, and open questions.
- If absent, write `Not explicitly discussed`.

## Related notes

- [[related-permanent-note-1]]
- [[related-permanent-note-2]]
```

Literature note extraction rules:

- Use headings in exact order shown above.
- Prefer short bullets over long paragraphs.
- Each bullet should capture one extractable unit whenever possible.
- Separate source claims from agent inference.
- Agent inference belongs in planning and note-candidate sections, not in extraction sections.
- If a bullet contains multiple concepts, comparisons, or causal steps, split it unless source clearly treats them as one unit.
- Do not skip sections. Use explicit placeholder text when information is absent.
- Every factual bullet or numbered item must include a citation in the form `(source: filename.md)`.
- Keep field-specific terminology from the source, but add a short plain-language gloss when needed.
- If the same concept appears under multiple names, note aliases in `Key Concepts`.

Literature note adaptation by source type:

- Empirical study: emphasize methods, evidence, limitations.
- Review: emphasize taxonomy, major claims, disagreements.
- Textbook or lecture notes: emphasize concepts, definitions, formalism.
- Essay or philosophy text: emphasize arguments, assumptions, distinctions.
- Technical report: emphasize procedures, architecture, constraints.

All literature notes still use the same top-level structure regardless of source type.

### Permanent Notes

Every permanent note should follow this structure:

```markdown
#llm_gen

# Note Title

Main content goes here. Focus on a single concept, claim, distinction, or idea.

Make the note self-contained and understandable without reopening the original sources.

Do not mention "the source", "this source", "the paper", "the text", "the author", or any other source-context framing in the main body. Write the note as standalone knowledge that holds without source narration.

Use clear headings and short paragraphs.

Link to related concepts using [[wiki-links]] throughout the text.

## Sources

- [[source-file-1.md]]
- [[source-file-2.md]]

## Related notes

- [[related-literature-note-1]]
- [[related-permanent-note-1]]
- [[related-permanent-note-2]]
```

## Permanent note granularity and dependency rules

Permanent notes must be atomic by default.

- Prefer one note per core concept, method, quantity, distinction, or claim.
- Prefer concept notes before relationship notes.
- If a proposed note title contains multiple specialized concepts, first check whether those concepts already have notes.
- If they do not, suggest or create the missing prerequisite notes first, unless the user explicitly wants a higher-level synthesis note.

Creation order during ingest:

1. Core concept notes
2. Method notes
3. Parameter / quantity notes

Relationship, comparison, and higher-level synthesis notes should not be automatically created during ingest. Suggest them only as follow-up work with user guidance after foundational notes exist.

Examples:

- Prefer [[Photosynthesis]], [[Chlorophyll]], and [[Light-Dependent Reactions]] before [[Chlorophyll Enables Light-Dependent Reactions in Photosynthesis]].
- Prefer [[Supply and Demand]] and [[Price Elasticity]] before [[Price Elasticity Changes Supply and Demand Responses]].

Title heuristics:

- Concept note titles should usually be noun phrases, not full claims.
- Claim note titles are allowed only when:
    - prerequisite concept notes already exist, or
    - those prerequisite notes are being created in the same approved batch.
- Avoid titles that compress an entire paragraph into one note.
- When in doubt, split one broad note into 2-5 smaller notes.

Linking rules:

- Every permanent note should link to broader, narrower, or sibling concepts when they exist.
- If a note depends on a concept that does not yet exist as a permanent note, flag it as a missing-note candidate during planning.

During ingest suggestion phase:

- Suggest permanent notes as a small note graph, not as an isolated list.
- Mark each suggestion as one of:
    - foundational
    - relational
    - synthesis
- Prefer approving foundational notes first.
- Only foundational notes are eligible for automatic creation during ingest.
- Relational and synthesis notes require explicit user-guided follow-up and should be deferred by default.

Before creating a permanent note, ask: "Can this note be understood as one idea, do its main terms already exist as notes, and does the body avoid any source-context phrasing?" If not, split, rewrite, or defer it.

## Citation rules

- Every factual claim should reference its source Markdown source file
- Use the format (source: filename.md) after the claim
- `Source` and `Sources` always refer to canonical `.md` files in the `sources/` directory
- Cite only `.md` files from the `sources/` directory
- Do not cite `.pdf` files or any file outside `sources/`
- If two source `.md` files disagree, note the contradiction explicitly
- If a claim has no source `.md` file, mark it as needing verification

## Question answering

When the user asks a question:

1. Read `Zettelkasten/index.md` first to find relevant notes
2. Read those notes and synthesize an answer
3. Cite specific notes in your response
4. If the answer is not in the zettelkasten, say so clearly
5. If the answer is valuable, offer to save it as a new note

Good answers should be filed back into the zettelkasten so they compound over time.

## Lint

When the user asks you to lint or audit the zettelkasten:

- Check for contradictions between notes
- Find orphan notes (no inbound links from other notes)
- Identify concepts mentioned in notes that lack their own permanent note
- Flag claims that may be outdated based on newer sources
- Check that all notes follow the note formats above
- Report findings as a numbered list with suggested fixes

## Rules

- Never modify anything in the `sources/` folder
- Always update `Zettelkasten/index.md` and `Zettelkasten/log.md` after changes
- Keep note names Capitalized With Spaces (e.g. `Machine Learning.md`)
- Write in clear, plain language
- All equations in zettelkasten notes must use $...$ for inline math and $$...$$ for block math (Obsidian compatible). Never use \(, \), \[, or \].
- Zettelkasten files must be written as obsidian style Markdown. Never wrap the entire file in triple backticks or any code block markers.
- Every note generated by the LLM Zettelkasten agent must include the Obsidian tag `#llm_gen` at the top of the file.
- Permanent note bodies must never explicitly mention source context such as "the source", "this source", "the paper", "the text", or "the author"; source attribution belongs only in the `## Sources` section.
- LLM Zettelkasten agent must use caveman mode for all user interaction (prompts, responses), but not when editing or writing notes.
- LLM Zettelkasten agent must ignore `.pdf` files and any non-`.md` files during ingest; only process `.md` source files in the `sources/` directory.
- LLM Zettelkasten agent must use only those `.md` files in `sources/` as canonical sources for literature notes, permanent notes, and citations.
- For zettelkasten note dates and log dates, use the current date already available in the agent/session context.
- Do not call tools, shell commands, or ask permission only to get the date.
- If a date tool must be used because the user directly asks for today’s date, use local time, not UTC.
- Write dates as `YYYY-MM-DD`.
- Default to smaller permanent notes over broader ones
- During ingest, automatically create only simple foundational permanent notes: core concept notes, method notes, and parameter / quantity notes
- Do not automatically create relationship, comparison, or synthesis notes during ingest
- Do not propose a synthesis or comparison note when its key component concepts do not yet exist as permanent notes, unless you also propose those prerequisite notes in the same plan
- During ingest, present note suggestions as a dependency-aware graph or ordered list, not a flat list
- If a source introduces many new terms, prefer creating foundational glossary-like permanent notes first
- When uncertain about how to categorize something, ask the user
- During ingest, never skip framing check before literature note creation
- During ingest, literature notes must separate extraction from interpretation
- In literature note extraction sections, use atomic bullets that can be directly compared across sources
- In literature note extraction sections, write `Not stated`, `Not applicable for this source type`,

# Git Commits and Branches

When user asks for git commit message, branch name, or both, always follow these conventions.

## Commit Messages

Use [Conventional Commits 1.0.0](https://www.conventionalcommits.org/en/v1.0.0/).

Rules:

- Format: `<type>[optional scope][!]: <description>`
- Use lowercase `type` and concise imperative description.
- Common types: `feat`, `fix`, `docs`, `style`, `refactor`, `perf`, `test`, `build`, `ci`, `chore`, `revert`.
- Add scope when it helps, like `feat(auth): add session refresh`.
- Mark breaking changes with `!` in header and/or `BREAKING CHANGE:` in footer.
- Keep subject short, specific, and without trailing period.
- If body is needed, explain what changed and why.
- If footer is needed, use standard trailers like `BREAKING CHANGE:` or issue refs.

## Branch Names

Use [Conventional Branch](https://conventional-branch.github.io/) conventions.

Rules:

- Format: `<type>/<description>`
- Optional scoped format allowed: `<type>/<scope>/<description>`
- Use lowercase words separated by hyphens.
- Keep names short, descriptive, and tied to actual work.
- Prefer branch `type` values that match commit intent, like `feat`, `fix`, `chore`, `docs`, `refactor`, `test`.
- Examples: `feat/auth-session-refresh`, `fix/login-race-condition`, `docs/api-auth-guide`.

## Changelog Updates

- Before creating a commit, check whether the staged changes are changelog-worthy. If they affect user-visible behavior, public API, package structure, supported workflows, dependencies, tooling expectations, documentation, or release-facing project layout, update `CHANGELOG.md` first.
- Record new work only under `## [Unreleased]`. Do not rewrite historical release entries unless correcting an actual historical mistake.
- Use Keep a Changelog style headings such as `Added`, `Changed`, `Fixed`, `Removed`, `Deprecated`, or `Security`, and add concise bullets that match the staged changes.
- Small purely local cleanup that does not matter to users or future maintainers, such as temporary files, ignored-file cleanup, or trivial typo fixes, does not require a changelog entry.
- When preparing a commit, treat the changelog update as part of the same change set whenever the change is notable enough to appear in project history.

## Behavior

- Never invent non-standard commit or branch formats when user asks for git naming help.
- If user gives summary of changes, return commit and branch names that match these conventions.
- If user asks to commit, or asks for a commit message without describing the changes, inspect the current staging area first and infer what the commit is about from the staged diff instead of asking the user to summarize it.
- Base commit message suggestions on staged changes only, not unstaged or untracked changes.
- If nothing is staged, say that clearly and ask the user whether they want help staging files before committing.
- Draft a commit message that follows Conventional Commits, show it to the user, and ask for clarifications, feedback, or approval before creating the commit.
- After the user confirms or refines the draft, proceed with the commit using the approved message.
- If change spans multiple concerns, prefer most meaningful user-facing type, or ask for clarification when needed.
- For commit messages and branch names, write normal style, not caveman style.

# Markdown

## Character Normalization

When creating or editing `.md` files, use ASCII punctuation by default. Normalize typographic variants to plain Markdown-friendly characters unless user explicitly asks for literal originals.

Replacements:

- `["“”„‟«»″‶]` -> `"`
- `[‘’‚‛᾽ʹˈ̀́′]` -> `'`
- `[—–‒―−]` -> `-`
- `[…]` -> `...`

Apply to headings, prose, lists, tables, and other normal Markdown text. Do not change code fences, inline code, regex examples, or other content where exact literal characters are intentionally shown.

## Documentation Voice and Style

Project documentation markdown should use neutral descriptive prose in the same general style as this document.

- Prefer declarative sentences over direct address.
- Avoid second-person wording such as `you`, `your`, or agent-style prompts.
- Describe what a directory, file, or workflow is for rather than telling the reader what to do conversationally.
- Keep project documentation consistent in tense and sentence structure with documents such as `repository-structure.md`.

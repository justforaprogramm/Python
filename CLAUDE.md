# Rules for Claude (mandatory, no exceptions)

## 1. Git workflow
- NEVER commit, push or merge to `main`. No force-push, no history rewriting.
- Work only on a dedicated branch: `claude/<short-description>`.
- When done, open a Pull Request against `main` with: what changed, why, how it was tested.
- NEVER merge the PR yourself. The owner reviews and merges.
- Small, focused commits with clear messages (Conventional Commits: `feat:`, `fix:`, `docs:`, ...).

## 2. Scope: do exactly what was asked
- Implement only what is explicitly specified. No extra features, refactors, renames, dependency changes or "improvements".
- If something is unspecified or ambiguous: STOP and ask before writing code. Never guess.
- If you notice other problems, mention them in the PR description, do not fix them.

## 3. Secrets and confidential data
- NEVER use, request, invent or commit real keys, tokens, passwords, certificates or private hostnames.
- Always use a placeholder in exactly this format:
  `<#Todo: description of the confidential value>`
  Example: `API_KEY = "<#Todo: API key for the weather service>"`
- Real values belong in environment variables / `.env` (git-ignored). Provide a `.env.example` containing only placeholders.
- If a task seems to require a real secret: use a placeholder and say so in the PR.

## 4. Language
- All code, comments, commit messages, PR texts and READMEs are in English.

## 5. Code quality
- Follow the existing style, structure and naming of the repo.
- Handle errors explicitly, validate inputs, no silent failures.
- Add or update tests when the repo has tests. Run them before opening the PR.
- Do not add new dependencies without asking.

## 6. README (update on EVERY change)
Create `README.md` if missing; otherwise update it in the same PR as the code change.
It must follow this structure:

```
# <Repo title>

## Overview
What the code does (2-4 sentences) plus an architecture diagram
(Mermaid or ASCII) showing components and data flow.

## Quickstart
- Start command
- Debug command
- Special start commands (flags, profiles, docker compose variants, ...)
- Required environment variables (names only, no values)

## Architecture
- Components and responsibilities.
- Networking rule: no hard-coded IP addresses anywhere, except Docker-internal
  service names/addresses. Everything else comes from config or env variables.

## <Further sections as relevant to the code>
e.g. Configuration, Testing, Deployment, Troubleshooting, Project structure.
Derive them from the actual code, only add what is true and useful.
```
- The README must always match the current code. Never document features that do not exist.

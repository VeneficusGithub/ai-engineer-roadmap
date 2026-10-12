# AI Engineer Roadmap

A self-study website for data science trainees preparing for a Junior AI Engineer role and its interview. It lists what to learn per topic, links to courses and exercises, and has interview questions with click-to-reveal answers. Trainees tick items off as they go; progress is saved in their own browser.

## Editing the content

All content is plain Markdown in [`docs/`](docs/), written in Dutch (technical terms and course titles stay in English):

- [`docs/index.md`](docs/index.md): home page with the roadmap and the "why this site exists" text
- [`docs/stages/`](docs/stages/): one file per stage

### Add a resource or exercise

Add a list item with a link followed by `{ ... }`:

```markdown
- [Title of the resource](https://example.com){ .rm-item data-source="Cursus · DataCamp" data-time="45 min" } Eén zin over waarom het de moeite waard is.
```

- Add `.rm-exercise` to label it as an exercise.
- Add `.rm-refresh` to include it in the half-day refresh route.
- Put it under `## Verdieping { .rm-full-only }` for optional extra depth.

### Add a question

```markdown
??? interview "De vraag?"
    Het antwoord, vier spaties ingesprongen.
```

Use `selfcheck` instead of `interview` for a check-your-understanding question, and add `rm-refresh` (`??? interview rm-refresh "..."`) to include it in the refresh route.

**Note:** progress is stored per link URL and per question text. Changing a link or rewording a question resets that item for trainees who already ticked it.

## Preview locally

Requires [uv](https://docs.astral.sh/uv/).

```sh
uv sync
uv run zensical serve     # open http://localhost:8000
```

## Development

```sh
uv run playwright install chromium   # once, for the browser tests
uv run pytest                        # build the site and run browser tests
uv run ruff check .                  # lint
uv run ruff format .                 # format
uv run mypy                          # type check
```

Pushing to `main` publishes the site to GitHub Pages via [`.github/workflows/deploy.yml`](.github/workflows/deploy.yml).

## Suggestions

Trainees can suggest resources or questions by opening an issue in this repository.

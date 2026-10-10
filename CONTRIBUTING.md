# Contributing

[中文](CONTRIBUTING.zh-CN.md)

All Lody-related configurations, practices, guides, and videos are welcome. Follow the structure and provide usage instructions. Maintainers judge relevance in PR review; test reports, performance evidence, and translations are not required.

## Choose a location

To recommend an ecosystem project, add a row to the Ecosystem table in both homepages with its name, repository link, type, and a short description.

Use `<scenario>/<type>/<entry>`. See the [homepage](README.md) for scenarios.

| Type | Submission |
| --- | --- |
| `roles/` | Directory: README.md, role.yaml, prompt.md |
| `schedules/` | Directory: README.md, schedule.yaml, prompt.md |
| `prompts/` | Directory: README.md, prompt.yaml, prompt.md |
| `skills/` | Complete Skill directory with README.md, or external-link Markdown |
| `guides/` | One Markdown file with original guidance or an article recommendation |
| `videos/` | One Markdown file introducing and linking a video |
| `recipes/` | Directory with shared instructions and multiple resources |

Choose one primary scenario and use tags for other uses. Names use lowercase English, digits, and hyphens. Do not duplicate resources across scenarios or create empty categories.

## Copy a template

Copy files directly, either locally or using GitHub’s web editor. No development environment or dependency installation is needed.

```sh
mkdir -p code-review/roles
cp -R templates/en/roles/example code-review/roles/my-reviewer
```

Choose other types from the [template catalog](templates/README.md). Replace the sample author, title, language, tags, and text. Remove irrelevant template instructions. Do not present template examples as verified community practices.

Configuration and Skill instructions describe purpose, relevance to Lody, prerequisites, and usage. Agent/model/reasoning recommendations and their rationale are encouraged, not required. External articles/videos need a short introduction, relevance, and source. Both require [metadata](docs/format.md).

Store prompt bodies in separate Markdown files referenced by promptFile. Version 1 Shortcuts are plain text; explain how users select any required Roles, Skills, or files. Users supply machine, project, Agent, and time zone settings. Do not submit your internal IDs, absolute paths, or credentials.

## Languages and navigation

Bilingual submissions are not mandatory. languages describes the content, for example `[en]` or `[zh-CN, en]`. Directory entries use README.md, with optional README.en.md or README.zh-CN.md translations linked to each other. Full Skills preserve their SKILL.md format; put repository metadata in README.md.

Add a type subheading and entry link under the relevant scenario in both homepages, including title, short description, and language. Remove that scenario’s “No submissions yet” note. The submission’s original title is acceptable; translating the content is not required.

## Checks and PRs

Before submitting, review the directory location, metadata, configuration fields, and referenced file paths against the [format guide](docs/format.md). Check that links point to the intended content. Maintainers review structure, instructions, relevance, and attribution in the PR; running submissions is not required.

Explain relevance to Lody in your PR. Prefer one entry or related recipe per PR; improvements to existing entries are welcome. Inclusion does not imply maintainer verification of results.

## Attribution and licensing

The repository uses [MIT](LICENSE); original contributions are submitted under MIT. For others’ articles, videos, or Skills, set authors to the original authors and source to the original URL. Git history records contributors. Copy third-party files only under their permissions, declare license, and retain required notices. Listing a link does not change external content’s license. Do not copy full content or files without the necessary permission.

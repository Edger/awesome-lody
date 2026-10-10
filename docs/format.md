# Sharing format v1

[中文](format.zh-CN.md)

This is the awesome-lody file format. Configure resources using their instructions. Paths identify entries; v1 needs no separate entry version or manifest.

## Entry layout

Use `<scenario>/<type>/<entry>`; see [scenarios](../README.md) and [types](../CONTRIBUTING.md). Slugs use lowercase English, digits, and hyphens.

Articles and videos use `<slug>.md`. Configurations, complete Skills, and recipes use `<slug>/README.md` plus resources. External Skills use `<slug>.md`. Directory entries may include README.en.md or README.zh-CN.md translations; these are not separate entries. Use UTF-8 text and no symlinks.

## Markdown entry metadata

```yaml
---
title: My project reviewer
description: Review project changes using Lody.
authors:
  - name: your-name
    url: https://github.com/your-name
languages: [en]
tags: [code-review]
---
```

| Field | Requirement |
| --- | --- |
| title, description | Required non-empty text |
| authors | Required non-empty list; name required, HTTP(S) url optional |
| languages | Required unique, non-empty BCP 47 tags, such as en or zh-CN |
| tags | Optional unique text list |
| source | Original HTTP(S) URL, required for external recommendations |
| license | Optional; declare third-party terms and retain required notices when copying |
| resources | Recipes only; relative paths to configurations or Skills |

External recommendations, including videos, articles, and Skills, require source. Credit original authors; Git history records contributors. Scenario and type come from the path. Do not use unknown fields or duplicate YAML keys.

Include Markdown instructions after frontmatter. People review their quality. Complete Skills preserve SKILL.md’s original format (name, description, and body); repository metadata goes in the companion README.md.

## Shared configuration fields

Only role.yaml, schedule.yaml, and prompt.yaml use this format. Single-resource entries use these fixed names. Recipe configurations may use descriptive filenames such as reviewer.yaml. Each YAML describes one resource.

| Field | Requirement |
| --- | --- |
| schemaVersion | Required integer 1 |
| kind | Required role / schedule / prompt |
| name | Required resource name |
| description | Optional purpose |
| promptFile | Required Markdown path relative to this YAML |

Prompt files contain non-empty prompt text with no frontmatter. Role name/description limits: 60/140 characters. Prompt name/description limits: 60/240, body at most 256 KiB. Schedule name/description limits: 200/1000, body at most 32 KiB.

All resolved paths stay within the repository. Use ../ to reuse resources when needed, but not absolute paths, URLs, backslashes, or symlinks. Update references when moving files. Do not include private IDs, runtime state, or credentials.

## Role

```yaml
schemaVersion: 1
kind: role
name: Project reviewer
promptFile: prompt.md
recommended:
  agent: codex
  runConfig:
    configOptionValues:
      reasoning_effort: high
```

recommended is optional and encouraged. When present, agent is required and uses a readable Agent identifier. runConfig may contain modelId, modeId, and configOptionValues; option values are strings or booleans. Use keys/values the actual Agent supports, include your model ID if useful, and explain the choice. Users may replace settings and should choose options supported by their Agent.

The prompt maps to promptPrefix. Users choose their machine and Agent configuration. v1 does not store memory bindings. Explain any recommended permission settings; users make the actual selection.

## Schedule

```yaml
schemaVersion: 1
kind: schedule
name: Weekday check
promptFile: prompt.md
trigger:
  kind: cron
  expression: "0 9 * * 1-5"
```

Required trigger supports:

- cron: five-field expression; optional timeZone recommends an IANA zone such as Asia/Shanghai. Users choose a zone when omitted.
- interval: integer everyMs of at least 60000. Users choose the anchor time during setup.

Use five-field cron expressions without randomized H values. Do not infer the user’s time zone or include one-off dates and runtime state.

Optional roleFile references Role YAML. Alternatively provide recommended using the Role shape; the two are mutually exclusive. roleFile expresses the intention to use the Role’s recommendations and instructions. Document the setup steps in the usage instructions.

## Prompt Shortcut

```yaml
schemaVersion: 1
kind: prompt
name: Review current changes
slug: review-changes
promptFile: prompt.md
```

Required slug: 1–40 lowercase letters, digits, or hyphens, starting with a letter or digit. Bodies are plain text: no variable substitution or ID-bearing mention objects. Markdown, ordinary @text, and other symbols remain literal content; do not describe them as automatically bound references.

## Recipe

Use README.md as the entry. When resources are included, list configurations and Skills in resources:

```yaml
resources:
  - roles/reviewer.yaml
  - schedules/daily-check.yaml
  - skills/project-summary
```

Store configurations under roles/, schedules/, prompts/, or similar internal directories; store Skills under skills/. Reuse existing repository entries via relative paths. Reference YAML for configurations, a directory containing SKILL.md for full Skills, or metadata-bearing Markdown for external Skill recommendations. Membership does not imply execution order. Shared instructions describe order, dependencies, and each resource; separate READMEs for child resources are unnecessary.

An instructional recipe may have only a README. Do not invent resources for it. Local configurations and items under skills/ must appear in resources.

## Format reference and review

The JSON files under schemas/ describe the three configuration types and entry metadata. They are format references, not an application or a required toolchain. Additional YAML shipped within Skills follows the Skill’s own format.

Review file paths, language tags, timing rules, and links before submitting. Maintainers review contributions against this document and the schemas. No build, dependency installation, or automated test step is required.

Original contributions use [MIT](../LICENSE). Third-party files retain their terms; linking external content does not change its license.

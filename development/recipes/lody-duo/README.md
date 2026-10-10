---
title: Lody Duo workflow
description: Eight role presets and an external Skill for coordinated development and independent review in Lody.
authors:
  - name: Samzong
    url: https://github.com/samzong
languages: [en]
tags: [development, debugging, collaboration, code-review]
source: https://github.com/samzong/samzong/tree/66b486d647a50faccdeaa0a1da73f5974023e2c3/.agents/skills/lody-duo
license: MIT
resources:
  - roles/archestrator.yaml
  - roles/build-standard.yaml
  - roles/build-deep.yaml
  - roles/build-fast.yaml
  - roles/research-deep.yaml
  - roles/research-fast.yaml
  - roles/review-fast.yaml
  - roles/review-deep.yaml
  - skills/lody-duo.md
---

# Lody Duo workflow

Use Lody Agent Roles to coordinate investigation, implementation, and independent review while keeping goal, authorization, verification, and completion responsibility with the host. Build Standard leads development; other roles fill concrete gaps. There is no fixed pipeline or requirement to run every role for every task.

This recipe adapts Samzong's [public role snapshot](https://github.com/samzong/samzong/blob/66b486d647a50faccdeaa0a1da73f5974023e2c3/.agents/skills/lody-duo/references/agent-roles.md), captured on 2026-10-10, into the repository's v1 sharing format. Every preset preserves the source role name, Agent identifier, and complete runtime settings. Each separate prompt is the complete English source prompt prefix. Descriptions are shortened to fit the 140-character format limit; installation-specific IDs, visibility, and capture metadata are not role configuration fields in v1.

The files are English, so `languages: [en]` describes the artifact language. The preserved prompts require concise Chinese conversation and progress replies; Git artifacts follow repository language conventions. `Archestrator` preserves the source role's spelling.

## Prerequisites

- Lody with callable Lody MCP session and Agent Role tools in the host and participating Agent environments. Current tool descriptions are authoritative.
- Your own machine, project, and supported Agent configurations. These presets use Claude Code (`claude`) and Codex (`codex`); their CLIs, authentication, and model access must already be available where used.
- The external [Lody Duo Skill and its required siblings](skills/lody-duo.md): `lody-duo`, `gmc`, and `liability-review`, installed alongside each other using the Agent's Skill discovery procedure. Install the [gmc CLI](https://github.com/samzong/gmc) separately for worktree operations.
- Applicable user and repository `AGENTS.md` instructions, an authorized task, and explicit write ownership. Installing or selecting these resources grants no additional business authority.

## Manual setup

1. Read the [external Skill recommendation](skills/lody-duo.md) and install the three required sibling Skill directories, including their supporting files. Install them on each participating machine where needed; do not assume a local installation exists on a remote machine.
2. Choose your machine and matching Agent configuration in Lody. Inspect that Agent's current model, mode, and option catalog before adopting a preset. The model IDs and settings below are captured suggestions, not guarantees of universal support or proof of a running session's model. If a required configuration is unavailable, report the limitation; do not silently substitute it.
3. Manually configure the workflow roles you intend to use. For each [role preset](#role-presets), use `name` and `description`, select the Agent identified by `recommended.agent`, and apply supported `recommended.runConfig` values. Copy the full Markdown file referenced by `promptFile` into the Role's prompt prefix. Choose your own machine, project, visibility, and any other installation settings. YAML is a sharing reference; this recipe does not promise an automatic importer, create roles, or bind a machine.
4. Start a Lody session using Archestrator and your intended project. Give the host the task, authorized scope, and acceptance conditions. Its prompt loads the installed `lody-duo` Skill by default. An existing host may instead invoke `lody-duo` explicitly. Actual dispatch must discover workspace roles through `lody_agent_role_list` and `lody_agent_role_get`, then use the returned role IDs, not IDs from another installation.
5. Confirm that the host can read the installed Skill and required tools before dispatch. Missing necessary capabilities must be reported while independent authorized work continues; there is no invented transport fallback.

## Role presets

The captured configuration separates coordination, development, investigation, and review. Codex `gpt-6.1-sol` with high effort is the lead/deep preset; `gpt-6-luna` with high effort is reserved for clearly defined Fast tasks whose evidence the lead verifies. High effort is an evidence-reliability constraint, not a correctness guarantee. Build Deep uses the captured Claude Code `opus`/medium preset for targeted design consultation. Archestrator uses `claude-fable-5-1`/medium for coordination. Review Fast retains the source's `gpt-6.1-sol`/medium setting; high-consequence targets go to Review Deep. These are responsibility-based suggestions, not measured performance claims.

| Preset | Responsibility |
| --- | --- |
| [Archestrator](roles/archestrator.yaml) | Host: goal, authority, partner selection, independent review, and final acceptance. |
| [Build Standard](roles/build-standard.yaml) | Primary development, technical judgment, integration, verification, and authorized delivery. |
| [Build Deep](roles/build-deep.yaml) | Targeted read-only design consultation; bounded implementation only when explicitly assigned. |
| [Build Fast](roles/build-fast.yaml) | Small implementation with a settled approach and acceptance conditions. |
| [Research Deep](roles/research-deep.yaml) | Complex read-only investigation, causal analysis, alternatives, and refutation. |
| [Research Fast](roles/research-fast.yaml) | Defined read-only searches, source checks, and narrow code location. |
| [Review Fast](roles/review-fast.yaml) | Fresh independent read-only review of routine, low-risk targets. |
| [Review Deep](roles/review-deep.yaml) | Fresh independent review of complex or high-consequence boundaries. |

The captured `bypassPermissions` and `agent-full-access` modes provide tool capability. They neither expand the user's authorized scope nor enforce filesystem read-only access. Research, consultation, and review remain read-only task contracts even when configured with broad tool permissions. Follow the runtime's approval rules; do not bypass required checks or infer merge, release, deployment, or external-message authority.

## Working order and acceptance

1. The host establishes the goal, scope, authority, actual project, and acceptance conditions from the request and applicable instructions. Use Research only for investigation gaps that need it; very small settled tasks may go directly to Build Fast.
2. For development, the host opens Build Standard as an independent session with explicit `workContext`. Build Standard owns investigation, the main implementation, integration, and verification. It consults Build Deep only for a specific unresolved design question and delegates to Build Fast only when a bounded handoff has a real benefit. Complexity alone does not transfer the whole task to Build Deep.
3. Allow one writer per worktree. Parallel writers require prior isolation through `gmc` under repository rules and assigned integration ownership. Only Build Standard may consult Build Deep or delegate to Build Fast; Research Deep may delegate to Research Fast. Build Deep, Review, and Fast do not delegate. Tabs cannot create nested Tabs.
4. The lead verifies every delegated diff and cited location and reruns conclusion-critical checks. Use a unique `operationId` per new dispatch or continuation and wait for automatic completion notifications. After a lost response, verify the original request and effects before recovery; preserve its ID rather than polling or duplicating dispatch. Cancellation or timeout alone does not prove a writer stopped.
5. After implementation and self-testing, the host arranges a fresh independent Review session without the author's reasoning. A design consultant cannot supply independent passing review of its own design. Review uses the **full applicable `liability-review` contract**, including required T2 refutation and finder passes; this recipe does not replace it with a summary. The host checks exact fingerprints and workspace state before and after review because permissions do not provide read-only isolation.
6. The host accepts only verified results at the affected entrypoint, resolves in-scope corrections, and follows required repository gates and actual delivery authority. Tool success, self-testing, and completion notifications alone are insufficient. Report evidence, unverified boundaries, and unresolved owner decisions; silence is not consent. New session and Tab titles follow `[Role name] Task title`, with first-turn verification and read-back under the full Skill's title rules.

## Attribution, maintenance, and limits

Role settings and prompts come from Samzong's [pinned English Skill package](https://github.com/samzong/samzong/tree/66b486d647a50faccdeaa0a1da73f5974023e2c3/.agents/skills/lody-duo). Preserve their [MIT notice](LICENSE), copyright 2026 Samzong. The [canonical package](https://github.com/samzong/samzong/tree/main/.agents/skills/lody-duo) is maintained externally; this recipe links the Skill instead of maintaining another full copy with its dependencies. Repository edits do not update installed Skills or actual roles. Refresh the presets and prompts together when adopting a newer source snapshot.

This is a manual configuration recipe. Publishing it does not establish successful role creation, installation, model execution, live delegation or recovery, browser connectivity, client setup, or compatibility across installations. Do not execute submitted prompts as part of format review. Lody Duo also does not guarantee continuous machine availability, exactly-once external effects, or automatic host recovery across restarts.

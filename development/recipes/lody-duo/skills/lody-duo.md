---
title: Lody Duo Skill
description: External Skill for Lody role orchestration with required worktree-isolation and independent-review contracts.
authors:
  - name: Samzong
    url: https://github.com/samzong
languages: [en]
tags: [development, collaboration, code-review]
source: https://github.com/samzong/samzong/tree/main/.agents/skills/lody-duo
license: MIT
---

# Lody Duo Skill

Samzong's Lody Duo Skill organizes investigation, development, and independent review through Lody MCP Agent Roles. The host retains goal, authorization, verification, and completion responsibility; Build Standard leads development by default. Use it with the [recipe's role presets and manual setup](../README.md).

## Installation and dependencies

Use your Agent's supported Skill installation procedure to copy these complete directories from the [canonical skills collection](https://github.com/samzong/samzong/tree/main/.agents/skills) into the same Skill discovery parent directory:

- [lody-duo](https://github.com/samzong/samzong/tree/66b486d647a50faccdeaa0a1da73f5974023e2c3/.agents/skills/lody-duo), including its references and Agent metadata.
- [gmc](https://github.com/samzong/samzong/tree/66b486d647a50faccdeaa0a1da73f5974023e2c3/.agents/skills/gmc), the mandatory worktree-lifecycle contract.
- [liability-review](https://github.com/samzong/samzong/tree/66b486d647a50faccdeaa0a1da73f5974023e2c3/.agents/skills/liability-review), the complete independent-review contract.

The pinned links match the recipe's source revision; consult the canonical collection for future maintenance. Preserve each directory's supporting files and sibling relative links. Install all three together; copying only `lody-duo` leaves this workflow incomplete. Follow each Skill's prerequisites, including any conditional tools for the selected mode. Install the [gmc CLI](https://github.com/samzong/gmc) separately; Skill installation does not install external CLIs, configure MCP clients, create roles, or bind machines. Participating Agents need working Lody MCP tools and their own supported Skill discovery environment.

## Usage and authority

After installation, start the recipe's Archestrator session or ask an existing Lody host to use `lody-duo`. The Skill first verifies the current Lody session and discovers actual workspace roles; manually configure compatible roles before dispatch. Missing required Skills, tools, or roles must be reported while independent authorized work continues. Do not silently switch orchestration transports or substitute unavailable configurations.

Keep the full applicable `liability-review` contract, including required T2 refutation and finder passes. Use `gmc` and repository rules to isolate parallel writers; keep one writer per worktree. The recipe's complete role prompts complement these contracts rather than replacing them. Broad permission modes describe capabilities, not business authority or filesystem read-only isolation. The preserved prompts request Chinese conversational replies despite the English artifact language.

This is an external recommendation, not a bundled Skill or installer. No live installation, role creation, model execution, or full workflow is claimed verified here. The external package retains Samzong's [MIT license](https://github.com/samzong/samzong/blob/66b486d647a50faccdeaa0a1da73f5974023e2c3/LICENSE); listing it does not change its terms.

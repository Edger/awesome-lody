---
title: Daily project check recipe
description: An example combining a Role and a scheduled task.
authors:
  - name: example-author
    url: https://github.com/example
languages: [en]
tags: [example]
resources:
  - roles/reviewer.yaml
  - schedules/daily-check.yaml
---

Template example. Replace metadata and instructions before submitting.

## Purpose and relevance to Lody

Explain the problem and how this resource is used in Lody.

## Prerequisites

Describe the required Agent, project, or tools.

## Usage

1. Create a reviewer from the [Role configuration](roles/reviewer.yaml), choosing your Agent.
2. Create a task from the [schedule configuration](schedules/daily-check.yaml), adopting the Role recommendations and choosing machine, project, and time zone.
3. Copy the [check prompt](prompts/check.md) into the task.
4. Create it through Lody and inspect results in the resulting conversations.

roleFile describes the relationship between resources. Follow the setup steps above.

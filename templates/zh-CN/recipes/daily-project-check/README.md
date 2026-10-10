---
title: 每日项目巡检组合
description: 组合 Role 与定时任务的示例。
authors:
  - name: example-author
    url: https://github.com/example
languages: [zh-CN]
tags: [example]
resources:
  - roles/reviewer.yaml
  - schedules/daily-check.yaml
---

模板示例，请替换元信息和说明后投稿。

## 用途与 Lody 的关联

说明解决什么问题，以及如何在 Lody 中使用。

## 所需环境

说明需要的 Agent、项目或工具。

## 使用方法

1. 使用 [Role 配置](roles/reviewer.yaml) 创建审查员，选择自己的 Agent。
2. 使用 [定时配置](schedules/daily-check.yaml) 创建任务；采用该 Role 的推荐设置，并选择机器、项目及时区。
3. 将 [巡检 Prompt](prompts/check.md) 填入定时任务。
4. 按 Lody 的流程创建，之后在运行产生的对话中查看结果。

roleFile 表达资源关系，按上述步骤完成设置。

# 分享格式 v1

[English](format.md)

这是 awesome-lody 的文件格式。按使用说明配置资源。路径标识条目；首次发布使用 schemaVersion 1，无独立条目版本或 manifest。

## 条目布局

`<场景>/<类型>/<条目>`；[场景列表](../README.zh-CN.md)和[类型列表](../CONTRIBUTING.zh-CN.md)。slug 使用小写英文、数字、连字符。

文章和视频是 `<slug>.md`。配置、完整 Skill、Recipe 是 `<slug>/README.md` 加资源文件。外链 Skill 是 `<slug>.md`。目录条目可提供 README.en.md、README.zh-CN.md 译文；译文不重复计数。所有文本使用 UTF-8，不使用符号链接。

## Markdown 入口元信息

```yaml
---
title: 我的项目审查员
description: 使用 Lody 检查项目改动。
authors:
  - name: your-name
    url: https://github.com/your-name
languages: [zh-CN]
tags: [code-review]
---
```

| 字段 | 要求 |
| --- | --- |
| title、description | 必填，非空文本 |
| authors | 必填，非空列表；name 必填，url 可选 HTTP(S) 地址 |
| languages | 必填，非空且不重复的 BCP 47 标签，例如 zh-CN、en |
| tags | 可选，不重复的文本列表 |
| source | 外链条目必填，原始来源 HTTP(S) 地址 |
| license | 可选，第三方复制资源应标明原授权并保留必要文件 |
| resources | 仅 Recipe，配置或 Skill 的相对路径列表 |

视频、文章和 Skill 等外链推荐必须填写 source。authors 记录原作者，Git 历史记录投稿者。场景和类型由路径确定，勿重复添加相应字段。不要使用未知字段或重复 YAML 键。

frontmatter 后必须有 Markdown 正文；使用说明的质量由 PR 审阅。完整 Skill 的 SKILL.md 保留原格式（name、description 和正文）；上述元信息放在同目录 README.md 中。

## 配置共同字段

仅 role.yaml、schedule.yaml、prompt.yaml 使用本格式，文件名固定在单项条目的根目录。Recipe 内可使用 reviewer.yaml 等描述性名称。每个 YAML 只描述一个资源。

| 字段 | 要求 |
| --- | --- |
| schemaVersion | 必填，整数 1 |
| kind | 必填，role / schedule / prompt |
| name | 必填，创建资源时的名称 |
| description | 可选，说明资源用途 |
| promptFile | 必填，相对当前 YAML 的 Markdown 文件路径 |

Prompt 文件只包含 Prompt 正文，无 frontmatter，且不为空。Role 名称最多 60 字符、描述最多 140；Prompt 名称最多 60、描述最多 240，正文最多 256 KiB；Schedule 名称最多 200、描述最多 1000，正文最多 32 KiB。

所有路径解析后必须留在仓库中，允许 `../` 复用仓库内资源，不允许绝对路径、URL、反斜杠和符号链接。引用改名或移动时同步更新。配置不包含个人内部 ID、运行状态和凭据。

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

recommended 可选但鼓励填写，存在时 agent 必填，使用可读的 Agent 标识。runConfig 可含 modelId、modeId、configOptionValues；选项值只能是字符串或布尔值。填写实际 Agent 支持的键和值，可添加真实使用的模型 ID，并在说明中解释选择。推荐设置可由使用者替换，应根据所用 Agent 支持的选项选择。

正文对应 Role 的 promptPrefix。机器和 Agent 配置由用户选择。v1 不保存 memory 绑定。权限设置如有推荐，仍需在说明中讲清用途，实际选择由使用者决定。

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

trigger 必填，支持两种形式：

- cron：expression 为五字段表达式；timeZone 可选，填写推荐 IANA 时区，如 Asia/Shanghai；省略时在使用时选择。
- interval：everyMs 为不小于 60000 的整数。起始时刻在使用时确定。

cron 使用五字段表达式，不使用随机 H 值。不会推断用户时区，不填一次性日期或运行状态。

可选 roleFile 引用 Role YAML；或者直接填写和 Role 相同的 recommended，两者不能同时出现。roleFile 表达采用该 Role 推荐设置和角色指令的意图；在使用说明中写清设置步骤。

## Prompt Shortcut

```yaml
schemaVersion: 1
kind: prompt
name: Review current changes
slug: review-changes
promptFile: prompt.md
```

slug 必填，1–40 字符，小写英文字母、数字、连字符，第一位为字母或数字。正文是纯文本，不做变量替换，不携带带 ID 的 mention 对象。Markdown、普通 @文字或其他符号保持字面文本；不要将它们描述为自动绑定的引用。

## Recipe

入口为 README.md；resources 在包含资源时列出每个配置和 Skill：

```yaml
resources:
  - roles/reviewer.yaml
  - schedules/daily-check.yaml
  - skills/project-summary
```

配置放在内部 roles/、schedules/、prompts/ 等目录，Skill 固定放 skills/。外部已有条目也可通过相对路径复用。配置引用指向 YAML，完整 Skill 指向含 SKILL.md 的目录，外链 Skill 推荐指向其带元信息的 Markdown。resources 仅表示包含哪些内容，不表示执行顺序；总说明解释顺序、依赖和每个资源的用途，不要求为内部资源分别写 README。

纯经验组合也可以只有 README，不需要虚构 resources。若有本地配置或 skills/ 下的 Skill，则必须列在 resources 中。

## 格式参考与审阅

schemas/ 下的 JSON 文件描述三类配置及条目元信息的字段，作为格式参考，不构成应用程序或必须使用的工具链。Skill 自带的其他 YAML 文件遵循其自身格式。

提交前检查文件路径、语言标记、时间规则和链接。维护者依据本文与 schema 审阅投稿，不要求构建、安装依赖或运行自动测试。

原创内容使用 [MIT](../LICENSE)。第三方文件保留原授权；外链目标不因收录改变许可证。

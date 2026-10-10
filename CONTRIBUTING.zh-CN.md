# 贡献指南

[English](CONTRIBUTING.md)

欢迎所有与 Lody 相关的配置、实践、教程和视频。结构符合要求、有使用说明即可提交，维护者在 PR 中判断收录边界，不要求你提供测试报告、效果证明或英文翻译。

## 选择位置

目录为 `<场景>/<类型>/<条目>`。场景列表见[首页](README.zh-CN.md)，类型如下：

| 类型 | 提交形式 |
| --- | --- |
| `roles/` | 目录：README.md、role.yaml、prompt.md |
| `schedules/` | 目录：README.md、schedule.yaml、prompt.md |
| `prompts/` | 目录：README.md、prompt.yaml、prompt.md |
| `skills/` | 完整 Skill 目录和 README.md，或一个外链 Markdown |
| `guides/` | 一个 Markdown，写原创经验或推荐外部文章 |
| `videos/` | 一个 Markdown，介绍并链接视频 |
| `recipes/` | 一个目录，含总说明和多个资源 |

选择一个主要场景，其他用途用 tags 表达。名称使用小写英文、数字和连字符。不要为每个场景复制同一份配置，也不需要创建空分类目录。

## 复制模板

直接复制文件即可，可在本地或 GitHub 网页编辑，不需要开发环境或安装依赖。

```sh
mkdir -p code-review/roles
cp -R templates/zh-CN/roles/example code-review/roles/my-reviewer
```

从[模板目录](templates/README.zh-CN.md)选择其他类型。替换示例作者、标题、语言、tags 和正文；删除与实际使用无关的模板说明。不要将模板示例当作已经验证的社区实践。

配置和 Skill 说明应包含：解决的问题、与 Lody 的关联、必要环境和使用步骤。推荐填写 Agent、模型、推理强度及选择理由，但不是合并硬性要求。文章、视频等外链只需简短介绍、关联说明及来源。两类都需要[元信息](docs/format.zh-CN.md)。

Prompt 正文保存在独立 Markdown 文件，配置用 promptFile 引用。首版 Shortcut 是纯文本；需要 Role、Skill 或文件时在说明中指导用户选择。机器、项目、Agent、时区等由使用者设置，不提交你的内部 ID、绝对路径或凭据。

## 语言和导航

原创内容不强制双语。languages 表示实际内容语言，例如 `[zh-CN]`；同时提供两种语言时写 `[zh-CN, en]`。目录条目的入口叫 README.md，可选翻译 README.en.md 或 README.zh-CN.md 并互相链接。完整 Skill 保留原有 SKILL.md 格式，仓库元信息写在 README.md。

在中英文首页的对应场景下添加类型小标题和条目链接，展示名称、简短介绍及语言，例如“我的审查员 — 检查项目改动 · 中文”。移除该场景的“暂无投稿”提示。可使用投稿原文标题，不要求翻译投稿本身。

## 检查与 PR

提交前对照[格式规范](docs/format.zh-CN.md)检查目录位置、元信息、配置字段和引用路径，确认链接指向正确内容。维护者在 PR 中审阅结构、使用说明、关联性和署名，不要求运行投稿内容。

提交 PR 时简述内容与 Lody 的关联。通常每个 PR 分享一个条目或一组相关实践，修复现有条目也欢迎。收录不表示维护者验证了运行效果。

## 署名与许可

仓库采用 [MIT](LICENSE)，原创投稿以 MIT 提交。推荐他人文章、视频或 Skill 时 authors 填原作者，source 填来源；投稿者由 Git 历史记录。复制第三方文件须符合原授权，填写 license 并保留必要的许可证与署名；单纯提供链接不会改变外部内容的许可证。不要复制没有相应授权的全文或文件。

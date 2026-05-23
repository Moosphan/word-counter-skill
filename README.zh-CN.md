# Word Counter Skills

**简体中文** | [English](README.md)

Word Counter 是一个可用于 Codex 和 Claude Code 的字数统计技能。它用固定规则统计中文、英文和中英混排文本，确保同一段内容每次都得到一致结果。

## 特性

- 提供确定性的 `zh`、`en`、`mixed` 三种统计方式
- 适用于文章、章节、小说、大纲、转写文本和粘贴文本
- 默认返回精简结果，只有在明确要求时才显示详细统计
- 中文提问返回中文结果，英文提问返回英文结果
- 同时提供 Codex skill 和 Claude Code skill

## 统计方式

- `zh`：统计中文字数
- `en`：统计英文词数
- `mixed`：统计中英混排总数

示例：

- `你好，世界！` -> `zh = 4`，`en = 0`，`mixed = 4`
- `OpenAI builds safe AI in 2026.` -> `zh = 24`，`en = 6`，`mixed = 6`
- `你好 OpenAI 2026` -> `zh = 12`，`en = 2`，`mixed = 4`

## 安装

### Codex

将 [skills/codex/word-counter](/Users/dorck/Documents/words-counter/skills/codex/word-counter) 复制到你的 Codex skills 目录，通常是 `~/.codex/skills/word-counter`。

### Claude Code

将 [skills/claude/.claude/skills/word-counter](/Users/dorck/Documents/words-counter/skills/claude/.claude/skills/word-counter) 复制到你的 Claude Code skills 目录，通常是 `~/.claude/skills/word-counter`。

## 如何使用

### 在 Codex 中

直接明确要求使用这个 skill，例如：

```text
请使用 word-counter skill 统计这篇文章的中文字数。
```

```text
Please use the word-counter skill to count this text in mixed mode.
```

如果你希望看到详细统计，也要直接说出来：

```text
请使用 word-counter skill，并显示详细统计数据。
```

### 在 Claude Code 中

通过 `/word-counter` 触发，例如：

```text
/word-counter 统计这个文件的英文词数。
```

```text
/word-counter Count this text in mixed mode and show detailed statistics.
```

## 你会得到什么

- 中文提问返回中文字段
- 英文提问返回英文字段
- 默认输出为精简版
- `CJK 字符`、`数字 token` 这类详细字段只有在你明确要求详细统计时才会出现

默认中文精简输出示例：

```md
# 字数统计结果

- 统计方式：`mixed`（中英混排总数）
- 总数：`4`
- 规则：`mixed_count = cjk_chars + english_words + number_tokens + other_words`

| 项目 | 数值 |
| --- | ---: |
| 中文字数 | 12 |
| 英文词数 | 2 |
| 混排总数 | 4 |
```

## 维护说明

发布与打包说明已移至 [docs/publish.md](docs/publish.md)。

## 许可证

本技能采用 [MIT License](/Users/dorck/Documents/words-counter/LICENSE) 开源发布。

# Word Counter Skills

[简体中文](README.zh-CN.md) | **English**

Word Counter is a skill for Codex and Claude Code. It counts Chinese text, English text, and mixed-language text with fixed rules, so the same content produces the same result every time.

## Features

- Deterministic counting for `zh`, `en`, and `mixed`
- Works well for articles, chapters, novels, outlines, transcripts, and pasted text
- Returns concise results by default, with detailed statistics only when requested
- Replies in Chinese for Chinese requests and in English for English requests
- Ships with both a Codex skill and a Claude Code skill

## Counting Modes

- `zh`: counts Chinese-style content length
- `en`: counts English words
- `mixed`: counts Chinese and English in one combined result

Examples:

- `你好，世界！` -> `zh = 4`, `en = 0`, `mixed = 4`
- `OpenAI builds safe AI in 2026.` -> `zh = 24`, `en = 6`, `mixed = 6`
- `你好 OpenAI 2026` -> `zh = 12`, `en = 2`, `mixed = 4`

## Install

### Codex

Copy [skills/codex/word-counter](/Users/dorck/Documents/words-counter/skills/codex/word-counter) into your Codex skills directory, usually `~/.codex/skills/word-counter`.

### Claude Code

Copy [skills/claude/.claude/skills/word-counter](/Users/dorck/Documents/words-counter/skills/claude/.claude/skills/word-counter) into your Claude Code skills directory, usually `~/.claude/skills/word-counter`.

## How To Use

### In Codex

Ask Codex to use the skill explicitly. For example:

```text
Please use the word-counter skill to count this chapter in zh mode.
```

```text
请使用 word-counter skill 统计这段文本的中英混排字数。
```

If you want detailed statistics, say so explicitly:

```text
Please use the word-counter skill and show detailed statistics.
```

### In Claude Code

Trigger the skill with `/word-counter`. For example:

```text
/word-counter Count this file with the English word count mode.
```

```text
/word-counter 统计这段文本的中文字数，并显示详细统计数据。
```

## What You Will Get

- Chinese requests return Chinese labels
- English requests return English labels
- Default output is concise
- Detailed fields such as `CJK characters` and `Number tokens` appear only when you explicitly ask for detailed statistics

Example concise Chinese output:

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

## For Maintainers

Release and publishing notes live in [docs/publish.md](docs/publish.md).

## License

This skill is released under the [MIT License](/Users/dorck/Documents/words-counter/LICENSE).

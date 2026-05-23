---
name: word-counter
description: Deterministic counting for Chinese, English, and mixed-language text such as articles, essays, novels, chapters, outlines, transcripts, and pasted paragraphs. Use when the user asks for word count, character count, manuscript length, bilingual text count, chapter length, or wants a stable count instead of a model estimate.
---

# Word Counter

Use the bundled script to produce a reproducible count instead of estimating from the model.

If the user asks in Chinese, run the script with `--locale zh` so the report is returned in Chinese. If the user asks in English, use `--locale en`. Only use `--details` when the user explicitly asks for detailed statistics.

## Pick A Profile

- Use `zh` for Chinese-style content counting.
- Use `en` for English-style word counting.
- Use `mixed` for one total across Chinese and English text.

If the user is ambiguous, run `mixed` first and mention the `zh` and `en` alternatives.

## Run The Script

For pasted content:

```bash
python3 "$HOME/.claude/skills/word-counter/scripts/word_counter.py" --profile mixed --locale en --format markdown --text "Hello world from OpenAI"
```

For a file:

```bash
python3 "$HOME/.claude/skills/word-counter/scripts/word_counter.py" --profile zh --locale zh --format markdown ./chapter-01.txt
```

## Return A Clear Summary

Return this compact Markdown structure. Use the English example as the default format reference:

```markdown
# Word Count Result

- Selected profile: `mixed` (Mixed-language count)
- Selected total: `1234`
- Applied formula: `mixed_count = cjk_chars + english_words + number_tokens + other_words`

| Metric | Value |
| --- | ---: |
| Chinese count | 1300 |
| English words | 45 |
| Mixed total | 1234 |
| Line count | 12 |
| Paragraph count | 4 |
```

For Chinese replies, use the same compact structure with Chinese labels. Do not show `CJK characters`, `English words`, or `Number tokens` unless the user explicitly asks for detailed statistics, in which case run with `--details`.

For rules and examples, read [references/counting-rules.md](references/counting-rules.md).

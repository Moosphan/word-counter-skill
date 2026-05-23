# Counting Rules

Use the same formulas as the Codex package so both platforms return identical totals.

## Profiles

### `zh`

```text
zh_content_chars = cjk_chars + latin_letters + digit_chars + other_letter_chars
```

### `en`

```text
en_word_count = english_words + number_tokens + other_words
```

### `mixed`

```text
mixed_count = cjk_chars + english_words + number_tokens + other_words
```

## Token Behavior

- Count each CJK character as `1`.
- Count `don't` as one English word.
- Count `state-of-the-art` as one English word.
- Count `2026`, `3.14`, `10/10`, and `25%` as one number token.
- Ignore whitespace and punctuation when producing the selected total.

## Example

Input:

```text
你好 OpenAI 2026
```

Output totals:

- `zh_content_chars = 12`
- `en_word_count = 2`
- `mixed_count = 4`


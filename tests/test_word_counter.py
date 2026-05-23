from __future__ import annotations

import json
import subprocess
import sys
import unittest
from pathlib import Path


PROJECT_ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(PROJECT_ROOT / "src"))

from word_counter import analyze_text  # noqa: E402


class WordCounterTests(unittest.TestCase):
    def test_chinese_profile_counts_content_characters(self) -> None:
        result = analyze_text("你好，世界！", profile="zh")
        self.assertEqual(result.selected_total, 4)
        self.assertEqual(result.zh_content_chars, 4)
        self.assertEqual(result.cjk_chars, 4)
        self.assertEqual(result.punctuation_chars, 2)

    def test_english_profile_counts_words_and_numbers(self) -> None:
        result = analyze_text("OpenAI builds safe AI in 2026.", profile="en")
        self.assertEqual(result.en_word_count, 6)
        self.assertEqual(result.selected_total, 6)
        self.assertEqual(result.english_words, 5)
        self.assertEqual(result.number_tokens, 1)

    def test_mixed_profile_counts_cjk_plus_word_tokens(self) -> None:
        result = analyze_text("你好 OpenAI 2026", profile="mixed")
        self.assertEqual(result.selected_total, 4)
        self.assertEqual(result.mixed_count, 4)
        self.assertEqual(result.zh_content_chars, 12)
        self.assertEqual(result.english_words, 1)
        self.assertEqual(result.number_tokens, 1)

    def test_fullwidth_content_normalizes_for_tokenization(self) -> None:
        result = analyze_text("ＡＩ测试１２３", profile="mixed")
        self.assertEqual(result.cjk_chars, 2)
        self.assertEqual(result.latin_letters, 2)
        self.assertEqual(result.digit_chars, 3)
        self.assertEqual(result.english_words, 1)
        self.assertEqual(result.number_tokens, 1)
        self.assertEqual(result.selected_total, 4)

    def test_cli_json_output(self) -> None:
        script = PROJECT_ROOT / "src" / "word_counter.py"
        proc = subprocess.run(
            [
                sys.executable,
                str(script),
                "--profile",
                "mixed",
                "--format",
                "json",
                "--text",
                "你好 OpenAI 2026",
            ],
            check=True,
            capture_output=True,
            text=True,
        )
        payload = json.loads(proc.stdout)
        self.assertEqual(payload["selected_total"], 4)
        self.assertEqual(payload["mixed_count"], 4)

    def test_cli_markdown_output(self) -> None:
        script = PROJECT_ROOT / "src" / "word_counter.py"
        proc = subprocess.run(
            [
                sys.executable,
                str(script),
                "--profile",
                "mixed",
                "--locale",
                "en",
                "--text",
                "你好 OpenAI 2026",
            ],
            check=True,
            capture_output=True,
            text=True,
        )
        self.assertIn("# Word Count Result", proc.stdout)
        self.assertIn("| Mixed total | 4 |", proc.stdout)
        self.assertNotIn("CJK characters", proc.stdout)
        self.assertNotIn("Number tokens", proc.stdout)

    def test_cli_markdown_output_in_chinese(self) -> None:
        script = PROJECT_ROOT / "src" / "word_counter.py"
        proc = subprocess.run(
            [
                sys.executable,
                str(script),
                "--profile",
                "en",
                "--locale",
                "zh",
                "--text",
                "OpenAI builds safe AI in 2026.",
            ],
            check=True,
            capture_output=True,
            text=True,
        )
        self.assertIn("# 字数统计结果", proc.stdout)
        self.assertIn("- 统计方式：`en`（英文词数）", proc.stdout)
        self.assertIn("| 英文词数 | 6 |", proc.stdout)
        self.assertNotIn("中文字数", proc.stdout)
        self.assertNotIn("数字 token", proc.stdout)

    def test_cli_full_detail_output_shows_hidden_metrics(self) -> None:
        script = PROJECT_ROOT / "src" / "word_counter.py"
        proc = subprocess.run(
            [
                sys.executable,
                str(script),
                "--profile",
                "mixed",
                "--locale",
                "zh",
                "--details",
                "--text",
                "你好 OpenAI 2026",
            ],
            check=True,
            capture_output=True,
            text=True,
        )
        self.assertIn("| CJK 字符 | 2 |", proc.stdout)
        self.assertIn("| 数字 token | 1 |", proc.stdout)
        self.assertIn("| 原文长度 | 14 |", proc.stdout)


if __name__ == "__main__":
    unittest.main()

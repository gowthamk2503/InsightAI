"""Utility Functions Module

This module contains various utility functions for text processing,
statistics, and UI helpers.
"""

import re
from collections import Counter
import math


class TextUtils:
    @staticmethod
    def count_words(text: str) -> int:
        """Count the number of words in the text."""
        return len(text.split())

    @staticmethod
    def count_characters(text: str) -> int:
        """Count the number of characters in the text (excluding spaces)."""
        return len(text.replace(" ", "").replace("\n", ""))

    @staticmethod
    def estimate_reading_time(text: str, words_per_minute: int = 200) -> float:
        """Estimate reading time in minutes."""
        word_count = TextUtils.count_words(text)
        return word_count / words_per_minute

    @staticmethod
    def calculate_compression_ratio(original_text: str, summary_text: str) -> float:
        """Calculate the compression ratio as a percentage."""
        if not original_text.strip():
            return 0.0
        original_words = TextUtils.count_words(original_text)
        summary_words = TextUtils.count_words(summary_text)
        if original_words == 0:
            return 0.0
        return ((original_words - summary_words) / original_words) * 100

    @staticmethod
    def highlight_sentences(original_text: str, summary_sentences: list) -> str:
        """Highlight sentences in the original text that appear in the summary."""
        highlighted_text = original_text
        for sentence in summary_sentences:
            sentence_str = str(sentence).strip()
            if sentence_str:
                # Use simple markup for highlighting
                highlighted_text = highlighted_text.replace(
                    sentence_str,
                    f"**{sentence_str}**"
                )
        return highlighted_text

    @staticmethod
    def extract_sentences(text: str) -> list:
        """Extract sentences from text."""
        # Simple sentence splitting
        sentences = re.split(r'(?<=[.!?])\s+', text.strip())
        return [s.strip() for s in sentences if s.strip()]


class UIUtils:
    @staticmethod
    def format_time(minutes: float) -> str:
        """Format time in minutes to a readable string."""
        if minutes < 1:
            seconds = int(minutes * 60)
            return f"{seconds} sec"
        elif minutes < 60:
            return f"{minutes:.1f} min"
        else:
            hours = int(minutes // 60)
            mins = int(minutes % 60)
            return f"{hours}h {mins}m"

    @staticmethod
    def format_percentage(value: float) -> str:
        """Format a float as percentage."""
        return f"{value:.1f}%"
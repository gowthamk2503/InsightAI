"""Keyword Extractor Module

This module extracts important keywords from text using frequency analysis.
"""

import re
from collections import Counter


class KeywordExtractor:
    @staticmethod
    def extract_keywords(text: str, num_keywords: int = 10) -> list:
        """Extract the most common keywords from the text.

        Args:
            text: The input text.
            num_keywords: Number of keywords to return.

        Returns:
            List of top keywords.
        """
        keywords, _ = KeywordExtractor.extract_keywords_with_frequencies(text, num_keywords)
        return keywords

    @staticmethod
    def extract_keywords_with_frequencies(text: str, num_keywords: int = 10) -> tuple:
        """Extract keywords with their frequencies.

        Returns:
            Tuple of (keywords_list, frequencies_list)
        """
        if not text.strip():
            return [], []

        # Clean the text: remove punctuation, convert to lowercase
        cleaned_text = re.sub(r'[^\w\s]', '', text.lower())

        # Split into words
        words = cleaned_text.split()

        # Remove common stop words (basic list)
        stop_words = set([
            'the', 'a', 'an', 'and', 'or', 'but', 'if', 'while', 'at', 'by', 'for',
            'with', 'about', 'against', 'between', 'into', 'through', 'during',
            'before', 'after', 'above', 'below', 'to', 'from', 'up', 'down', 'in',
            'out', 'on', 'off', 'over', 'under', 'again', 'further', 'then',
            'once', 'here', 'there', 'when', 'where', 'why', 'how', 'all', 'any',
            'both', 'each', 'few', 'more', 'most', 'other', 'some', 'such', 'no',
            'nor', 'not', 'only', 'own', 'same', 'so', 'than', 'too', 'very', 's',
            't', 'can', 'will', 'just', 'don', 'should', 'now'
        ])

        # Filter words
        filtered_words = [word for word in words if word not in stop_words and len(word) > 2]

        # Count frequencies
        word_counts = Counter(filtered_words)

        # Get top keywords and frequencies
        top_items = word_counts.most_common(num_keywords)
        keywords = [word for word, _ in top_items]
        frequencies = [count for _, count in top_items]

        return keywords, frequencies

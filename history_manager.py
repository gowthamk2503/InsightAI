"""History Manager Module

This module manages the history of generated summaries.
"""

import json
import os
from datetime import datetime
from typing import List, Dict


class HistoryManager:
    def __init__(self, history_file: str = "summary_history.json"):
        self.history_file = history_file
        self.history: List[Dict] = []
        self.load_history()

    def load_history(self):
        """Load history from file."""
        if os.path.exists(self.history_file):
            try:
                with open(self.history_file, 'r', encoding='utf-8') as f:
                    self.history = json.load(f)
            except:
                self.history = []

    def save_history(self):
        """Save history to file."""
        try:
            with open(self.history_file, 'w', encoding='utf-8') as f:
                json.dump(self.history, f, indent=2, ensure_ascii=False)
        except Exception as e:
            print(f"Error saving history: {e}")

    def add_entry(self, original_text: str, summary: str, keywords: list,
                  algorithm: str, length: str, compression_ratio: float):
        """Add a new summary entry to history."""
        entry = {
            'timestamp': datetime.now().isoformat(),
            'original_text': original_text[:500] + '...' if len(original_text) > 500 else original_text,
            'summary': summary,
            'keywords': keywords,
            'algorithm': algorithm,
            'length': length,
            'compression_ratio': compression_ratio,
            'original_word_count': len(original_text.split()),
            'summary_word_count': len(summary.split())
        }

        self.history.insert(0, entry)  # Add to beginning

        # Keep only last 50 entries
        if len(self.history) > 50:
            self.history = self.history[:50]

        self.save_history()

    def get_history(self) -> List[Dict]:
        """Get all history entries."""
        return self.history.copy()

    def delete_entry(self, index: int):
        """Delete an entry by index."""
        if 0 <= index < len(self.history):
            self.history.pop(index)
            self.save_history()

    def clear_history(self):
        """Clear all history."""
        self.history = []
        self.save_history()
"""Charts Module

This module handles chart generation using matplotlib for keyword frequency visualization.
"""

import matplotlib.pyplot as plt
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg
import customtkinter as ctk
from collections import Counter


class ChartGenerator:
    @staticmethod
    def create_keyword_chart(keywords: list, frequencies: list, parent_widget):
        """Create a bar chart for keyword frequencies."""
        # Clear any existing chart
        for widget in parent_widget.winfo_children():
            widget.destroy()

        if not keywords or not frequencies:
            no_data_label = ctk.CTkLabel(parent_widget, text="No keywords to display")
            no_data_label.pack(expand=True)
            return

        # Create figure
        fig, ax = plt.subplots(figsize=(6, 4), dpi=100)
        fig.patch.set_facecolor('#2b2b2b')  # Dark background
        ax.set_facecolor('#2b2b2b')

        # Create bars
        bars = ax.bar(keywords, frequencies, color='#1f6aa5', alpha=0.8)

        # Customize appearance
        ax.set_title('Keyword Frequency', color='white', fontsize=12, fontweight='bold')
        ax.set_xlabel('Keywords', color='white', fontsize=10)
        ax.set_ylabel('Frequency', color='white', fontsize=10)
        ax.tick_params(colors='white', labelsize=8)

        # Rotate x-axis labels for better readability
        plt.xticks(rotation=45, ha='right')

        # Add value labels on bars
        for bar in bars:
            height = bar.get_height()
            ax.text(bar.get_x() + bar.get_width()/2., height,
                   f'{int(height)}', ha='center', va='bottom',
                   color='white', fontsize=8)

        plt.tight_layout()

        # Embed in tkinter
        canvas = FigureCanvasTkAgg(fig, master=parent_widget)
        canvas.draw()
        canvas.get_tk_widget().pack(fill="both", expand=True)

        return canvas

    @staticmethod
    def get_keyword_frequencies(text: str, keywords: list) -> list:
        """Get frequencies for the given keywords in the text."""
        if not text or not keywords:
            return []

        # Clean text
        import re
        cleaned_text = re.sub(r'[^\w\s]', '', text.lower())
        words = cleaned_text.split()

        # Count frequencies
        word_counts = Counter(words)

        return [word_counts.get(keyword.lower(), 0) for keyword in keywords]
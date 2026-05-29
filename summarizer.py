"""Text Summarizer Module

This module uses the Sumy library to generate summaries of text.
It supports different summary lengths and multiple algorithms.
"""

from sumy.parsers.plaintext import PlaintextParser
from sumy.nlp.tokenizers import Tokenizer
from sumy.summarizers.lsa import LsaSummarizer
from sumy.summarizers.text_rank import TextRankSummarizer
from sumy.summarizers.lex_rank import LexRankSummarizer
from sumy.nlp.stemmers import Stemmer
from sumy.utils import get_stop_words


class TextSummarizer:
    def __init__(self, language="english"):
        self.language = language
        self.stemmer = Stemmer(language)
        self.summarizers = {
            'lsa': LsaSummarizer(self.stemmer),
            'textrank': TextRankSummarizer(self.stemmer),
            'lexrank': LexRankSummarizer(self.stemmer)
        }
        for summarizer in self.summarizers.values():
            summarizer.stop_words = get_stop_words(language)

    def summarize(self, text: str, length: str = "medium", algorithm: str = "lsa") -> str:
        """Generate a summary of the given text.

        Args:
            text: The input text to summarize.
            length: 'short', 'medium', or 'long' for summary length.
            algorithm: 'lsa', 'textrank', or 'lexrank'.

        Returns:
            A summarized version of the text.
        """
        if not text.strip():
            return "No text provided."

        # Parse the text
        parser = PlaintextParser.from_string(text, Tokenizer(self.language))

        # Determine number of sentences based on length
        if length == "short":
            sentence_count = 2
        elif length == "medium":
            sentence_count = 4
        elif length == "long":
            sentence_count = 6
        else:
            sentence_count = 4  # default to medium

        # Get the summarizer
        summarizer = self.summarizers.get(algorithm.lower(), self.summarizers['lsa'])

        # Generate summary
        summary_sentences = summarizer(parser.document, sentence_count)

        # Join sentences into a string
        summary = " ".join(str(sentence) for sentence in summary_sentences)

        return summary if summary else "Unable to generate summary."

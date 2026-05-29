"""AI Smart Text Summarizer

Entry point for the application. Launches the GUI.
"""

from ui import SummarizerApp


def main():
    # Create and run the app
    app = SummarizerApp()
    app.mainloop()


if __name__ == "__main__":
    main()

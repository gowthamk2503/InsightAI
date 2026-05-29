"""User Interface for AI Smart Text Summarizer - Corporate HR Theme

This module creates a modern GUI using CustomTkinter with HR corporate styling.
"""

import tkinter as tk
from tkinter import filedialog, messagebox, scrolledtext
import customtkinter as ctk
import threading
import pyperclip
import matplotlib.pyplot as plt
plt.style.use('seaborn-v0_8-whitegrid')

from summarizer import TextSummarizer
from pdf_reader import PDFReader
from keyword_extractor import KeywordExtractor
from charts import ChartGenerator
from history_manager import HistoryManager
from utils import TextUtils, UIUtils


# ── HR Corporate Colour Palette ──────────────────────────────────────────────
HR_NAVY          = "#1B2A4A"   # primary brand / sidebar bg
HR_NAVY_LIGHT    = "#243560"   # hover / selected nav item
HR_BLUE          = "#2E5DA6"   # accent buttons
HR_BLUE_HOVER    = "#3A72CC"   # button hover
HR_GOLD          = "#C9A84C"   # highlight / badge accent
HR_WHITE         = "#FFFFFF"
HR_OFF_WHITE     = "#F4F6FA"   # page background
HR_SURFACE       = "#FFFFFF"   # card surface
HR_BORDER        = "#D6DCE8"   # subtle border
HR_TEXT_PRIMARY  = "#1B2A4A"   # headings
HR_TEXT_BODY     = "#3D4F6B"   # body copy
HR_TEXT_MUTED    = "#7A8DAA"   # labels / hints
HR_SUCCESS       = "#1E7E5E"
HR_DANGER        = "#C0392B"


# ── Custom Fonts (fallback chain keeps it cross-platform) ─────────────────────
FONT_HEADING   = ("Georgia", 20, "bold")
FONT_SUBHEAD   = ("Georgia", 14, "bold")
FONT_LABEL     = ("Segoe UI", 10, "bold")
FONT_BODY      = ("Segoe UI", 10)
FONT_SMALL     = ("Segoe UI", 9)
FONT_MONO      = ("Courier New", 10)


class HRCard(ctk.CTkFrame):
    """A white card with a subtle border – the base HR UI surface."""

    def __init__(self, master, **kwargs):
        kwargs.setdefault("fg_color", HR_SURFACE)
        kwargs.setdefault("border_width", 1)
        kwargs.setdefault("border_color", HR_BORDER)
        kwargs.setdefault("corner_radius", 8)
        super().__init__(master, **kwargs)


class HRButton(ctk.CTkButton):
    """Primary action button styled in HR navy-blue."""

    def __init__(self, master, **kwargs):
        kwargs.setdefault("fg_color", HR_BLUE)
        kwargs.setdefault("hover_color", HR_BLUE_HOVER)
        kwargs.setdefault("text_color", HR_WHITE)
        kwargs.setdefault("corner_radius", 6)
        kwargs.setdefault("font", ctk.CTkFont(family="Segoe UI", size=10, weight="bold"))
        super().__init__(master, **kwargs)


class HRSecondaryButton(ctk.CTkButton):
    """Secondary / ghost button."""

    def __init__(self, master, **kwargs):
        kwargs.setdefault("fg_color", "transparent")
        kwargs.setdefault("hover_color", HR_OFF_WHITE)
        kwargs.setdefault("text_color", HR_BLUE)
        kwargs.setdefault("border_width", 1)
        kwargs.setdefault("border_color", HR_BLUE)
        kwargs.setdefault("corner_radius", 6)
        kwargs.setdefault("font", ctk.CTkFont(family="Segoe UI", size=10))
        super().__init__(master, **kwargs)


class HRDangerButton(ctk.CTkButton):
    """Destructive action button."""

    def __init__(self, master, **kwargs):
        kwargs.setdefault("fg_color", HR_DANGER)
        kwargs.setdefault("hover_color", "#A93226")
        kwargs.setdefault("text_color", HR_WHITE)
        kwargs.setdefault("corner_radius", 6)
        kwargs.setdefault("font", ctk.CTkFont(family="Segoe UI", size=10))
        super().__init__(master, **kwargs)


class StatusBadge(ctk.CTkLabel):
    """A coloured pill badge (e.g. 'LSA', 'Medium')."""

    COLOURS = {
        "blue":  (HR_BLUE,    HR_WHITE),
        "gold":  (HR_GOLD,    HR_WHITE),
        "green": (HR_SUCCESS, HR_WHITE),
        "muted": (HR_BORDER,  HR_TEXT_BODY),
    }

    def __init__(self, master, text, colour="blue", **kwargs):
        bg, fg = self.COLOURS.get(colour, self.COLOURS["blue"])
        kwargs.setdefault("fg_color", bg)
        kwargs.setdefault("text_color", fg)
        kwargs.setdefault("corner_radius", 10)
        kwargs.setdefault("font", ctk.CTkFont(family="Segoe UI", size=9, weight="bold"))
        kwargs.setdefault("padx", 8)
        kwargs.setdefault("pady", 2)
        super().__init__(master, text=text.upper(), **kwargs)


# ─────────────────────────────────────────────────────────────────────────────
#  Main Application
# ─────────────────────────────────────────────────────────────────────────────

class SummarizerApp(ctk.CTk):

    def __init__(self):
        super().__init__()

        # ── Window setup ──────────────────────────────────────────────────────
        self.title("HR Document Intelligence — AI Summarizer")
        self.geometry("1280x820")
        self.minsize(1024, 680)
        self.resizable(True, True)

        # Force light mode so our custom HR palette displays correctly
        ctk.set_appearance_mode("light")
        ctk.set_default_color_theme("blue")
        self.configure(fg_color=HR_OFF_WHITE)

        # ── Domain components ─────────────────────────────────────────────────
        self.summarizer        = TextSummarizer()
        self.pdf_reader        = PDFReader()
        self.keyword_extractor = KeywordExtractor()
        self.history_manager   = HistoryManager()
        self.chart_generator   = ChartGenerator()

        # ── State ─────────────────────────────────────────────────────────────
        self.current_text      = ""
        self.current_summary   = ""
        self.current_keywords  = []
        self.keyword_frequencies = []
        self.is_processing     = False

        # ── Build ─────────────────────────────────────────────────────────────
        self._build_ui()

    # ── Top-level layout ──────────────────────────────────────────────────────

    def _build_ui(self):
        # Root grid: sidebar | content
        self.grid_columnconfigure(1, weight=1)
        self.grid_rowconfigure(0, weight=1)

        self._build_sidebar()
        self._build_content_area()

    # ── Sidebar ───────────────────────────────────────────────────────────────

    def _build_sidebar(self):
        sidebar = ctk.CTkFrame(self, fg_color=HR_NAVY, corner_radius=0, width=220)
        sidebar.grid(row=0, column=0, sticky="ns")
        sidebar.grid_propagate(False)
        sidebar.grid_rowconfigure(10, weight=1)   # spacer row

        # Logo / brand strip
        brand_frame = ctk.CTkFrame(sidebar, fg_color=HR_NAVY, corner_radius=0)
        brand_frame.grid(row=0, column=0, sticky="ew", padx=0, pady=0)

        logo_label = ctk.CTkLabel(
            brand_frame,
            text="⬡  HR Intelligence",
            font=ctk.CTkFont(family="Georgia", size=15, weight="bold"),
            text_color=HR_WHITE,
            anchor="w",
        )
        logo_label.pack(padx=20, pady=(28, 4))

        tagline = ctk.CTkLabel(
            brand_frame,
            text="Document Analysis Suite",
            font=ctk.CTkFont(family="Segoe UI", size=9),
            text_color=HR_TEXT_MUTED,
            anchor="w",
        )
        tagline.pack(padx=20, pady=(0, 20))

        # Divider
        div = ctk.CTkFrame(sidebar, fg_color="#2E3F60", height=1, corner_radius=0)
        div.grid(row=1, column=0, sticky="ew", padx=0)

        # Section label
        section_lbl = ctk.CTkLabel(
            sidebar,
            text="NAVIGATION",
            font=ctk.CTkFont(family="Segoe UI", size=8, weight="bold"),
            text_color=HR_TEXT_MUTED,
            anchor="w",
        )
        section_lbl.grid(row=2, column=0, sticky="w", padx=20, pady=(18, 6))

        # Nav items  (icon, label, page_key)
        nav_items = [
            ("📄", "Summarize",      "main"),
            ("📚", "History",        "history"),
        ]

        self._nav_buttons = {}
        for r, (icon, label, page) in enumerate(nav_items, start=3):
            btn = ctk.CTkButton(
                sidebar,
                text=f"  {icon}  {label}",
                command=lambda p=page: self._show_page(p),
                anchor="w",
                fg_color="transparent",
                hover_color=HR_NAVY_LIGHT,
                text_color=HR_WHITE,
                corner_radius=6,
                font=ctk.CTkFont(family="Segoe UI", size=11),
                height=38,
            )
            btn.grid(row=r, column=0, sticky="ew", padx=12, pady=2)
            self._nav_buttons[page] = btn

        # Spacer
        # (row 10 is weight=1 spacer)

        # Bottom: user card
        user_card = ctk.CTkFrame(sidebar, fg_color=HR_NAVY_LIGHT, corner_radius=8)
        user_card.grid(row=11, column=0, sticky="ew", padx=12, pady=(0, 20))

        avatar = ctk.CTkLabel(
            user_card,
            text="HR",
            font=ctk.CTkFont(family="Segoe UI", size=12, weight="bold"),
            fg_color=HR_GOLD,
            text_color=HR_WHITE,
            corner_radius=20,
            width=36,
            height=36,
        )
        avatar.grid(row=0, column=0, padx=(10, 8), pady=10)

        name_lbl = ctk.CTkLabel(
            user_card,
            text="HR Department",
            font=ctk.CTkFont(family="Segoe UI", size=10, weight="bold"),
            text_color=HR_WHITE,
            anchor="w",
        )
        name_lbl.grid(row=0, column=1, sticky="w", pady=10)

    # ── Content area ─────────────────────────────────────────────────────────

    def _build_content_area(self):
        wrapper = ctk.CTkFrame(self, fg_color=HR_OFF_WHITE, corner_radius=0)
        wrapper.grid(row=0, column=1, sticky="nsew")
        wrapper.grid_rowconfigure(1, weight=1)
        wrapper.grid_columnconfigure(0, weight=1)

        self._build_topbar(wrapper)

        self.pages = {}
        self.current_page = "main"

        page_host = ctk.CTkFrame(wrapper, fg_color=HR_OFF_WHITE, corner_radius=0)
        page_host.grid(row=1, column=0, sticky="nsew")
        page_host.grid_rowconfigure(0, weight=1)
        page_host.grid_columnconfigure(0, weight=1)
        self._page_host = page_host

        self._build_main_page(page_host)
        self._build_history_page(page_host)
        self._show_page("main")

    def _build_topbar(self, parent):
        bar = ctk.CTkFrame(parent, fg_color=HR_SURFACE, corner_radius=0,
                           border_width=0, height=56)
        bar.grid(row=0, column=0, sticky="ew")
        bar.grid_propagate(False)
        bar.grid_columnconfigure(1, weight=1)

        # Page title (updated dynamically)
        self._topbar_title = ctk.CTkLabel(
            bar,
            text="Text Summarization",
            font=ctk.CTkFont(family="Georgia", size=16, weight="bold"),
            text_color=HR_TEXT_PRIMARY,
        )
        self._topbar_title.grid(row=0, column=0, padx=24, pady=0, sticky="w")

        # Right side: breadcrumb / meta
        meta_lbl = ctk.CTkLabel(
            bar,
            text="Human Resources  ›  Document Intelligence",
            font=ctk.CTkFont(family="Segoe UI", size=9),
            text_color=HR_TEXT_MUTED,
        )
        meta_lbl.grid(row=0, column=2, padx=24, pady=0, sticky="e")

        # Bottom border line
        border = ctk.CTkFrame(parent, fg_color=HR_BORDER, height=1, corner_radius=0)
        border.grid(row=0, column=0, sticky="sew")

    # ── Main page ─────────────────────────────────────────────────────────────

    def _build_main_page(self, host):
        page = ctk.CTkScrollableFrame(host, fg_color=HR_OFF_WHITE, corner_radius=0)
        page.grid(row=0, column=0, sticky="nsew")
        page.grid_columnconfigure(0, weight=1)
        self.pages["main"] = page

        # ── Stats row ────────────────────────────────────────────────────────
        stats_row = ctk.CTkFrame(page, fg_color="transparent")
        stats_row.pack(fill="x", padx=24, pady=(20, 0))
        stats_row.grid_columnconfigure((0, 1, 2, 3), weight=1)

        self._stat_cards = {}
        stats = [
            ("Documents Processed", "0",  "📄"),
            ("Words Analysed",       "0",  "🔤"),
            ("Avg. Compression",     "0%", "📉"),
            ("Keywords Found",       "0",  "🏷️"),
        ]
        for col, (label, val, icon) in enumerate(stats):
            card = HRCard(stats_row)
            card.grid(row=0, column=col, padx=(0 if col == 0 else 8, 0), sticky="ew")
            ctk.CTkLabel(card, text=f"{icon}  {label}",
                         font=ctk.CTkFont(family="Segoe UI", size=9),
                         text_color=HR_TEXT_MUTED).pack(anchor="w", padx=14, pady=(12, 2))
            val_lbl = ctk.CTkLabel(card, text=val,
                                   font=ctk.CTkFont(family="Georgia", size=22, weight="bold"),
                                   text_color=HR_TEXT_PRIMARY)
            val_lbl.pack(anchor="w", padx=14, pady=(0, 12))
            self._stat_cards[label] = val_lbl

        # ── Two-column work area ──────────────────────────────────────────────
        work = ctk.CTkFrame(page, fg_color="transparent")
        work.pack(fill="both", expand=True, padx=24, pady=16)
        work.grid_columnconfigure(0, weight=2)
        work.grid_columnconfigure(1, weight=3)
        work.grid_rowconfigure(0, weight=1)

        self._build_input_panel(work)
        self._build_output_panel(work)

    def _build_input_panel(self, parent):
        card = HRCard(parent)
        card.grid(row=0, column=0, sticky="nsew", padx=(0, 10))
        card.grid_rowconfigure(3, weight=1)
        card.grid_columnconfigure(0, weight=1)

        # Card header
        hdr = ctk.CTkFrame(card, fg_color=HR_NAVY, corner_radius=0,
                           height=44)
        hdr.grid(row=0, column=0, sticky="ew")
        hdr.grid_propagate(False)
        hdr.grid_columnconfigure(1, weight=1)

        ctk.CTkLabel(hdr, text="  Document Input",
                     font=ctk.CTkFont(family="Segoe UI", size=11, weight="bold"),
                     text_color=HR_WHITE).grid(row=0, column=0, sticky="w", padx=4)

        upload_btn = HRSecondaryButton(
            hdr, text="⬆  Upload File",
            command=self.upload_file,
            height=28, width=110,
            fg_color="transparent",
            border_color=HR_WHITE,
            text_color=HR_WHITE,
            hover_color=HR_NAVY_LIGHT,
        )
        upload_btn.grid(row=0, column=2, padx=10, pady=8)

        # Algorithm + length controls
        ctrl = ctk.CTkFrame(card, fg_color="transparent")
        ctrl.grid(row=1, column=0, sticky="ew", padx=14, pady=(14, 6))
        ctrl.grid_columnconfigure((1, 3), weight=1)

        ctk.CTkLabel(ctrl, text="Algorithm",
                     font=ctk.CTkFont(family="Segoe UI", size=9, weight="bold"),
                     text_color=HR_TEXT_MUTED).grid(row=0, column=0, sticky="w")

        self.algorithm_var = ctk.StringVar(value="LSA")
        algo_menu = ctk.CTkOptionMenu(
            ctrl, values=["LSA", "TextRank", "LexRank"],
            variable=self.algorithm_var,
            fg_color=HR_SURFACE, button_color=HR_BLUE,
            button_hover_color=HR_BLUE_HOVER,
            text_color=HR_TEXT_PRIMARY,
            font=ctk.CTkFont(family="Segoe UI", size=10),
            width=110, height=32,
        )
        algo_menu.grid(row=0, column=1, padx=(6, 12), sticky="ew")

        ctk.CTkLabel(ctrl, text="Length",
                     font=ctk.CTkFont(family="Segoe UI", size=9, weight="bold"),
                     text_color=HR_TEXT_MUTED).grid(row=0, column=2, sticky="w")

        self.length_var = ctk.StringVar(value="medium")
        length_menu = ctk.CTkOptionMenu(
            ctrl, values=["short", "medium", "long"],
            variable=self.length_var,
            fg_color=HR_SURFACE, button_color=HR_BLUE,
            button_hover_color=HR_BLUE_HOVER,
            text_color=HR_TEXT_PRIMARY,
            font=ctk.CTkFont(family="Segoe UI", size=10),
            width=100, height=32,
        )
        length_menu.grid(row=0, column=3, padx=(6, 0), sticky="ew")

        # Text area
        self.text_input = ctk.CTkTextbox(
            card, wrap="word",
            font=ctk.CTkFont(family="Segoe UI", size=10),
            fg_color=HR_OFF_WHITE,
            border_width=1, border_color=HR_BORDER,
            text_color=HR_TEXT_BODY,
            scrollbar_button_color=HR_BLUE,
        )
        self.text_input.grid(row=3, column=0, sticky="nsew", padx=14, pady=(0, 0))
        self.text_input.bind("<KeyRelease>", self._update_word_count)

        # Word count bar
        count_bar = ctk.CTkFrame(card, fg_color="transparent")
        count_bar.grid(row=4, column=0, sticky="ew", padx=14, pady=(4, 4))

        self.word_counter_label = ctk.CTkLabel(
            count_bar, text="Words: 0  |  Characters: 0",
            font=ctk.CTkFont(family="Segoe UI", size=9),
            text_color=HR_TEXT_MUTED,
        )
        self.word_counter_label.pack(side="left")

        # Generate button
        self.generate_btn = HRButton(
            card, text="▶   Generate Summary",
            command=self._start_summarization,
            height=38,
            font=ctk.CTkFont(family="Segoe UI", size=11, weight="bold"),
        )
        self.generate_btn.grid(row=5, column=0, sticky="ew",
                               padx=14, pady=(6, 14))

    def _build_output_panel(self, parent):
        card = HRCard(parent)
        card.grid(row=0, column=1, sticky="nsew")
        card.grid_rowconfigure(1, weight=1)
        card.grid_columnconfigure(0, weight=1)

        # Card header
        hdr = ctk.CTkFrame(card, fg_color=HR_NAVY, corner_radius=0, height=44)
        hdr.grid(row=0, column=0, sticky="ew")
        hdr.grid_propagate(False)
        hdr.grid_columnconfigure(1, weight=1)

        ctk.CTkLabel(hdr, text="  Analysis Results",
                     font=ctk.CTkFont(family="Segoe UI", size=11, weight="bold"),
                     text_color=HR_WHITE).grid(row=0, column=0, sticky="w", padx=4)

        self.summary_stats_label = ctk.CTkLabel(
            hdr, text="",
            font=ctk.CTkFont(family="Segoe UI", size=9),
            text_color=HR_TEXT_MUTED,
        )
        self.summary_stats_label.grid(row=0, column=2, padx=10)

        # Tabs
        self.tabview = ctk.CTkTabview(
            card,
            fg_color=HR_SURFACE,
            segmented_button_fg_color=HR_OFF_WHITE,
            segmented_button_selected_color=HR_BLUE,
            segmented_button_selected_hover_color=HR_BLUE_HOVER,
            segmented_button_unselected_color=HR_OFF_WHITE,
            segmented_button_unselected_hover_color=HR_BORDER,
            text_color=HR_TEXT_PRIMARY,
            text_color_disabled=HR_TEXT_MUTED,
        )
        self.tabview.grid(row=1, column=0, sticky="nsew", padx=0, pady=0)

        self._build_summary_tab(self.tabview.add("  Summary  "))
        self._build_keywords_tab(self.tabview.add("  Keywords  "))
        self._build_analysis_tab(self.tabview.add("  Analysis  "))

    def _build_summary_tab(self, parent):
        parent.grid_rowconfigure(0, weight=1)
        parent.grid_columnconfigure(0, weight=1)

        self.summary_text = ctk.CTkTextbox(
            parent, wrap="word",
            font=ctk.CTkFont(family="Segoe UI", size=11),
            fg_color=HR_OFF_WHITE,
            border_width=1, border_color=HR_BORDER,
            text_color=HR_TEXT_BODY,
        )
        self.summary_text.grid(row=0, column=0, sticky="nsew",
                               padx=14, pady=(14, 8))

        btn_row = ctk.CTkFrame(parent, fg_color="transparent")
        btn_row.grid(row=1, column=0, sticky="ew", padx=14, pady=(0, 14))

        HRSecondaryButton(btn_row, text="📋  Copy",
                          command=self._copy_summary,
                          width=90, height=32).pack(side="left", padx=(0, 8))

        HRSecondaryButton(btn_row, text="💾  Save",
                          command=self.save_summary,
                          width=90, height=32).pack(side="left")

    def _build_keywords_tab(self, parent):
        parent.grid_rowconfigure(1, weight=1)
        parent.grid_columnconfigure(0, weight=1)

        self.keywords_text = ctk.CTkTextbox(
            parent, height=70, wrap="word",
            font=ctk.CTkFont(family="Segoe UI", size=10),
            fg_color=HR_OFF_WHITE,
            border_width=1, border_color=HR_BORDER,
            text_color=HR_TEXT_BODY,
        )
        self.keywords_text.grid(row=0, column=0, sticky="ew",
                                padx=14, pady=(14, 8))

        chart_card = HRCard(parent)
        chart_card.grid(row=1, column=0, sticky="nsew", padx=14, pady=(0, 14))

        ctk.CTkLabel(chart_card, text="Keyword Frequency",
                     font=ctk.CTkFont(family="Georgia", size=12, weight="bold"),
                     text_color=HR_TEXT_PRIMARY).pack(anchor="w", padx=14, pady=(10, 4))

        self.chart_container = ctk.CTkFrame(
            chart_card, fg_color="transparent")
        self.chart_container.pack(fill="both", expand=True,
                                  padx=10, pady=(0, 10))

    def _build_analysis_tab(self, parent):
        parent.grid_rowconfigure(1, weight=1)
        parent.grid_columnconfigure(0, weight=1)

        # Stats strip
        stats_card = HRCard(parent, fg_color=HR_NAVY)
        stats_card.grid(row=0, column=0, sticky="ew", padx=14, pady=(14, 8))

        self.analysis_stats_label = ctk.CTkLabel(
            stats_card,
            text="Original: — words  |  Summary: — words  |  Reduction: —",
            font=ctk.CTkFont(family="Segoe UI", size=10),
            text_color=HR_WHITE,
        )
        self.analysis_stats_label.pack(padx=16, pady=10)

        # Highlighted text
        ctk.CTkLabel(parent, text="Highlighted Key Sentences",
                     font=ctk.CTkFont(family="Georgia", size=12, weight="bold"),
                     text_color=HR_TEXT_PRIMARY).grid(
            row=1, column=0, sticky="nw", padx=14, pady=(0, 4))

        hl_frame = ctk.CTkFrame(parent,
                                fg_color=HR_SURFACE,
                                border_width=1,
                                border_color=HR_BORDER,
                                corner_radius=6)
        hl_frame.grid(row=2, column=0, sticky="nsew", padx=14, pady=(0, 14))
        parent.grid_rowconfigure(2, weight=1)

        self.highlighted_text = scrolledtext.ScrolledText(
            hl_frame, wrap="word",
            font=("Segoe UI", 10),
            bg=HR_OFF_WHITE, fg=HR_TEXT_BODY,
            relief="flat", bd=0,
            padx=12, pady=10,
        )
        self.highlighted_text.pack(fill="both", expand=True)

    # ── History page ──────────────────────────────────────────────────────────

    def _build_history_page(self, host):
        page = ctk.CTkFrame(host, fg_color=HR_OFF_WHITE, corner_radius=0)
        page.grid(row=0, column=0, sticky="nsew")
        page.grid_rowconfigure(1, weight=1)
        page.grid_columnconfigure(0, weight=1)
        self.pages["history"] = page

        # Toolbar
        toolbar = ctk.CTkFrame(page, fg_color=HR_SURFACE,
                               corner_radius=0, height=52,
                               border_width=0)
        toolbar.grid(row=0, column=0, sticky="ew")
        toolbar.grid_propagate(False)
        toolbar.grid_columnconfigure(1, weight=1)

        ctk.CTkLabel(toolbar, text="  Summary History",
                     font=ctk.CTkFont(family="Georgia", size=14, weight="bold"),
                     text_color=HR_TEXT_PRIMARY).grid(
            row=0, column=0, padx=16, sticky="w")

        HRDangerButton(toolbar, text="🗑  Clear All",
                       command=self._clear_history,
                       width=110, height=32).grid(
            row=0, column=2, padx=16, pady=10, sticky="e")

        # Scrollable list
        self.history_frame = ctk.CTkScrollableFrame(
            page, fg_color=HR_OFF_WHITE, corner_radius=0)
        self.history_frame.grid(row=1, column=0, sticky="nsew",
                                padx=0, pady=0)

        self._load_history_items()

    # ── Page navigation ───────────────────────────────────────────────────────

    def _show_page(self, page_name):
        titles = {
            "main":    "Text Summarization",
            "history": "Summary History",
        }
        for name, page in self.pages.items():
            if name == page_name:
                page.grid()
            else:
                page.grid_remove()

        self.current_page = page_name
        if hasattr(self, "_topbar_title"):
            self._topbar_title.configure(text=titles.get(page_name, ""))

        # Highlight active nav button
        for name, btn in self._nav_buttons.items():
            btn.configure(
                fg_color=HR_NAVY_LIGHT if name == page_name else "transparent"
            )

    # ── File handling ─────────────────────────────────────────────────────────

    def upload_file(self):
        file_path = filedialog.askopenfilename(
            filetypes=[("Text files", "*.txt"), ("PDF files", "*.pdf")]
        )
        if file_path:
            self._load_file(file_path)

    def _load_file(self, file_path):
        try:
            if file_path.endswith(".txt"):
                with open(file_path, "r", encoding="utf-8") as f:
                    text = f.read()
            elif file_path.endswith(".pdf"):
                text = self.pdf_reader.extract_text(file_path)
            else:
                messagebox.showerror("Unsupported File", "Only .txt and .pdf files are supported.")
                return

            self.current_text = text
            self.text_input.delete("1.0", tk.END)
            self.text_input.insert("1.0", text)
            self._update_word_count()
            messagebox.showinfo("File Loaded",
                                f"Successfully loaded:\n{file_path.split('/')[-1]}")
        except Exception as e:
            messagebox.showerror("Load Error", f"Failed to load file:\n{str(e)}")

    # ── Word count ────────────────────────────────────────────────────────────

    def _update_word_count(self, event=None):
        text  = self.text_input.get("1.0", tk.END).strip()
        words = TextUtils.count_words(text)
        chars = TextUtils.count_characters(text)
        self.word_counter_label.configure(
            text=f"Words: {words:,}  |  Characters: {chars:,}")

    # ── Summarization ─────────────────────────────────────────────────────────

    def _start_summarization(self):
        if self.is_processing:
            return

        text = self.text_input.get("1.0", tk.END).strip()
        if not text:
            messagebox.showwarning("No Input",
                                   "Please enter or upload a document first.")
            return

        self.is_processing   = True
        self.current_text    = text
        self.generate_btn.configure(state="disabled",
                                    text="⏳  Processing…")

        thread = threading.Thread(target=self._generate_summary_thread,
                                  daemon=True)
        thread.start()

    def _generate_summary_thread(self):
        try:
            algorithm = self.algorithm_var.get().lower()
            length    = self.length_var.get()

            summary              = self.summarizer.summarize(
                self.current_text, length, algorithm)
            keywords, frequencies = self.keyword_extractor \
                .extract_keywords_with_frequencies(self.current_text)

            self.after(0, lambda: self._update_results(
                summary, keywords, frequencies, algorithm, length))

        except Exception as e:
            self.after(0, lambda: self._show_error(str(e)))
        finally:
            self.after(0, self._finish_processing)

    def _update_results(self, summary, keywords, frequencies,
                        algorithm, length):
        self.current_summary      = summary
        self.current_keywords     = keywords
        self.keyword_frequencies  = frequencies

        # Summary tab
        self.summary_text.delete("1.0", tk.END)
        self.summary_text.insert("1.0", summary)

        # Keywords tab
        self.keywords_text.delete("1.0", tk.END)
        self.keywords_text.insert("1.0", ", ".join(keywords))

        # Chart
        self.chart_generator.create_keyword_chart(
            keywords[:10], frequencies[:10], self.chart_container)

        # Analysis tab
        self._update_analysis()

        # Persist to history
        compression = TextUtils.calculate_compression_ratio(
            self.current_text, summary)
        self.history_manager.add_entry(
            self.current_text, summary, keywords,
            algorithm, length, compression)

        # Update stat cards
        history = self.history_manager.get_history()
        orig_words = TextUtils.count_words(self.current_text)
        self._stat_cards["Documents Processed"].configure(
            text=str(len(history)))
        self._stat_cards["Words Analysed"].configure(
            text=f"{orig_words:,}")
        self._stat_cards["Avg. Compression"].configure(
            text=f"{compression:.0f}%")
        self._stat_cards["Keywords Found"].configure(
            text=str(len(keywords)))

        # Topbar stats
        summ_time = UIUtils.format_time(
            TextUtils.estimate_reading_time(self.current_summary))
        self.summary_stats_label.configure(
            text=f"Reading time: {summ_time}  |  "
                 f"Compression: {UIUtils.format_percentage(compression)}")

        if self.current_page == "history":
            self._load_history_items()

    def _update_analysis(self):
        from sumy.parsers.plaintext import PlaintextParser
        from sumy.nlp.tokenizers import Tokenizer

        parser    = PlaintextParser.from_string(
            self.current_text, Tokenizer("english"))
        algorithm = self.algorithm_var.get().lower()
        summarizer_obj = self.summarizer.summarizers[algorithm]

        count_map = {"short": 2, "medium": 4, "long": 6}
        count     = count_map.get(self.length_var.get(), 4)

        summary_sentences = list(summarizer_obj(parser.document, count))
        highlighted       = TextUtils.highlight_sentences(
            self.current_text, summary_sentences)

        self.highlighted_text.delete("1.0", tk.END)
        self.highlighted_text.insert("1.0", highlighted)
        self.highlighted_text.tag_configure(
            "highlight",
            background="#D6E8FF",
            foreground=HR_NAVY,
        )

        orig_words = TextUtils.count_words(self.current_text)
        summ_words = TextUtils.count_words(self.current_summary)
        compression = TextUtils.calculate_compression_ratio(
            self.current_text, self.current_summary)
        orig_time  = UIUtils.format_time(
            TextUtils.estimate_reading_time(self.current_text))
        summ_time  = UIUtils.format_time(
            TextUtils.estimate_reading_time(self.current_summary))

        self.analysis_stats_label.configure(
            text=(f"Original: {orig_words:,} words ({orig_time})  |  "
                  f"Summary: {summ_words:,} words ({summ_time})  |  "
                  f"Reduction: {UIUtils.format_percentage(compression)}")
        )

    def _finish_processing(self):
        self.is_processing = False
        self.generate_btn.configure(state="normal",
                                    text="▶   Generate Summary")

    def _show_error(self, error_msg):
        messagebox.showerror("Processing Error",
                             f"Summarization failed:\n{error_msg}")

    # ── Actions ───────────────────────────────────────────────────────────────

    def _copy_summary(self):
        if self.current_summary:
            pyperclip.copy(self.current_summary)
            messagebox.showinfo("Copied",
                                "Summary copied to clipboard.")

    def save_summary(self):
        if not self.current_summary:
            messagebox.showwarning("Nothing to Save",
                                   "Please generate a summary first.")
            return

        file_path = filedialog.asksaveasfilename(
            defaultextension=".txt",
            filetypes=[("Text files", "*.txt")],
        )
        if not file_path:
            return
        try:
            with open(file_path, "w", encoding="utf-8") as f:
                f.write(self.current_summary)
            messagebox.showinfo("Saved", "Summary saved successfully.")
        except Exception as e:
            messagebox.showerror("Save Error",
                                 f"Failed to save file:\n{str(e)}")

    # ── History page helpers ──────────────────────────────────────────────────

    def _load_history_items(self):
        for widget in self.history_frame.winfo_children():
            widget.destroy()

        history = self.history_manager.get_history()

        if not history:
            ctk.CTkLabel(
                self.history_frame,
                text="No records yet. Generate a summary to begin.",
                font=ctk.CTkFont(family="Segoe UI", size=13),
                text_color=HR_TEXT_MUTED,
            ).pack(pady=60)
            return

        for i, entry in enumerate(history):
            self._build_history_card(i, entry)

    def _build_history_card(self, index, entry):
        card = HRCard(self.history_frame)
        card.pack(fill="x", padx=20, pady=(0, 10))
        card.grid_columnconfigure(1, weight=1)

        # Left accent bar
        accent = ctk.CTkFrame(card, fg_color=HR_BLUE,
                              width=4, corner_radius=0)
        accent.grid(row=0, column=0, rowspan=3, sticky="ns",
                    padx=(0, 0), pady=0)

        # Header row
        hdr = ctk.CTkFrame(card, fg_color="transparent")
        hdr.grid(row=0, column=1, sticky="ew", padx=14, pady=(12, 4))
        hdr.grid_columnconfigure(3, weight=1)

        timestamp = entry["timestamp"][:19].replace("T", "  ")
        ctk.CTkLabel(hdr, text=timestamp,
                     font=ctk.CTkFont(family="Segoe UI", size=9, weight="bold"),
                     text_color=HR_TEXT_MUTED).grid(
            row=0, column=0, sticky="w")

        StatusBadge(hdr, entry["algorithm"], colour="blue").grid(
            row=0, column=1, padx=8)
        StatusBadge(hdr, entry["length"], colour="gold").grid(
            row=0, column=2)

        compression_lbl = ctk.CTkLabel(
            hdr,
            text=f"{entry['compression_ratio']:.1f}% reduction",
            font=ctk.CTkFont(family="Segoe UI", size=9),
            text_color=HR_SUCCESS,
        )
        compression_lbl.grid(row=0, column=3, sticky="e")

        # Action buttons
        btn_row = ctk.CTkFrame(hdr, fg_color="transparent")
        btn_row.grid(row=0, column=4, padx=(12, 0))

        HRSecondaryButton(btn_row, text="Load",
                          command=lambda e=entry: self._load_history_entry(e),
                          width=60, height=26).pack(side="left", padx=(0, 6))

        HRDangerButton(btn_row, text="✕",
                       command=lambda idx=index: self._delete_history_entry(idx),
                       width=30, height=26).pack(side="left")

        # Summary preview
        preview = (entry["summary"][:220] + "…"
                   if len(entry["summary"]) > 220 else entry["summary"])
        ctk.CTkLabel(
            card, text=preview,
            wraplength=700,
            justify="left",
            font=ctk.CTkFont(family="Segoe UI", size=10),
            text_color=HR_TEXT_BODY,
        ).grid(row=1, column=1, sticky="w", padx=14, pady=(0, 12))

    def _load_history_entry(self, entry):
        self.current_text = entry["original_text"]
        self.text_input.delete("1.0", tk.END)
        self.text_input.insert("1.0", self.current_text)
        self._update_word_count()
        self._show_page("main")
        self.algorithm_var.set(entry["algorithm"])
        self.length_var.set(entry["length"])
        self._update_results(
            entry["summary"],
            entry["keywords"],
            [],
            entry["algorithm"],
            entry["length"],
        )

    def _delete_history_entry(self, index):
        self.history_manager.delete_entry(index)
        self._load_history_items()

    def _clear_history(self):
        if messagebox.askyesno("Confirm",
                               "Delete all history records?"):
            self.history_manager.clear_history()
            self._load_history_items()
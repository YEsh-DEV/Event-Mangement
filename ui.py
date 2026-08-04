import os
import tkinter as tk
from tkinter import ttk, messagebox
from datetime import datetime
import customtkinter as ctk

# Matplotlib integration for Tkinter/CustomTkinter
import matplotlib
matplotlib.use("TkAgg")
import matplotlib.pyplot as plt
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg

from utils import init_sample_data
from events import (
    get_all_events, add_event, delete_event, get_event_titles
)
from registration import (
    get_all_participants, register_participant, search_participants,
    delete_participant, get_event_enrollment_count
)
from payments import (
    record_payment, get_payment_summary
)
from attendance import (
    mark_attendance, get_attendance_summary
)
from analytics import (
    generate_full_analytics, get_random_insight
)
from reports import (
    generate_text_report, export_participants_csv, list_report_files, read_report_file
)

# ---------------------------------------------------------
# DESIGN SYSTEM & COLOR PALETTE (WARM BROWN & BRONZE THEME)
# ---------------------------------------------------------
BG_MAIN = "#1C1917"          # Deep Warm Espresso
BG_NAV = "#181513"           # Dark Espresso Top Navigation Bar
COLOR_CARD = "#292524"         # Dark Mocha / Warm Stone Surface
COLOR_CARD_HOVER = "#383431"   # Elevated Mocha Surface
COLOR_ACCENT = "#D97706"       # Warm Bronze Accent
COLOR_ACCENT_HOVER = "#B45309" # Deep Bronze Hover
COLOR_GOLD = "#F59E0B"         # Golden Amber Highlight
COLOR_TEXT_MAIN = "#F5F5F4"    # Warm White Text
COLOR_TEXT_MUTED = "#A8A29E"   # Light Warm Gray Text
COLOR_BORDER = "#44403C"       # Warm Stone Border
COLOR_SUCCESS = "#10B981"      # Emerald Green
COLOR_WARNING = "#F59E0B"      # Amber Yellow
COLOR_DANGER = "#EF4444"       # Coral Red
COLOR_PURPLE = "#8B5CF6"       # Soft Violet Accent

FONT_FAMILY = "Segoe UI"

# Set CustomTkinter Appearance
ctk.set_appearance_mode("Dark")
ctk.set_default_color_theme("blue")


# ---------------------------------------------------------
# REUSABLE KPI CARD COMPONENT
# ---------------------------------------------------------
class KPICard(ctk.CTkFrame):
    """
    Reusable KPI Metric Card Widget.
    Displays icon, metric title, primary value, and progress indicator.
    """
    def __init__(self, parent, title, value, icon="📊", subtitle="", progress=None, accent_color=COLOR_ACCENT):
        super().__init__(parent, fg_color=COLOR_CARD, corner_radius=12, border_width=1, border_color=COLOR_BORDER)
        
        # Top Row: Title + Icon
        top_frame = ctk.CTkFrame(self, fg_color="transparent")
        top_frame.pack(fill="x", padx=16, pady=(12, 4))
        
        ctk.CTkLabel(
            top_frame, text=title.upper(),
            font=ctk.CTkFont(family=FONT_FAMILY, size=11, weight="bold"),
            text_color=COLOR_TEXT_MUTED
        ).pack(side="left")
        
        ctk.CTkLabel(
            top_frame, text=icon,
            font=ctk.CTkFont(size=16)
        ).pack(side="right")

        # Numeric Value
        ctk.CTkLabel(
            self, text=value,
            font=ctk.CTkFont(family=FONT_FAMILY, size=22, weight="bold"),
            text_color=accent_color
        ).pack(anchor="w", padx=16, pady=(2, 4))

        # Progress Bar (optional)
        if progress is not None:
            pb = ctk.CTkProgressBar(self, height=6, progress_color=accent_color, fg_color=COLOR_CARD_HOVER)
            pb.set(max(0.0, min(1.0, progress)))
            pb.pack(fill="x", padx=16, pady=(4, 6))

        # Subtitle
        if subtitle:
            ctk.CTkLabel(
                self, text=subtitle,
                font=ctk.CTkFont(family=FONT_FAMILY, size=11),
                text_color=COLOR_TEXT_MUTED
            ).pack(anchor="w", padx=16, pady=(0, 12))
        else:
            ctk.CTkFrame(self, height=8, fg_color="transparent").pack()


# ---------------------------------------------------------
# MATPLOTLIB CHART EMBEDDER HELPER
# ---------------------------------------------------------
class ChartWidget(ctk.CTkFrame):
    """
    CustomTkinter Frame embedding a Matplotlib graphical chart.
    Cleanly handles figure creation, dark mocha styling, and canvas rendering.
    """
    def __init__(self, parent, title="Graphical Chart"):
        super().__init__(parent, fg_color=COLOR_CARD, corner_radius=12, border_width=1, border_color=COLOR_BORDER)
        self.title = title
        
        # Header Label
        ctk.CTkLabel(
            self, text=self.title,
            font=ctk.CTkFont(family=FONT_FAMILY, size=14, weight="bold"),
            text_color=COLOR_TEXT_MAIN
        ).pack(anchor="w", padx=16, pady=(12, 4))
        
        self.canvas_frame = ctk.CTkFrame(self, fg_color="transparent")
        self.canvas_frame.pack(fill="both", expand=True, padx=8, pady=(0, 8))
        self.canvas = None
        self.fig = None

    def plot_donut_chart(self, labels, values, colors=None):
        """Generates a stylish Donut/Pie chart."""
        self.clear_chart()
        if not values or sum(values) == 0:
            labels = ["No Data"]
            values = [1]
            colors = [COLOR_CARD_HOVER]

        if colors is None:
            colors = [COLOR_ACCENT, COLOR_GOLD, COLOR_SUCCESS, COLOR_PURPLE, COLOR_DANGER]

        self.fig, ax = plt.subplots(figsize=(4.2, 2.6), facecolor=COLOR_CARD)
        ax.set_facecolor(COLOR_CARD)

        wedges, texts, autotexts = ax.pie(
            values,
            labels=labels,
            autopct="%1.0f%%" if sum(values) > 1 else "",
            startangle=140,
            colors=colors[:len(labels)],
            textprops=dict(color=COLOR_TEXT_MAIN, fontsize=9, fontfamily="sans-serif"),
            wedgeprops=dict(width=0.4, edgecolor=COLOR_CARD, linewidth=2)
        )
        for at in autotexts:
            at.set_color(COLOR_TEXT_MAIN)
            at.set_fontsize(9)
            at.set_weight("bold")

        ax.axis("equal")
        plt.tight_layout()

        self.canvas = FigureCanvasTkAgg(self.fig, master=self.canvas_frame)
        self.canvas.draw()
        self.canvas.get_tk_widget().pack(fill="both", expand=True)

    def plot_bar_chart(self, categories, values, colors=None):
        """Generates a stylish Bar Graph."""
        self.clear_chart()
        if not values:
            categories = ["No Data"]
            values = [0]

        if colors is None:
            colors = COLOR_ACCENT

        self.fig, ax = plt.subplots(figsize=(4.5, 2.6), facecolor=COLOR_CARD)
        ax.set_facecolor(COLOR_CARD)

        # Truncate category names if too long
        short_labels = [c[:12] + ".." if len(c) > 14 else c for c in categories]

        bars = ax.bar(short_labels, values, color=colors, width=0.5, edgecolor=COLOR_BORDER)
        
        ax.tick_params(colors=COLOR_TEXT_MUTED, labelsize=8)
        ax.spines['top'].set_visible(False)
        ax.spines['right'].set_visible(False)
        ax.spines['left'].set_color(COLOR_BORDER)
        ax.spines['bottom'].set_color(COLOR_BORDER)
        ax.grid(axis='y', linestyle='--', alpha=0.3, color=COLOR_BORDER)

        for bar in bars:
            yval = bar.get_height()
            ax.text(bar.get_x() + bar.get_width()/2.0, yval + 0.1, f"${yval:.0f}" if yval > 0 else "0", ha='center', va='bottom', color=COLOR_TEXT_MAIN, fontsize=8, fontweight='bold')

        plt.tight_layout()

        self.canvas = FigureCanvasTkAgg(self.fig, master=self.canvas_frame)
        self.canvas.draw()
        self.canvas.get_tk_widget().pack(fill="both", expand=True)

    def clear_chart(self):
        if self.canvas:
            self.canvas.get_tk_widget().destroy()
            self.canvas = None
        if self.fig:
            plt.close(self.fig)
            self.fig = None


# ---------------------------------------------------------
# MAIN APPLICATION CLASS
# ---------------------------------------------------------
class EventManagementApp(ctk.CTk):
    """
    Main Application Window Class.
    Features a modern TOP NAVIGATION BAR layout and Matplotlib graphical chart widgets.
    """
    def __init__(self):
        super().__init__()

        # Initialize sample data if needed
        init_sample_data()

        # Window Setup
        self.title("Event Management System - Desktop Course Project")
        self.geometry("1200x780")
        self.minsize(1050, 700)
        self.configure(fg_color=BG_MAIN)

        # Configure Grid Layout (Row 0: Top Navbar, Row 1: Main Container)
        self.grid_rowconfigure(0, weight=0)  # Fixed Top Navbar
        self.grid_rowconfigure(1, weight=1)  # Expandable Main Content
        self.grid_columnconfigure(0, weight=1)

        # Navigation State
        self.active_nav_key = None
        self.nav_buttons = {}

        # Build UI Structure
        self.setup_styles()
        self.create_top_navbar()
        self.create_main_container()

        # Load Default Dashboard View
        self.nav_to("dashboard")

    def setup_styles(self):
        """Configures ttk Treeview style to match Warm Brown theme."""
        style = ttk.Style()
        style.theme_use("default")
        style.configure(
            "Treeview",
            background=COLOR_CARD,
            foreground=COLOR_TEXT_MAIN,
            fieldbackground=COLOR_CARD,
            bordercolor=COLOR_BORDER,
            borderwidth=0,
            rowheight=32,
            font=(FONT_FAMILY, 10)
        )
        style.configure(
            "Treeview.Heading",
            background=COLOR_CARD_HOVER,
            foreground=COLOR_TEXT_MAIN,
            bordercolor=COLOR_BORDER,
            borderwidth=1,
            relief="flat",
            font=(FONT_FAMILY, 10, "bold")
        )
        style.map(
            "Treeview",
            background=[("selected", COLOR_ACCENT)],
            foreground=[("selected", COLOR_TEXT_MAIN)]
        )

    # ---------------------------------------------------------
    # TOP NAVIGATION BAR (SHIFTED LAYOUT)
    # ---------------------------------------------------------
    def create_top_navbar(self):
        self.top_nav = ctk.CTkFrame(self, fg_color=BG_NAV, corner_radius=0, height=65, border_width=1, border_color=COLOR_BORDER)
        self.top_nav.grid(row=0, column=0, sticky="ew")
        self.top_nav.pack_propagate(False)

        # Left: Brand Logo & Title
        brand_frame = ctk.CTkFrame(self.top_nav, fg_color="transparent")
        brand_frame.pack(side="left", padx=20, pady=10)

        ctk.CTkLabel(
            brand_frame, text="🤎 EventManager",
            font=ctk.CTkFont(family=FONT_FAMILY, size=18, weight="bold"),
            text_color=COLOR_GOLD
        ).pack(side="left")

        ctk.CTkLabel(
            brand_frame, text=" | Desktop Edition",
            font=ctk.CTkFont(family=FONT_FAMILY, size=11),
            text_color=COLOR_TEXT_MUTED
        ).pack(side="left", padx=(4, 0))

        # Center: Navigation Pill Buttons
        nav_center = ctk.CTkFrame(self.top_nav, fg_color="transparent")
        nav_center.pack(side="left", expand=True, pady=10)

        nav_items = [
            ("dashboard", "📊 Dashboard"),
            ("events", "📅 Events"),
            ("registration", "📝 Registration"),
            ("payments", "💳 Payments"),
            ("attendance", "📋 Attendance"),
            ("analytics", "📈 Analytics"),
            ("reports", "📄 Reports"),
        ]

        for key, label in nav_items:
            btn = ctk.CTkButton(
                nav_center,
                text=label,
                font=ctk.CTkFont(family=FONT_FAMILY, size=12, weight="bold"),
                fg_color="transparent",
                text_color=COLOR_TEXT_MUTED,
                hover_color=COLOR_CARD_HOVER,
                corner_radius=20,
                height=36,
                width=110,
                command=lambda k=key: self.nav_to(k)
            )
            btn.pack(side="left", padx=3)
            self.nav_buttons[key] = btn

        # Right: Clock & User Chip
        right_frame = ctk.CTkFrame(self.top_nav, fg_color="transparent")
        right_frame.pack(side="right", padx=20, pady=10)

        # Clock
        self.time_label = ctk.CTkLabel(
            right_frame, text="",
            font=ctk.CTkFont(family=FONT_FAMILY, size=11),
            text_color=COLOR_TEXT_MUTED
        )
        self.time_label.pack(side="left", padx=10)
        self.update_clock()

        # User Badge Chip
        badge = ctk.CTkFrame(right_frame, fg_color=COLOR_CARD_HOVER, corner_radius=20, border_width=1, border_color=COLOR_BORDER)
        badge.pack(side="left", padx=(5, 0))

        ctk.CTkLabel(
            badge, text="👤 Admin",
            font=ctk.CTkFont(family=FONT_FAMILY, size=11, weight="bold"),
            text_color=COLOR_GOLD
        ).pack(padx=12, pady=4)

    def update_clock(self):
        now = datetime.now().strftime("📅 %a, %b %d  ⏰ %H:%M")
        self.time_label.configure(text=now)
        self.after(30000, self.update_clock)

    def nav_to(self, key):
        """Switches views and updates top navbar active button style."""
        for k, btn in self.nav_buttons.items():
            if k == key:
                btn.configure(fg_color=COLOR_ACCENT, text_color=COLOR_TEXT_MAIN)
            else:
                btn.configure(fg_color="transparent", text_color=COLOR_TEXT_MUTED)

        self.clear_main_container()

        view_map = {
            "dashboard": self.render_dashboard,
            "events": self.render_events,
            "registration": self.render_registration,
            "payments": self.render_payments,
            "attendance": self.render_attendance,
            "analytics": self.render_analytics,
            "reports": self.render_reports
        }
        if key in view_map:
            view_map[key]()

    def create_main_container(self):
        self.main_container = ctk.CTkFrame(self, fg_color="transparent")
        self.main_container.grid(row=1, column=0, sticky="nsew", padx=18, pady=16)
        self.main_container.grid_rowconfigure(0, weight=1)
        self.main_container.grid_columnconfigure(0, weight=1)

    def clear_main_container(self):
        plt.close('all')  # Close matplotlib figures
        for child in self.main_container.winfo_children():
            child.destroy()

    # ---------------------------------------------------------
    # VIEW 1: DASHBOARD (WITH GRAPHICAL PLOTS)
    # ---------------------------------------------------------
    def render_dashboard(self):
        analytics = generate_full_analytics()

        scroll = ctk.CTkScrollableFrame(self.main_container, fg_color="transparent")
        scroll.pack(fill="both", expand=True)

        # Section Subheader
        sub_hdr = ctk.CTkFrame(scroll, fg_color="transparent")
        sub_hdr.pack(fill="x", pady=(0, 14))

        ctk.CTkLabel(sub_hdr, text="Dashboard Overview", font=ctk.CTkFont(family=FONT_FAMILY, size=20, weight="bold"), text_color=COLOR_TEXT_MAIN).pack(side="left")
        ctk.CTkLabel(sub_hdr, text="Real-time event metrics & visual chart analytics", font=ctk.CTkFont(family=FONT_FAMILY, size=12), text_color=COLOR_TEXT_MUTED).pack(side="left", padx=12, pady=(4, 0))

        # KPI Cards Row
        kpi_row = ctk.CTkFrame(scroll, fg_color="transparent")
        kpi_row.pack(fill="x", pady=(0, 16))
        kpi_row.grid_columnconfigure((0, 1, 2, 3), weight=1)

        c1 = KPICard(kpi_row, "Total Events", str(analytics["total_events"]), icon="📅", subtitle="Active Scheduled", accent_color=COLOR_GOLD)
        c1.grid(row=0, column=0, padx=6, sticky="ew")

        c2 = KPICard(kpi_row, "Participants", str(analytics["total_participants"]), icon="👥", subtitle=f"Occupancy {analytics['occupancy_rate']:.1f}%", progress=analytics['occupancy_rate']/100.0, accent_color=COLOR_ACCENT)
        c2.grid(row=0, column=1, padx=6, sticky="ew")

        c3 = KPICard(kpi_row, "Revenue Collected", f"${analytics['total_revenue_collected']:.2f}", icon="💰", subtitle=f"Collection {analytics['collection_rate']:.1f}%", progress=analytics['collection_rate']/100.0, accent_color=COLOR_SUCCESS)
        c3.grid(row=0, column=2, padx=6, sticky="ew")

        c4 = KPICard(kpi_row, "Outstanding Dues", f"${analytics['outstanding_dues']:.2f}", icon="⏳", subtitle=f"{analytics['payment_counts']['Pending']} Pending Payments", accent_color=COLOR_DANGER)
        c4.grid(row=0, column=3, padx=6, sticky="ew")

        # GRAPHICAL PLOTS ROW (MATPLOTLIB CHARTS)
        charts_row = ctk.CTkFrame(scroll, fg_color="transparent")
        charts_row.pack(fill="x", pady=(0, 16))
        charts_row.grid_columnconfigure(0, weight=1)
        charts_row.grid_columnconfigure(1, weight=1)

        # Chart 1: Donut Chart for Categories
        cat_chart = ChartWidget(charts_row, title="🍩 Registrations by Event Category")
        cat_chart.grid(row=0, column=0, padx=(0, 8), sticky="nsew")

        cat_labels = list(analytics["category_counts"].keys())
        cat_vals = list(analytics["category_counts"].values())
        cat_chart.plot_donut_chart(cat_labels, cat_vals, colors=[COLOR_ACCENT, COLOR_GOLD, COLOR_SUCCESS, COLOR_PURPLE, COLOR_DANGER])

        # Chart 2: Revenue Bar Graph
        rev_chart = ChartWidget(charts_row, title="📊 Revenue Collection per Event ($)")
        rev_chart.grid(row=0, column=1, padx=(8, 0), sticky="nsew")

        events = get_all_events()
        participants = get_all_participants()
        evt_rev = {}
        for p in participants:
            title = p.get("event", "Unknown")
            evt_rev[title] = evt_rev.get(title, 0.0) + p.get("amount_paid", 0.0)

        evt_labels = list(evt_rev.keys()) or [e["title"] for e in events]
        evt_vals = [evt_rev.get(t, 0.0) for t in evt_labels] or [0]
        rev_chart.plot_bar_chart(evt_labels, evt_vals, colors=COLOR_ACCENT)

        # Highlights & Insights Row
        body = ctk.CTkFrame(scroll, fg_color="transparent")
        body.pack(fill="x", pady=(0, 16))
        body.grid_columnconfigure(0, weight=3)
        body.grid_columnconfigure(1, weight=2)

        # Left: Executive Highlights
        left_col = ctk.CTkFrame(body, fg_color=COLOR_CARD, corner_radius=12, border_width=1, border_color=COLOR_BORDER)
        left_col.grid(row=0, column=0, padx=(0, 8), sticky="nsew")

        ctk.CTkLabel(left_col, text="📈 Performance Highlights", font=ctk.CTkFont(family=FONT_FAMILY, size=15, weight="bold"), text_color=COLOR_TEXT_MAIN).pack(anchor="w", padx=18, pady=(14, 10))

        info_text = (
            f"🏆 Most Popular Event:   {analytics['most_popular_event']} ({analytics['most_popular_count']} participants)\n"
            f"💵 Top Revenue Event:    {analytics['top_revenue_event']} (${analytics['top_revenue_amount']:.2f} earned)\n"
            f"🏟️ Venue Capacity Used: {analytics['total_participants']} of {analytics['total_capacity']} available seats\n"
            f"💳 Collection Rate:      {analytics['collection_rate']:.1f}% of overall expected tuition/fees"
        )
        ctk.CTkLabel(left_col, text=info_text, font=ctk.CTkFont(family=FONT_FAMILY, size=12), text_color=COLOR_TEXT_MAIN, justify="left").pack(anchor="w", padx=18, pady=(0, 14))

        # Right: Quick Actions & Management Tip
        right_col = ctk.CTkFrame(body, fg_color=COLOR_CARD, corner_radius=12, border_width=1, border_color=COLOR_BORDER)
        right_col.grid(row=0, column=1, padx=(8, 0), sticky="nsew")

        ctk.CTkLabel(right_col, text="💡 Event Insight Tip", font=ctk.CTkFont(family=FONT_FAMILY, size=14, weight="bold"), text_color=COLOR_GOLD).pack(anchor="w", padx=18, pady=(14, 6))

        tip_lbl = ctk.CTkLabel(right_col, text=analytics["random_insight"], font=ctk.CTkFont(family=FONT_FAMILY, size=12), text_color=COLOR_TEXT_MAIN, wraplength=280, justify="left")
        tip_lbl.pack(anchor="w", padx=18, pady=(0, 12))

    # ---------------------------------------------------------
    # VIEW 2: EVENTS MANAGEMENT
    # ---------------------------------------------------------
    def render_events(self):
        sub_hdr = ctk.CTkFrame(self.main_container, fg_color="transparent")
        sub_hdr.pack(fill="x", pady=(0, 14))
        ctk.CTkLabel(sub_hdr, text="Event Management", font=ctk.CTkFont(family=FONT_FAMILY, size=20, weight="bold"), text_color=COLOR_TEXT_MAIN).pack(side="left")

        body = ctk.CTkFrame(self.main_container, fg_color="transparent")
        body.pack(fill="both", expand=True)
        body.grid_columnconfigure(0, weight=2)
        body.grid_columnconfigure(1, weight=3)
        body.grid_rowconfigure(0, weight=1)

        # Form Column
        form_card = ctk.CTkFrame(body, fg_color=COLOR_CARD, corner_radius=12, border_width=1, border_color=COLOR_BORDER)
        form_card.grid(row=0, column=0, padx=(0, 8), sticky="nsew")

        ctk.CTkLabel(form_card, text="Add New Event", font=ctk.CTkFont(family=FONT_FAMILY, size=16, weight="bold"), text_color=COLOR_TEXT_MAIN).pack(anchor="w", padx=18, pady=(16, 12))

        title_e = ctk.CTkEntry(form_card, placeholder_text="Event Title (e.g. AI Tech Summit)", fg_color=COLOR_CARD_HOVER, border_color=COLOR_BORDER)
        title_e.pack(fill="x", padx=18, pady=6)

        cat_m = ctk.CTkOptionMenu(form_card, values=["Technology", "Workshop", "Seminar", "Competition", "Cultural"], fg_color=COLOR_CARD_HOVER, button_color=COLOR_ACCENT)
        cat_m.pack(fill="x", padx=18, pady=6)

        date_e = ctk.CTkEntry(form_card, placeholder_text="Date (YYYY-MM-DD)", fg_color=COLOR_CARD_HOVER, border_color=COLOR_BORDER)
        date_e.pack(fill="x", padx=18, pady=6)

        time_e = ctk.CTkEntry(form_card, placeholder_text="Time (e.g. 10:00 AM)", fg_color=COLOR_CARD_HOVER, border_color=COLOR_BORDER)
        time_e.pack(fill="x", padx=18, pady=6)

        venue_e = ctk.CTkEntry(form_card, placeholder_text="Venue (e.g. Auditorium Hall)", fg_color=COLOR_CARD_HOVER, border_color=COLOR_BORDER)
        venue_e.pack(fill="x", padx=18, pady=6)

        cap_e = ctk.CTkEntry(form_card, placeholder_text="Max Capacity (e.g. 50)", fg_color=COLOR_CARD_HOVER, border_color=COLOR_BORDER)
        cap_e.pack(fill="x", padx=18, pady=6)

        fee_e = ctk.CTkEntry(form_card, placeholder_text="Registration Fee ($)", fg_color=COLOR_CARD_HOVER, border_color=COLOR_BORDER)
        fee_e.pack(fill="x", padx=18, pady=6)

        def add_handler():
            ok, msg = add_event(title_e.get(), cat_m.get(), date_e.get(), time_e.get(), venue_e.get(), cap_e.get(), fee_e.get())
            if ok:
                messagebox.showinfo("Success", msg)
                self.render_events()
            else:
                messagebox.showerror("Error", msg)

        ctk.CTkButton(form_card, text="Create Event", fg_color=COLOR_ACCENT, hover_color=COLOR_ACCENT_HOVER, font=ctk.CTkFont(family=FONT_FAMILY, size=13, weight="bold"), command=add_handler).pack(fill="x", padx=18, pady=(16, 18))

        # Table Column
        table_card = ctk.CTkFrame(body, fg_color=COLOR_CARD, corner_radius=12, border_width=1, border_color=COLOR_BORDER)
        table_card.grid(row=0, column=1, padx=(8, 0), sticky="nsew")

        ctk.CTkLabel(table_card, text="Scheduled Events List", font=ctk.CTkFont(family=FONT_FAMILY, size=16, weight="bold"), text_color=COLOR_TEXT_MAIN).pack(anchor="w", padx=18, pady=(16, 12))

        cols = ("ID", "Title", "Category", "Venue", "Seats", "Fee")
        tree = ttk.Treeview(table_card, columns=cols, show="headings", height=12)
        for col in cols:
            tree.heading(col, text=col)
            tree.column(col, width=80 if col not in ["Title", "Venue"] else 130, anchor="center")

        tree.pack(fill="both", expand=True, padx=16, pady=(0, 10))

        for evt in get_all_events():
            enrolled = get_event_enrollment_count(evt["title"])
            tree.insert("", "end", values=(
                evt["id"], evt["title"], evt["category"], evt["venue"], f"{enrolled}/{evt['capacity']}", f"${evt['fee']:.2f}"
            ))

        def delete_handler():
            sel = tree.selection()
            if not sel:
                messagebox.showwarning("Warning", "Select an event to delete.")
                return
            evt_id = tree.item(sel[0])["values"][0]
            if messagebox.askyesno("Confirm Delete", f"Delete Event ID {evt_id}?"):
                d_ok, d_msg = delete_event(evt_id)
                if d_ok:
                    messagebox.showinfo("Deleted", d_msg)
                    self.render_events()
                else:
                    messagebox.showerror("Error", d_msg)

        ctk.CTkButton(table_card, text="Delete Selected Event", fg_color=COLOR_DANGER, hover_color="#C0392B", command=delete_handler).pack(anchor="e", padx=16, pady=12)

    # ---------------------------------------------------------
    # VIEW 3: REGISTRATION
    # ---------------------------------------------------------
    def render_registration(self):
        sub_hdr = ctk.CTkFrame(self.main_container, fg_color="transparent")
        sub_hdr.pack(fill="x", pady=(0, 14))
        ctk.CTkLabel(sub_hdr, text="Participant Registration", font=ctk.CTkFont(family=FONT_FAMILY, size=20, weight="bold"), text_color=COLOR_TEXT_MAIN).pack(side="left")

        body = ctk.CTkFrame(self.main_container, fg_color="transparent")
        body.pack(fill="both", expand=True)
        body.grid_columnconfigure(0, weight=2)
        body.grid_columnconfigure(1, weight=3)
        body.grid_rowconfigure(0, weight=1)

        # Form Card
        form_card = ctk.CTkFrame(body, fg_color=COLOR_CARD, corner_radius=12, border_width=1, border_color=COLOR_BORDER)
        form_card.grid(row=0, column=0, padx=(0, 8), sticky="nsew")

        ctk.CTkLabel(form_card, text="Register Attendee", font=ctk.CTkFont(family=FONT_FAMILY, size=16, weight="bold"), text_color=COLOR_TEXT_MAIN).pack(anchor="w", padx=18, pady=(16, 12))

        name_e = ctk.CTkEntry(form_card, placeholder_text="Full Name", fg_color=COLOR_CARD_HOVER, border_color=COLOR_BORDER)
        name_e.pack(fill="x", padx=18, pady=5)

        age_e = ctk.CTkEntry(form_card, placeholder_text="Age (e.g. 21)", fg_color=COLOR_CARD_HOVER, border_color=COLOR_BORDER)
        age_e.pack(fill="x", padx=18, pady=5)

        gender_m = ctk.CTkOptionMenu(form_card, values=["Male", "Female", "Other"], fg_color=COLOR_CARD_HOVER, button_color=COLOR_ACCENT)
        gender_m.pack(fill="x", padx=18, pady=5)

        org_e = ctk.CTkEntry(form_card, placeholder_text="College / Organization", fg_color=COLOR_CARD_HOVER, border_color=COLOR_BORDER)
        org_e.pack(fill="x", padx=18, pady=5)

        phone_e = ctk.CTkEntry(form_card, placeholder_text="Phone Number", fg_color=COLOR_CARD_HOVER, border_color=COLOR_BORDER)
        phone_e.pack(fill="x", padx=18, pady=5)

        email_e = ctk.CTkEntry(form_card, placeholder_text="Email Address", fg_color=COLOR_CARD_HOVER, border_color=COLOR_BORDER)
        email_e.pack(fill="x", padx=18, pady=5)

        titles = get_event_titles() or ["No Events"]
        evt_m = ctk.CTkOptionMenu(form_card, values=titles, fg_color=COLOR_CARD_HOVER, button_color=COLOR_ACCENT)
        evt_m.pack(fill="x", padx=18, pady=5)

        def reg_sub():
            r_ok, r_msg = register_participant(name_e.get(), age_e.get(), gender_m.get(), org_e.get(), phone_e.get(), email_e.get(), evt_m.get())
            if r_ok:
                messagebox.showinfo("Success", r_msg)
                self.render_registration()
            else:
                messagebox.showerror("Error", r_msg)

        ctk.CTkButton(form_card, text="Complete Registration", fg_color=COLOR_ACCENT, hover_color=COLOR_ACCENT_HOVER, font=ctk.CTkFont(family=FONT_FAMILY, size=13, weight="bold"), command=reg_sub).pack(fill="x", padx=18, pady=(14, 16))

        # Right: Roster & Search
        table_card = ctk.CTkFrame(body, fg_color=COLOR_CARD, corner_radius=12, border_width=1, border_color=COLOR_BORDER)
        table_card.grid(row=0, column=1, padx=(8, 0), sticky="nsew")

        search_f = ctk.CTkFrame(table_card, fg_color="transparent")
        search_f.pack(fill="x", padx=16, pady=14)

        search_e = ctk.CTkEntry(search_f, placeholder_text="🔍 Search Name, Reg ID, or Event...", fg_color=COLOR_CARD_HOVER, border_color=COLOR_BORDER)
        search_e.pack(side="left", fill="x", expand=True, padx=(0, 8))

        def refresh_grid(q=""):
            for row in tree.get_children():
                tree.delete(row)
            for p in search_participants(q):
                tree.insert("", "end", values=(p["reg_id"], p["name"], p["event"], p["phone"], p["payment_status"]))

        ctk.CTkButton(search_f, text="Search", width=80, fg_color=COLOR_ACCENT, hover_color=COLOR_ACCENT_HOVER, command=lambda: refresh_grid(search_e.get())).pack(side="right")

        cols = ("Reg ID", "Name", "Event", "Phone", "Payment Status")
        tree = ttk.Treeview(table_card, columns=cols, show="headings", height=12)
        for col in cols:
            tree.heading(col, text=col)
            tree.column(col, width=100 if col not in ["Name", "Event"] else 130, anchor="center")

        tree.pack(fill="both", expand=True, padx=16, pady=(0, 10))
        refresh_grid()

        def del_sub():
            sel = tree.selection()
            if not sel:
                messagebox.showwarning("Warning", "Select a participant to delete.")
                return
            reg_id = tree.item(sel[0])["values"][0]
            if messagebox.askyesno("Confirm Delete", f"Delete Participant {reg_id}?"):
                d_ok, d_msg = delete_participant(reg_id)
                if d_ok:
                    messagebox.showinfo("Deleted", d_msg)
                    self.render_registration()
                else:
                    messagebox.showerror("Error", d_msg)

        ctk.CTkButton(table_card, text="Delete Selected", fg_color=COLOR_DANGER, hover_color="#C0392B", command=del_sub).pack(anchor="e", padx=16, pady=12)

    # ---------------------------------------------------------
    # VIEW 4: PAYMENTS TRACKING
    # ---------------------------------------------------------
    def render_payments(self):
        sub_hdr = ctk.CTkFrame(self.main_container, fg_color="transparent")
        sub_hdr.pack(fill="x", pady=(0, 14))
        ctk.CTkLabel(sub_hdr, text="Payment Tracking", font=ctk.CTkFont(family=FONT_FAMILY, size=20, weight="bold"), text_color=COLOR_TEXT_MAIN).pack(side="left")

        summary = get_payment_summary()

        strip = ctk.CTkFrame(self.main_container, fg_color=COLOR_CARD, corner_radius=12, border_width=1, border_color=COLOR_BORDER)
        strip.pack(fill="x", pady=(0, 16))

        info = (
            f"💵 Expected: ${summary['total_fee_expected']:.2f}    |    "
            f"✅ Collected: ${summary['total_collected']:.2f}    |    "
            f"⏳ Outstanding Dues: ${summary['outstanding_dues']:.2f}    |    "
            f"📊 Rate: {summary['collection_rate']:.1f}%"
        )
        ctk.CTkLabel(strip, text=info, font=ctk.CTkFont(family=FONT_FAMILY, size=13, weight="bold"), text_color=COLOR_GOLD).pack(padx=20, pady=12)

        body = ctk.CTkFrame(self.main_container, fg_color="transparent")
        body.pack(fill="both", expand=True)
        body.grid_columnconfigure(0, weight=2)
        body.grid_columnconfigure(1, weight=3)
        body.grid_rowconfigure(0, weight=1)

        form_card = ctk.CTkFrame(body, fg_color=COLOR_CARD, corner_radius=12, border_width=1, border_color=COLOR_BORDER)
        form_card.grid(row=0, column=0, padx=(0, 8), sticky="nsew")

        ctk.CTkLabel(form_card, text="Record Payment", font=ctk.CTkFont(family=FONT_FAMILY, size=16, weight="bold"), text_color=COLOR_TEXT_MAIN).pack(anchor="w", padx=18, pady=(16, 12))

        reg_e = ctk.CTkEntry(form_card, placeholder_text="Registration ID (e.g. REG-2026-1001)", fg_color=COLOR_CARD_HOVER, border_color=COLOR_BORDER)
        reg_e.pack(fill="x", padx=18, pady=8)

        amt_e = ctk.CTkEntry(form_card, placeholder_text="Amount Paid ($)", fg_color=COLOR_CARD_HOVER, border_color=COLOR_BORDER)
        amt_e.pack(fill="x", padx=18, pady=8)

        mode_m = ctk.CTkOptionMenu(form_card, values=["UPI", "Cash", "Credit/Debit Card"], fg_color=COLOR_CARD_HOVER, button_color=COLOR_ACCENT)
        mode_m.pack(fill="x", padx=18, pady=8)

        def pay_sub():
            p_ok, p_msg = record_payment(reg_e.get(), amt_e.get(), mode_m.get())
            if p_ok:
                messagebox.showinfo("Success", p_msg)
                self.render_payments()
            else:
                messagebox.showerror("Error", p_msg)

        ctk.CTkButton(form_card, text="Submit Payment", fg_color=COLOR_SUCCESS, hover_color="#059669", font=ctk.CTkFont(family=FONT_FAMILY, size=13, weight="bold"), command=pay_sub).pack(fill="x", padx=18, pady=(16, 18))

        table_card = ctk.CTkFrame(body, fg_color=COLOR_CARD, corner_radius=12, border_width=1, border_color=COLOR_BORDER)
        table_card.grid(row=0, column=1, padx=(8, 0), sticky="nsew")

        ctk.CTkLabel(table_card, text="Payment Ledger & Dues", font=ctk.CTkFont(family=FONT_FAMILY, size=16, weight="bold"), text_color=COLOR_TEXT_MAIN).pack(anchor="w", padx=18, pady=(16, 12))

        cols = ("Reg ID", "Name", "Fee", "Paid", "Due", "Status", "Mode")
        tree = ttk.Treeview(table_card, columns=cols, show="headings", height=12)
        for col in cols:
            tree.heading(col, text=col)
            tree.column(col, width=80 if col not in ["Name"] else 120, anchor="center")

        tree.pack(fill="both", expand=True, padx=16, pady=(0, 16))

        for p in get_all_participants():
            due = p["fee"] - p["amount_paid"]
            tree.insert("", "end", values=(
                p["reg_id"], p["name"], f"${p['fee']:.2f}", f"${p['amount_paid']:.2f}",
                f"${due:.2f}", p["payment_status"], p.get("payment_mode", "N/A")
            ))

    # ---------------------------------------------------------
    # VIEW 5: ATTENDANCE
    # ---------------------------------------------------------
    def render_attendance(self):
        sub_hdr = ctk.CTkFrame(self.main_container, fg_color="transparent")
        sub_hdr.pack(fill="x", pady=(0, 14))
        ctk.CTkLabel(sub_hdr, text="Attendance & Certificates", font=ctk.CTkFont(family=FONT_FAMILY, size=20, weight="bold"), text_color=COLOR_TEXT_MAIN).pack(side="left")

        att = get_attendance_summary()

        strip = ctk.CTkFrame(self.main_container, fg_color=COLOR_CARD, corner_radius=12, border_width=1, border_color=COLOR_BORDER)
        strip.pack(fill="x", pady=(0, 16))

        info = (
            f"📋 Enrolled: {att['total']}    |    "
            f"✅ Present: {att['present']}    |    "
            f"❌ Absent: {att['absent']}    |    "
            f"📊 Attendance Rate: {att['attendance_rate']:.1f}%    |    "
            f"🎓 Certificate Eligible: {att['eligible_certificates']}"
        )
        ctk.CTkLabel(strip, text=info, font=ctk.CTkFont(family=FONT_FAMILY, size=13, weight="bold"), text_color=COLOR_GOLD).pack(padx=20, pady=12)

        card = ctk.CTkFrame(self.main_container, fg_color=COLOR_CARD, corner_radius=12, border_width=1, border_color=COLOR_BORDER)
        card.pack(fill="both", expand=True)

        cols = ("Reg ID", "Name", "Event", "Payment Status", "Attendance", "Certificate Status")
        tree = ttk.Treeview(card, columns=cols, show="headings", height=12)
        for col in cols:
            tree.heading(col, text=col)
            tree.column(col, width=120 if col not in ["Name", "Event"] else 150, anchor="center")

        tree.pack(fill="both", expand=True, padx=16, pady=(16, 10))

        for p in get_all_participants():
            tree.insert("", "end", values=(
                p["reg_id"], p["name"], p["event"],
                p["payment_status"], p.get("attendance", "Absent"), p.get("certificate_eligible", "Not Eligible")
            ))

        btn_bar = ctk.CTkFrame(card, fg_color="transparent")
        btn_bar.pack(fill="x", padx=16, pady=(0, 16))

        def mark_sub(stat):
            sel = tree.selection()
            if not sel:
                messagebox.showwarning("Warning", "Select a participant.")
                return
            reg_id = tree.item(sel[0])["values"][0]
            m_ok, m_msg = mark_attendance(reg_id, stat)
            if m_ok:
                messagebox.showinfo("Updated", m_msg)
                self.render_attendance()
            else:
                messagebox.showerror("Error", m_msg)

        ctk.CTkButton(btn_bar, text="Mark Present", fg_color=COLOR_SUCCESS, hover_color="#059669", command=lambda: mark_sub("Present")).pack(side="left", padx=(0, 8))
        ctk.CTkButton(btn_bar, text="Mark Absent", fg_color=COLOR_DANGER, hover_color="#C0392B", command=lambda: mark_sub("Absent")).pack(side="left")

    # ---------------------------------------------------------
    # VIEW 6: ANALYTICS (WITH GRAPHICAL PLOTS)
    # ---------------------------------------------------------
    def render_analytics(self):
        sub_hdr = ctk.CTkFrame(self.main_container, fg_color="transparent")
        sub_hdr.pack(fill="x", pady=(0, 14))
        ctk.CTkLabel(sub_hdr, text="Participant & Demographic Analytics", font=ctk.CTkFont(family=FONT_FAMILY, size=20, weight="bold"), text_color=COLOR_TEXT_MAIN).pack(side="left")

        analytics = generate_full_analytics()

        scroll = ctk.CTkScrollableFrame(self.main_container, fg_color="transparent")
        scroll.pack(fill="both", expand=True)

        # Charts Row 1: Payment Status Donut + Gender Donut
        r1 = ctk.CTkFrame(scroll, fg_color="transparent")
        r1.pack(fill="x", pady=(0, 16))
        r1.grid_columnconfigure(0, weight=1)
        r1.grid_columnconfigure(1, weight=1)

        c_pay = ChartWidget(r1, title="💳 Payment Status Distribution")
        c_pay.grid(row=0, column=0, padx=(0, 8), sticky="nsew")
        c_pay.plot_donut_chart(["Paid", "Partially Paid", "Pending"], list(analytics["payment_counts"].values()), colors=[COLOR_SUCCESS, COLOR_WARNING, COLOR_DANGER])

        c_gen = ChartWidget(r1, title="🚻 Gender Demographics")
        c_gen.grid(row=0, column=1, padx=(8, 0), sticky="nsew")
        c_gen.plot_donut_chart(list(analytics["gender_counts"].keys()), list(analytics["gender_counts"].values()), colors=[COLOR_GOLD, COLOR_ACCENT, COLOR_PURPLE])

        # Charts Row 2: Category Registrations Bar Chart
        r2 = ctk.CTkFrame(scroll, fg_color="transparent")
        r2.pack(fill="x", pady=(0, 16))
        r2.grid_columnconfigure(0, weight=1)

        c_cat = ChartWidget(r2, title="🏷️ Category Enrollment Metrics")
        c_cat.grid(row=0, column=0, sticky="nsew")
        c_cat.plot_bar_chart(list(analytics["category_counts"].keys()), list(analytics["category_counts"].values()), colors=COLOR_GOLD)

    # ---------------------------------------------------------
    # VIEW 7: REPORTS
    # ---------------------------------------------------------
    def render_reports(self):
        sub_hdr = ctk.CTkFrame(self.main_container, fg_color="transparent")
        sub_hdr.pack(fill="x", pady=(0, 14))
        ctk.CTkLabel(sub_hdr, text="Reports & Data Export Center", font=ctk.CTkFont(family=FONT_FAMILY, size=20, weight="bold"), text_color=COLOR_TEXT_MAIN).pack(side="left")

        controls = ctk.CTkFrame(self.main_container, fg_color=COLOR_CARD, corner_radius=12, border_width=1, border_color=COLOR_BORDER)
        controls.pack(fill="x", pady=(0, 16))

        ctk.CTkLabel(controls, text="Export Actions", font=ctk.CTkFont(family=FONT_FAMILY, size=15, weight="bold"), text_color=COLOR_TEXT_MAIN).pack(anchor="w", padx=18, pady=(14, 8))

        btn_row = ctk.CTkFrame(controls, fg_color="transparent")
        btn_row.pack(fill="x", padx=18, pady=(0, 14))

        def gen_txt():
            ok, name, path = generate_text_report()
            if ok:
                messagebox.showinfo("Report Generated", f"Text Report saved:\n{name}")
                load_files()
            else:
                messagebox.showerror("Error", name)

        def exp_csv():
            ok, name, path = export_participants_csv()
            if ok:
                messagebox.showinfo("CSV Exported", f"CSV file exported:\n{name}")
                load_files()
            else:
                messagebox.showerror("Error", name)

        ctk.CTkButton(btn_row, text="📄  Generate Text Summary", fg_color=COLOR_ACCENT, hover_color=COLOR_ACCENT_HOVER, command=gen_txt).pack(side="left", padx=(0, 10))
        ctk.CTkButton(btn_row, text="📊  Export CSV File", fg_color=COLOR_SUCCESS, hover_color="#059669", command=exp_csv).pack(side="left")

        # Report Viewer Box
        viewer = ctk.CTkFrame(self.main_container, fg_color=COLOR_CARD, corner_radius=12, border_width=1, border_color=COLOR_BORDER)
        viewer.pack(fill="both", expand=True)

        hdr = ctk.CTkFrame(viewer, fg_color="transparent")
        hdr.pack(fill="x", padx=18, pady=12)

        ctk.CTkLabel(hdr, text="View Saved Report:", font=ctk.CTkFont(family=FONT_FAMILY, size=13, weight="bold"), text_color=COLOR_TEXT_MAIN).pack(side="left", padx=(0, 10))

        dropdown = ctk.CTkOptionMenu(hdr, values=["No Reports"], fg_color=COLOR_CARD_HOVER, button_color=COLOR_ACCENT)
        dropdown.pack(side="left", fill="x", expand=True, padx=(0, 10))

        txt_area = ctk.CTkTextbox(viewer, font=ctk.CTkFont(family="Consolas", size=11), fg_color=BG_MAIN, text_color=COLOR_TEXT_MAIN)
        txt_area.pack(fill="both", expand=True, padx=18, pady=(0, 18))

        def load_files():
            files = list_report_files()
            if files:
                dropdown.configure(values=files)
                dropdown.set(files[0])
                view_file()
            else:
                dropdown.configure(values=["No Reports"])

        def view_file():
            fname = dropdown.get()
            if fname and fname != "No Reports":
                content = read_report_file(fname)
                txt_area.delete("1.0", "end")
                txt_area.insert("1.0", content)

        ctk.CTkButton(hdr, text="Open File", width=90, fg_color=COLOR_CARD_HOVER, hover_color=COLOR_BORDER, command=view_file).pack(side="right")
        load_files()

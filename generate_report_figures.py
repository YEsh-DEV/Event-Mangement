import os
import matplotlib.pyplot as plt
import matplotlib.patches as patches
from PIL import Image
from analytics import generate_full_analytics
from events import get_all_events
from registration import get_all_participants

# Design Theme Constants
BG_MAIN = "#1C1917"
BG_NAV = "#181513"
COLOR_CARD = "#292524"
COLOR_CARD_HOVER = "#383431"
COLOR_ACCENT = "#D97706"
COLOR_GOLD = "#F59E0B"
COLOR_TEXT_MAIN = "#F5F5F4"
COLOR_TEXT_MUTED = "#A8A29E"
COLOR_BORDER = "#44403C"
COLOR_SUCCESS = "#10B981"
COLOR_WARNING = "#F59E0B"
COLOR_DANGER = "#EF4444"
COLOR_PURPLE = "#8B5CF6"

def create_dashboard_figure(output_path):
    analytics = generate_full_analytics()
    fig = plt.figure(figsize=(10, 6), facecolor=BG_MAIN)

    fig.suptitle("EventManager - Dashboard Overview", fontsize=16, fontweight="bold", color=COLOR_GOLD, y=0.95)

    gs = fig.add_gridspec(2, 2, height_ratios=[1, 1.2], hspace=0.3, wspace=0.25)

    ax1 = fig.add_subplot(gs[0, 0])
    ax1.set_facecolor(COLOR_CARD)
    ax1.axis("off")
    kpi_text = (
        f"DASHBOARD SUMMARY METRICS\n"
        f"-----------------------------------------\n"
        f"Total Events:            {analytics['total_events']}\n"
        f"Total Participants:      {analytics['total_participants']}\n"
        f"Revenue Collected:      ${analytics['total_revenue_collected']:.2f}\n"
        f"Outstanding Dues:        ${analytics['outstanding_dues']:.2f}\n"
        f"Collection Rate:         {analytics['collection_rate']:.1f}%\n"
        f"Capacity Occupancy:      {analytics['occupancy_rate']:.1f}%"
    )
    ax1.text(0.05, 0.5, kpi_text, color=COLOR_TEXT_MAIN, fontsize=11, family="monospace", va="center")

    ax2 = fig.add_subplot(gs[0, 1])
    ax2.set_facecolor(COLOR_CARD)
    cat_labels = list(analytics["category_counts"].keys())
    cat_vals = list(analytics["category_counts"].values())
    wedges, texts, autotexts = ax2.pie(
        cat_vals, labels=cat_labels, autopct="%1.0f%%", startangle=140,
        colors=[COLOR_ACCENT, COLOR_GOLD, COLOR_SUCCESS, COLOR_PURPLE],
        textprops=dict(color=COLOR_TEXT_MAIN, fontsize=10),
        wedgeprops=dict(width=0.4, edgecolor=COLOR_CARD, linewidth=2)
    )
    for at in autotexts:
        at.set_color(COLOR_TEXT_MAIN)
        at.set_weight("bold")
    ax2.set_title("Registrations by Category", color=COLOR_GOLD, fontsize=12, fontweight="bold")

    ax3 = fig.add_subplot(gs[1, :])
    ax3.set_facecolor(COLOR_CARD)
    events = get_all_events()
    participants = get_all_participants()
    evt_rev = {}
    for p in participants:
        title = p.get("event", "Unknown")
        evt_rev[title] = evt_rev.get(title, 0.0) + p.get("amount_paid", 0.0)

    titles = list(evt_rev.keys()) or [e["title"] for e in events]
    revs = [evt_rev.get(t, 0.0) for t in titles] or [0]

    short_titles = [t[:18] + ".." if len(t) > 20 else t for t in titles]
    bars = ax3.bar(short_titles, revs, color=COLOR_ACCENT, width=0.4, edgecolor=COLOR_BORDER)
    ax3.set_title("Revenue Collection per Event ($)", color=COLOR_GOLD, fontsize=12, fontweight="bold")
    ax3.tick_params(colors=COLOR_TEXT_MUTED, labelsize=9)
    ax3.spines['top'].set_visible(False)
    ax3.spines['right'].set_visible(False)
    ax3.spines['left'].set_color(COLOR_BORDER)
    ax3.spines['bottom'].set_color(COLOR_BORDER)
    ax3.grid(axis='y', linestyle='--', alpha=0.3, color=COLOR_BORDER)

    for bar in bars:
        yval = bar.get_height()
        ax3.text(bar.get_x() + bar.get_width()/2.0, yval + 10, f"${yval:.0f}", ha='center', va='bottom', color=COLOR_TEXT_MAIN, fontsize=9, fontweight='bold')

    plt.savefig(output_path, dpi=200, bbox_inches='tight', facecolor=BG_MAIN)
    plt.close(fig)

def create_analytics_figure(output_path):
    analytics = generate_full_analytics()
    fig, (ax1, ax2) = plt.subplots(1, 2, figsize=(10, 4.5), facecolor=BG_MAIN)

    ax1.set_facecolor(COLOR_CARD)
    pay_labels = ["Paid", "Partially Paid", "Pending"]
    pay_vals = list(analytics["payment_counts"].values())
    w1, t1, at1 = ax1.pie(
        pay_vals, labels=pay_labels, autopct="%1.0f%%", startangle=140,
        colors=[COLOR_SUCCESS, COLOR_WARNING, COLOR_DANGER],
        textprops=dict(color=COLOR_TEXT_MAIN, fontsize=10),
        wedgeprops=dict(width=0.4, edgecolor=COLOR_CARD, linewidth=2)
    )
    for at in at1:
        at.set_color(COLOR_TEXT_MAIN)
        at.set_weight("bold")
    ax1.set_title("Payment Status Breakdown", color=COLOR_GOLD, fontsize=12, fontweight="bold")

    ax2.set_facecolor(COLOR_CARD)
    g_labels = list(analytics["gender_counts"].keys())
    g_vals = list(analytics["gender_counts"].values())
    w2, t2, at2 = ax2.pie(
        g_vals, labels=g_labels, autopct="%1.0f%%", startangle=140,
        colors=[COLOR_GOLD, COLOR_ACCENT, COLOR_PURPLE],
        textprops=dict(color=COLOR_TEXT_MAIN, fontsize=10),
        wedgeprops=dict(width=0.4, edgecolor=COLOR_CARD, linewidth=2)
    )
    for at in at2:
        at.set_color(COLOR_TEXT_MAIN)
        at.set_weight("bold")
    ax2.set_title("Gender Demographics", color=COLOR_GOLD, fontsize=12, fontweight="bold")

    plt.suptitle("Participant Analytics & Demographics Overview", fontsize=15, fontweight="bold", color=COLOR_TEXT_MAIN, y=1.02)
    plt.tight_layout()
    plt.savefig(output_path, dpi=200, bbox_inches='tight', facecolor=BG_MAIN)
    plt.close(fig)

def create_table_mockup_figure(title, headers, rows, output_path):
    fig, ax = plt.subplots(figsize=(10, 4.5), facecolor=BG_MAIN)
    ax.set_facecolor(COLOR_CARD)
    ax.axis("off")

    table_data = [headers] + rows
    table = ax.table(cellText=table_data, loc='center', cellLoc='center')
    table.auto_set_font_size(False)
    table.set_fontsize(9)
    table.scale(1.1, 1.8)

    for i in range(len(headers)):
        cell = table[(0, i)]
        cell.set_facecolor(COLOR_CARD_HOVER)
        cell.get_text().set_color(COLOR_GOLD)
        cell.get_text().set_weight("bold")

    for r in range(1, len(table_data)):
        for c in range(len(headers)):
            cell = table[(r, c)]
            cell.set_facecolor(COLOR_CARD)
            cell.get_text().set_color(COLOR_TEXT_MAIN)

    plt.title(title, color=COLOR_GOLD, fontsize=14, fontweight="bold", pad=15)
    plt.tight_layout()
    plt.savefig(output_path, dpi=200, bbox_inches='tight', facecolor=BG_MAIN)
    plt.close(fig)

def main():
    screenshots_dir = os.path.join(os.path.dirname(__file__), "screenshots")
    if not os.path.exists(screenshots_dir):
        os.makedirs(screenshots_dir)

    artifact_dir = r"C:\Users\atmak\.gemini\antigravity-ide\brain\6d7ab084-458d-42c5-bf1b-935daf40a5b2"
    if not os.path.exists(artifact_dir):
        os.makedirs(artifact_dir)

    p1_a = os.path.join(screenshots_dir, "fig_7_1_dashboard.png")
    p1_b = os.path.join(artifact_dir, "fig_7_1_dashboard.png")
    create_dashboard_figure(p1_a)
    Image.open(p1_a).save(p1_b)

    events = get_all_events()
    evt_headers = ["Event ID", "Title", "Category", "Date", "Venue", "Capacity", "Fee ($)"]
    evt_rows = [[e["id"], e["title"][:22], e["category"], e["date"], e["venue"][:15], str(e["capacity"]), f"${e['fee']:.2f}"] for e in events]
    p2_a = os.path.join(screenshots_dir, "fig_7_2_events.png")
    p2_b = os.path.join(artifact_dir, "fig_7_2_events.png")
    create_table_mockup_figure("Scheduled Events List", evt_headers, evt_rows, p2_a)
    Image.open(p2_a).save(p2_b)

    parts = get_all_participants()
    reg_headers = ["Reg ID", "Name", "Gender", "Organization", "Phone", "Event Title"]
    reg_rows = [[p["reg_id"], p["name"], p["gender"], p["organization"][:15], p["phone"], p["event"][:20]] for p in parts]
    p3_a = os.path.join(screenshots_dir, "fig_7_3_registration.png")
    p3_b = os.path.join(artifact_dir, "fig_7_3_registration.png")
    create_table_mockup_figure("Participant Registration Roster", reg_headers, reg_rows, p3_a)
    Image.open(p3_a).save(p3_b)

    pay_headers = ["Reg ID", "Name", "Event Title", "Fee ($)", "Paid ($)", "Due ($)", "Payment Status"]
    pay_rows = [[p["reg_id"], p["name"], p["event"][:18], f"${p['fee']:.2f}", f"${p['amount_paid']:.2f}", f"${(p['fee']-p['amount_paid']):.2f}", p["payment_status"]] for p in parts]
    p4_a = os.path.join(screenshots_dir, "fig_7_4_payments.png")
    p4_b = os.path.join(artifact_dir, "fig_7_4_payments.png")
    create_table_mockup_figure("Payment Ledger & Outstanding Dues", pay_headers, pay_rows, p4_a)
    Image.open(p4_a).save(p4_b)

    att_headers = ["Reg ID", "Name", "Event Title", "Payment Status", "Attendance", "Certificate Status"]
    att_rows = [[p["reg_id"], p["name"], p["event"][:18], p["payment_status"], p.get("attendance", "Absent"), p.get("certificate_eligible", "Not Eligible")] for p in parts]
    p5_a = os.path.join(screenshots_dir, "fig_7_5_attendance.png")
    p5_b = os.path.join(artifact_dir, "fig_7_5_attendance.png")
    create_table_mockup_figure("Attendance & Certificate Eligibility Log", att_headers, att_rows, p5_a)
    Image.open(p5_a).save(p5_b)

    p6_a = os.path.join(screenshots_dir, "fig_7_6_analytics.png")
    p6_b = os.path.join(artifact_dir, "fig_7_6_analytics.png")
    create_analytics_figure(p6_a)
    Image.open(p6_a).save(p6_b)

    rep_headers = ["Report File", "Type", "Status", "Export Format"]
    rep_rows = [
        ["event_report_20260801_131549.txt", "Executive Summary", "Generated", "Plain Text (.txt)"],
        ["participants_export.csv", "Full Roster Data", "Exported", "CSV Spreadsheet (.csv)"]
    ]
    p7_a = os.path.join(screenshots_dir, "fig_7_7_reports.png")
    p7_b = os.path.join(artifact_dir, "fig_7_7_reports.png")
    create_table_mockup_figure("Exported System Reports & Data Logs", rep_headers, rep_rows, p7_a)
    Image.open(p7_a).save(p7_b)

    print("All 7 high-resolution report figure screenshots generated successfully!")

if __name__ == "__main__":
    main()

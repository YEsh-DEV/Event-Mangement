import os
import time
import ctypes
from ctypes import windll, byref, c_int, c_void_p
import mss
from PIL import Image

import ui

def capture_window_mss(app, filename):
    """
    Captures window using mss and window coordinates.
    """
    app.update_idletasks()
    app.update()
    time.sleep(0.3)

    x = app.winfo_rootx()
    y = app.winfo_rooty()
    w = app.winfo_width()
    h = app.winfo_height()

    with mss.mss() as sct:
        monitor = {"top": y, "left": x, "width": w, "height": h}
        sct_img = sct.grab(monitor)
        img = Image.frombytes("RGB", sct_img.size, sct_img.bgra, "raw", "BGRX")
        img.save(filename)
        print(f"Captured screenshot: {filename}")

def main():
    screenshots_dir = os.path.join(os.path.dirname(__file__), "screenshots")
    if not os.path.exists(screenshots_dir):
        os.makedirs(screenshots_dir)

    artifact_dir = r"C:\Users\atmak\.gemini\antigravity-ide\brain\6d7ab084-458d-42c5-bf1b-935daf40a5b2"
    if not os.path.exists(artifact_dir):
        os.makedirs(artifact_dir)

    print("Launching Event Management System for automated screenshot capture...")
    app = ui.EventManagementApp()
    app.update()
    app.deiconify()
    app.focus_force()

    tabs = [
        ("dashboard", "fig_7_1_dashboard.png"),
        ("events", "fig_7_2_events.png"),
        ("registration", "fig_7_3_registration.png"),
        ("payments", "fig_7_4_payments.png"),
        ("attendance", "fig_7_5_attendance.png"),
        ("analytics", "fig_7_6_analytics.png"),
        ("reports", "fig_7_7_reports.png")
    ]

    for key, fname in tabs:
        app.nav_to(key)
        app.update()
        time.sleep(0.5)

        path1 = os.path.join(screenshots_dir, fname)
        path2 = os.path.join(artifact_dir, fname)

        capture_window_mss(app, path1)
        # Duplicate to artifact folder for markdown embedding
        Image.open(path1).save(path2)

    app.destroy()
    print("All 7 UI screenshots captured and saved successfully!")

if __name__ == "__main__":
    main()

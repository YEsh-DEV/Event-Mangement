import sys
from ui import EventManagementApp

def main():
    """
    Main application entry point.
    Initializes configuration, pre-seeds data if empty, and launches CustomTkinter main loop.
    """
    try:
        app = EventManagementApp()
        app.mainloop()
    except Exception as e:
        print(f"An unexpected error occurred while running the application: {e}")
        sys.exit(1)

if __name__ == "__main__":
    main()

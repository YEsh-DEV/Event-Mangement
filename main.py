import sys
from ui import EventManagementApp

def main():
    """
    Entry point for the Event Management System.
    Initializes and launches the CustomTkinter graphical application interface.
    """
    try:
        app = EventManagementApp()
        app.mainloop()
    except Exception as e:
        print(f"An unexpected error occurred while running the application: {e}")
        sys.exit(1)

if __name__ == "__main__":
    main()

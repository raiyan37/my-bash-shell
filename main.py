"""
Interactive Python Shell with GUI

Main entry point for the application.
"""

import tkinter as tk
from gui import ShellGUI


def main():
    """Start the application"""
    root = tk.Tk()
    ShellGUI(root)
    root.mainloop()


if __name__ == "__main__":
    main()
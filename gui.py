"""
GUI components for the Interactive Python Shell.
"""

import os
import tkinter as tk
from tkinter import ttk, scrolledtext
from config import GUIConfig, IS_MAC, WELCOME_MESSAGE
from parser import CommandParser
from history_manager import HistoryManager
from commands import BuiltInCommands
from executor import CommandExecutor


class ShellGUI:
    """
    Main GUI class for the shell.
    Split into two panels: file browser on left, terminal on right.
    """
    
    def __init__(self, root):
        """
        Initialize the GUI.
        
        Args:
            root: Tkinter root window
        """
        self.root = root
        self.root.title("Interactive Python Shell")
        self.root.geometry(GUIConfig.get_geometry())
        
        # Initialize core components
        self.history_manager = HistoryManager()
        self.builtin_commands = BuiltInCommands(self.history_manager)
        self.executor = CommandExecutor(self.builtin_commands)
        self.parser = CommandParser()
        
        # Build the interface
        self._create_layout()
        self._show_welcome()
        self.refresh_tree()
        self.command_entry.focus()
    
    def _create_layout(self):
        """Create the main GUI layout"""
        # Create the split-pane layout
        main_container = ttk.PanedWindow(self.root, orient=tk.HORIZONTAL)
        main_container.pack(fill=tk.BOTH, expand=True, padx=5, pady=5)
        
        # Left panel - file browser
        left_frame = ttk.Frame(main_container)
        main_container.add(left_frame, weight=1)
        self._create_file_browser(left_frame)
        
        # Right panel - terminal
        right_frame = ttk.Frame(main_container)
        main_container.add(right_frame, weight=2)
        self._create_terminal(right_frame)
    
    def _create_file_browser(self, parent):
        """Create the file browser panel"""
        ttk.Label(
            parent,
            text=GUIConfig.FILE_BROWSER_TITLE,
            font=("Arial", 11, "bold")
        ).pack(pady=5)
        
        # Show current directory
        self.current_dir_var = tk.StringVar(value=os.getcwd())
        dir_frame = ttk.Frame(parent)
        dir_frame.pack(fill=tk.X, padx=5, pady=5)
        ttk.Label(dir_frame, text="Current:").pack(side=tk.LEFT)
        ttk.Entry(
            dir_frame,
            textvariable=self.current_dir_var,
            state="readonly"
        ).pack(side=tk.LEFT, fill=tk.X, expand=True, padx=5)
        
        # Tree view for files and folders
        tree_frame = ttk.Frame(parent)
        tree_frame.pack(fill=tk.BOTH, expand=True, padx=5, pady=5)
        
        self.file_tree = ttk.Treeview(tree_frame, selectmode='browse')
        tree_scroll = ttk.Scrollbar(
            tree_frame,
            orient=tk.VERTICAL,
            command=self.file_tree.yview
        )
        self.file_tree.configure(yscrollcommand=tree_scroll.set)
        
        self.file_tree.pack(side=tk.LEFT, fill=tk.BOTH, expand=True)
        tree_scroll.pack(side=tk.RIGHT, fill=tk.Y)
        
        # Double-click to navigate into folders
        self.file_tree.bind('<Double-1>', self.on_tree_double_click)
        
        # Quick action buttons
        action_frame = ttk.Frame(parent)
        action_frame.pack(fill=tk.X, padx=5, pady=5)
        
        ttk.Button(
            action_frame,
            text="📁 New Folder",
            command=self.create_folder
        ).pack(side=tk.LEFT, padx=2)
        ttk.Button(
            action_frame,
            text="📄 New File",
            command=self.create_file
        ).pack(side=tk.LEFT, padx=2)
        ttk.Button(
            action_frame,
            text="🔄 Refresh",
            command=self.refresh_tree
        ).pack(side=tk.LEFT, padx=2)
    
    def _create_terminal(self, parent):
        """Create the terminal panel"""
        ttk.Label(
            parent,
            text=GUIConfig.TERMINAL_TITLE,
            font=("Arial", 11, "bold")
        ).pack(pady=5)
        
        # Terminal display with classic green on black
        self.terminal = scrolledtext.ScrolledText(
            parent,
            wrap=tk.WORD,
            bg=GUIConfig.TERMINAL_BG,
            fg=GUIConfig.TERMINAL_FG,
            insertbackground=GUIConfig.TERMINAL_CURSOR,
            font=GUIConfig.get_terminal_font(),
            height=20
        )
        self.terminal.pack(fill=tk.BOTH, expand=True, padx=5, pady=5)
        
        # Command input area
        input_frame = ttk.Frame(parent)
        input_frame.pack(fill=tk.X, padx=5, pady=5)
        
        terminal_font = GUIConfig.get_terminal_font()
        ttk.Label(
            input_frame,
            text=GUIConfig.PROMPT_SYMBOL,
            foreground="green",
            font=(terminal_font[0], terminal_font[1], 'bold')
        ).pack(side=tk.LEFT)
        
        self.command_entry = ttk.Entry(input_frame, font=GUIConfig.get_entry_font())
        self.command_entry.pack(side=tk.LEFT, fill=tk.X, expand=True, padx=5)
        
        # Keyboard shortcuts
        self.command_entry.bind('<Return>', self.execute_command)
        self.command_entry.bind('<Up>', self.history_up)
        self.command_entry.bind('<Down>', self.history_down)
        
        # Mac-specific shortcuts for clearing terminal
        if IS_MAC:
            self.command_entry.bind('<Command-l>', lambda e: self._clear_terminal())
            self.command_entry.bind('<Command-k>', lambda e: self._clear_terminal())
        
        ttk.Button(input_frame, text="Run", command=self.execute_command).pack(side=tk.LEFT)
    
    def _show_welcome(self):
        """Display welcome message"""
        self.write_output(WELCOME_MESSAGE.format(cwd=os.getcwd()))
    
    def _clear_terminal(self):
        """Clear the terminal display"""
        self.terminal.delete(1.0, tk.END)
    
    def write_output(self, text):
        """
        Write text to the terminal and auto-scroll to bottom.
        
        Args:
            text (str): Text to display
        """
        self.terminal.insert(tk.END, text)
        self.terminal.see(tk.END)
    
    def execute_command(self, event=None):
        """Main entry point when user runs a command"""
        command = self.command_entry.get().strip()
        if not command:
            return
        
        # Handle special commands first
        if command == "exit":
            self.history_manager.save_to_histfile()
            self.root.quit()
            return
        
        if command == "clear":
            self._clear_terminal()
            self.command_entry.delete(0, tk.END)
            return
        
        # Add to history
        self.history_manager.add(command)
        
        # Show command in terminal
        self.write_output(f"$ {command}\n")
        self.command_entry.delete(0, tk.END)
        
        # Parse and execute
        parts = self.parser.parse(command)
        if not parts:
            return
        
        try:
            output = self.executor.execute(parts)
            if output:
                self.write_output(output + "\n")
        except Exception as e:
            self.write_output(f"Error: {str(e)}\n")
        
        # Refresh file browser in case files changed
        self.refresh_tree()
    
    def refresh_tree(self):
        """Update the file browser to show current directory"""
        self.file_tree.delete(*self.file_tree.get_children())
        self.current_dir_var.set(os.getcwd())
        
        try:
            # Add ".." to go up one level
            self.file_tree.insert('', 'end', text="📁 ..", values=('..', 'dir'))
            
            # List everything in current directory
            items = os.listdir('.')
            for item in sorted(items):
                if os.path.isdir(item):
                    self.file_tree.insert(
                        '', 'end',
                        text=f"📁 {item}",
                        values=(item, 'dir')
                    )
                else:
                    self.file_tree.insert(
                        '', 'end',
                        text=f"📄 {item}",
                        values=(item, 'file')
                    )
        except PermissionError:
            self.write_output("Permission denied to list directory\n")
    
    def on_tree_double_click(self, event):
        """Handle double-click on folders to navigate"""
        selection = self.file_tree.selection()
        if not selection:
            return
        
        item = self.file_tree.item(selection[0])
        values = item['values']
        
        if values and len(values) >= 2:
            name, item_type = values[0], values[1]
            
            if item_type == 'dir':
                try:
                    os.chdir(name)
                    self.current_dir_var.set(os.getcwd())
                    self.write_output(f"$ cd {name}\n")
                    self.write_output(f"Changed to: {os.getcwd()}\n")
                    self.refresh_tree()
                except Exception as e:
                    self.write_output(f"Error: {str(e)}\n")
    
    def create_folder(self):
        """Show popup dialog to create a new folder"""
        dialog = tk.Toplevel(self.root)
        dialog.title("Create Folder")
        dialog.geometry("300x100")
        dialog.transient(self.root)
        
        ttk.Label(dialog, text="Folder name:").pack(pady=10)
        entry = ttk.Entry(dialog, width=30)
        entry.pack(pady=5)
        entry.focus()
        
        def create():
            name = entry.get().strip()
            if name:
                try:
                    os.makedirs(name, exist_ok=True)
                    self.write_output(f"Created folder: {name}\n")
                    self.refresh_tree()
                    dialog.destroy()
                except Exception as e:
                    self.write_output(f"Error creating folder: {str(e)}\n")
        
        entry.bind('<Return>', lambda e: create())
        ttk.Button(dialog, text="Create", command=create).pack(pady=5)
    
    def create_file(self):
        """Show popup dialog to create a new file"""
        dialog = tk.Toplevel(self.root)
        dialog.title("Create File")
        dialog.geometry("300x100")
        dialog.transient(self.root)
        
        ttk.Label(dialog, text="File name:").pack(pady=10)
        entry = ttk.Entry(dialog, width=30)
        entry.pack(pady=5)
        entry.focus()
        
        def create():
            name = entry.get().strip()
            if name:
                try:
                    with open(name, 'a'):
                        pass
                    self.write_output(f"Created file: {name}\n")
                    self.refresh_tree()
                    dialog.destroy()
                except Exception as e:
                    self.write_output(f"Error creating file: {str(e)}\n")
        
        entry.bind('<Return>', lambda e: create())
        ttk.Button(dialog, text="Create", command=create).pack(pady=5)
    
    def history_up(self, event):
        """Go to previous command in history (up arrow key)"""
        prev_cmd = self.history_manager.get_previous()
        if prev_cmd is not None:
            self.command_entry.delete(0, tk.END)
            self.command_entry.insert(0, prev_cmd)
    
    def history_down(self, event):
        """Go to next command in history (down arrow key)"""
        next_cmd = self.history_manager.get_next()
        if next_cmd is not None:
            self.command_entry.delete(0, tk.END)
            self.command_entry.insert(0, next_cmd)
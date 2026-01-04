"""
Command history management for the Interactive Python Shell.
Handles storing, loading, and navigating command history.
"""

import os


class HistoryManager:
    """Manages command history with file persistence"""
    
    def __init__(self):
        """Initialize history manager"""
        self.history = []
        self.saved_count = 0
        self.current_index = 0
        
        # Try to load history from HISTFILE if it exists
        self._load_from_histfile()
    
    def _load_from_histfile(self):
        """Load history from HISTFILE environment variable if set"""
        histfile_env = os.environ.get("HISTFILE")
        if histfile_env and os.path.exists(histfile_env):
            try:
                with open(histfile_env, 'r') as f:
                    self.history = [line.strip() for line in f if line.strip()]
                    self.saved_count = len(self.history)
                    self.current_index = len(self.history)
            except Exception:
                pass
    
    def add(self, command):
        """
        Add a command to history.
        
        Args:
            command (str): Command to add
        """
        self.history.append(command)
        self.current_index = len(self.history)
    
    def get_previous(self, current_text=""):
        """
        Get the previous command in history.
        
        Args:
            current_text (str): Current input text (unused for now)
            
        Returns:
            str or None: Previous command or None if at start
        """
        if self.current_index > 0:
            self.current_index -= 1
            return self.history[self.current_index]
        return None
    
    def get_next(self):
        """
        Get the next command in history.
        
        Returns:
            str or None: Next command or None if at end
        """
        if self.current_index < len(self.history) - 1:
            self.current_index += 1
            return self.history[self.current_index]
        elif self.current_index == len(self.history) - 1:
            # At the end, return empty to clear entry
            self.current_index = len(self.history)
            return ""
        return None
    
    def read_from_file(self, filepath):
        """
        Read history from a file.
        
        Args:
            filepath (str): Path to history file
            
        Returns:
            int: Number of commands loaded
        """
        with open(filepath, 'r') as f:
            self.history = [line.strip() for line in f if line.strip()]
            self.saved_count = len(self.history)
            self.current_index = len(self.history)
        return len(self.history)
    
    def write_to_file(self, filepath):
        """
        Write all history to a file.
        
        Args:
            filepath (str): Path to history file
            
        Returns:
            int: Number of commands written
        """
        with open(filepath, 'w') as f:
            for cmd in self.history:
                f.write(cmd + '\n')
        self.saved_count = len(self.history)
        return len(self.history)
    
    def append_to_file(self, filepath):
        """
        Append only new commands to a file.
        
        Args:
            filepath (str): Path to history file
            
        Returns:
            int: Number of new commands appended
        """
        current_len = len(self.history)
        new_items = current_len - self.saved_count
        
        if new_items > 0:
            with open(filepath, 'a') as f:
                for cmd in self.history[-new_items:]:
                    f.write(cmd + '\n')
            self.saved_count = current_len
        
        return new_items
    
    def save_to_histfile(self):
        """Save history to HISTFILE if environment variable is set"""
        histfile = os.environ.get("HISTFILE")
        if histfile:
            try:
                self.write_to_file(histfile)
            except Exception:
                pass
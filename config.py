"""
Configuration and constants for the Interactive Python Shell.
"""

import platform

# Commands that are built into this shell (not external programs)
BUILT_IN_COMMANDS = (
    "echo", "exit", "type", "pwd", "cd", "history",
    "ls", "mkdir", "touch", "cat", "clear"
)

# Platform detection
IS_MAC = platform.system() == 'Darwin'

# GUI Configuration
class GUIConfig:
    """GUI-related configuration settings"""
    
    # Window dimensions
    MAC_GEOMETRY = "1100x650"
    DEFAULT_GEOMETRY = "1000x600"
    
    # Fonts
    MAC_TERMINAL_FONT = ('Monaco', 11)
    MAC_ENTRY_FONT = ('Monaco', 11)
    DEFAULT_TERMINAL_FONT = ('Courier', 10)
    DEFAULT_ENTRY_FONT = ('Courier', 10)
    
    # Terminal colors
    TERMINAL_BG = 'black'
    TERMINAL_FG = '#00ff00'
    TERMINAL_CURSOR = '#00ff00'
    
    # Labels
    PROMPT_SYMBOL = "$"
    FILE_BROWSER_TITLE = "📁 File Browser"
    TERMINAL_TITLE = "💻 Terminal"
    
    @classmethod
    def get_geometry(cls):
        """Get appropriate window geometry for current platform"""
        return cls.MAC_GEOMETRY if IS_MAC else cls.DEFAULT_GEOMETRY
    
    @classmethod
    def get_terminal_font(cls):
        """Get appropriate terminal font for current platform"""
        return cls.MAC_TERMINAL_FONT if IS_MAC else cls.DEFAULT_TERMINAL_FONT
    
    @classmethod
    def get_entry_font(cls):
        """Get appropriate entry font for current platform"""
        return cls.MAC_ENTRY_FONT if IS_MAC else cls.DEFAULT_ENTRY_FONT


# Command execution settings
SUBPROCESS_TIMEOUT = 5  # seconds

# Welcome message
WELCOME_MESSAGE = """Welcome to Interactive Python Shell!
Current directory: {cwd}
Type 'help' for available commands
Supports pipelines (|) and history commands

"""
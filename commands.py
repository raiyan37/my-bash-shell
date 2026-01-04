"""
Built-in command implementations for the Interactive Python Shell.
"""

import os
from config import BUILT_IN_COMMANDS


class BuiltInCommands:
    """Handler for all built-in shell commands"""
    
    def __init__(self, history_manager):
        """
        Initialize with a reference to the history manager.
        
        Args:
            history_manager: HistoryManager instance for history command
        """
        self.history_manager = history_manager
    
    def execute(self, command, args):
        """
        Execute a built-in command.
        
        Args:
            command (str): The command name
            args (list): Command arguments
            
        Returns:
            str: Command output or None for commands that don't produce output
        """
        if command == "help":
            return self._help()
        elif command == "echo":
            return self._echo(args)
        elif command == "pwd":
            return self._pwd()
        elif command == "cd":
            return self._cd(args)
        elif command == "ls":
            return self._ls(args)
        elif command == "mkdir":
            return self._mkdir(args)
        elif command == "touch":
            return self._touch(args)
        elif command == "cat":
            return self._cat(args)
        elif command == "type":
            return self._type(args)
        elif command == "history":
            return self._history(args)
        else:
            return f"{command}: unknown command"
    
    def _help(self):
        """Display help information"""
        return (
            "Available commands:\n"
            "  Built-in: echo, pwd, cd, ls, mkdir, touch, cat, clear, type, history, exit\n"
            "  Pipelines: Use | to chain commands (e.g., 'ls | cat')\n"
            "  History: 'history' to view, 'history -r <file>' to read, 'history -w <file>' to write\n"
            "           'history -a <file>' to append new entries\n"
            "  Use the file browser on the left to navigate\n"
            "  Double-click folders to cd into them"
        )
    
    def _echo(self, args):
        """Print arguments to output"""
        return " ".join(args)
    
    def _pwd(self):
        """Print working directory"""
        return os.getcwd()
    
    def _cd(self, args):
        """Change directory"""
        if len(args) == 0:
            path = os.path.expanduser("~")
        else:
            path = os.path.expanduser(args[0])
        
        try:
            os.chdir(path)
            return f"Changed to: {os.getcwd()}"
        except Exception as e:
            return f"cd: {str(e)}"
    
    def _ls(self, args):
        """List directory contents"""
        try:
            path = args[0] if args else "."
            items = os.listdir(path)
            result = []
            
            for item in sorted(items):
                full_path = os.path.join(path, item)
                if os.path.isdir(full_path):
                    result.append(f"📁 {item}/")
                else:
                    result.append(f"📄 {item}")
            
            return "\n".join(result) if result else "(empty directory)"
        except Exception as e:
            return f"ls: {str(e)}"
    
    def _mkdir(self, args):
        """Create a directory"""
        if not args:
            return "mkdir: missing operand"
        
        try:
            os.makedirs(args[0], exist_ok=True)
            return f"Created directory: {args[0]}"
        except Exception as e:
            return f"mkdir: {str(e)}"
    
    def _touch(self, args):
        """Create an empty file"""
        if not args:
            return "touch: missing operand"
        
        try:
            with open(args[0], 'a'):
                pass
            return f"Created file: {args[0]}"
        except Exception as e:
            return f"touch: {str(e)}"
    
    def _cat(self, args):
        """Display file contents"""
        if not args:
            return "cat: missing operand"
        
        try:
            with open(args[0], 'r') as f:
                return f.read()
        except Exception as e:
            return f"cat: {str(e)}"
    
    def _type(self, args):
        """Show information about a command"""
        if not args:
            return "type: missing operand"
        
        if args[0] in BUILT_IN_COMMANDS:
            return f"{args[0]} is a shell builtin"
        else:
            # Search PATH for the command
            path_env = os.environ.get("PATH", "")
            directories = path_env.split(os.pathsep)
            
            for directory in directories:
                full_path = os.path.join(directory, args[0])
                if os.path.isfile(full_path) and os.access(full_path, os.X_OK):
                    return f"{args[0]} is {full_path}"
            
            return f"{args[0]}: not found"
    
    def _history(self, args):
        """Manage command history"""
        # history -r <file>: read history from file
        if len(args) >= 2 and args[0] == "-r":
            path = args[1]
            try:
                count = self.history_manager.read_from_file(path)
                return f"Loaded {count} commands from {path}"
            except FileNotFoundError:
                return f"history: {path}: No such file or directory"
            except Exception as e:
                return f"history: {path}: {str(e)}"
        
        # history -w <file>: write history to file
        elif len(args) >= 2 and args[0] == "-w":
            path = args[1]
            try:
                count = self.history_manager.write_to_file(path)
                return f"Wrote {count} commands to {path}"
            except Exception as e:
                return f"history: {path}: {str(e)}"
        
        # history -a <file>: append new commands only
        elif len(args) >= 2 and args[0] == "-a":
            path = args[1]
            try:
                count = self.history_manager.append_to_file(path)
                if count > 0:
                    return f"Appended {count} new commands to {path}"
                else:
                    return "No new commands to append"
            except Exception as e:
                return f"history: {path}: {str(e)}"
        
        # Just show history (optionally last N commands)
        else:
            start_index = 0
            if len(args) > 0:
                try:
                    n = int(args[0])
                    start_index = max(0, len(self.history_manager.history) - n)
                except ValueError:
                    pass
            
            result = []
            for i in range(start_index, len(self.history_manager.history)):
                result.append(f"{i + 1:>5}  {self.history_manager.history[i]}")
            
            return "\n".join(result) if result else "(no history)"
"""
Command execution engine for the Interactive Python Shell.
Handles both built-in commands and external programs, including pipelines.
"""

import sys
import io
import subprocess
from config import BUILT_IN_COMMANDS, SUBPROCESS_TIMEOUT


class CommandExecutor:
    """Executes commands and pipelines"""
    
    def __init__(self, builtin_commands):
        """
        Initialize with built-in command handler.
        
        Args:
            builtin_commands: BuiltInCommands instance
        """
        self.builtin_commands = builtin_commands
    
    def execute(self, parts):
        """
        Execute a command or pipeline.
        
        Args:
            parts (list): Parsed command tokens
            
        Returns:
            str: Command output
        """
        if not parts:
            return ""
        
        # Check if it's a pipeline (has | symbol)
        if '|' in parts:
            return self._execute_pipeline(parts)
        else:
            return self._execute_single(parts)
    
    def _execute_pipeline(self, parts):
        """
        Execute commands connected by pipes.
        Example: "ls | cat" runs ls and feeds output to cat
        
        Args:
            parts (list): Command tokens including pipe symbols
            
        Returns:
            str: Final pipeline output
        """
        # Split by pipe symbol
        commands = []
        current_cmd = []
        
        for part in parts:
            if part == '|':
                if current_cmd:
                    commands.append(current_cmd)
                current_cmd = []
            else:
                current_cmd.append(part)
        
        if current_cmd:
            commands.append(current_cmd)
        
        if not commands:
            return ""
        
        # Run each command in sequence
        prev_output = None
        
        for i, cmd_parts in enumerate(commands):
            if not cmd_parts:
                continue
            
            is_last = (i == len(commands) - 1)
            command = cmd_parts[0]
            
            # Handle built-in commands
            if command in BUILT_IN_COMMANDS:
                # Capture output by redirecting stdout
                old_stdout = sys.stdout
                sys.stdout = io.StringIO()
                
                try:
                    self._execute_single(cmd_parts)
                    output = sys.stdout.getvalue()
                finally:
                    sys.stdout = old_stdout
                
                if is_last:
                    return output.strip()
                else:
                    prev_output = output
            
            # Handle external commands
            else:
                try:
                    stdin_data = prev_output.encode() if prev_output else None
                    
                    result = subprocess.run(
                        cmd_parts,
                        input=stdin_data,
                        capture_output=True,
                        text=False,
                        timeout=SUBPROCESS_TIMEOUT
                    )
                    
                    output = result.stdout.decode()
                    if result.stderr:
                        output += result.stderr.decode()
                    
                    if is_last:
                        return output.strip()
                    else:
                        prev_output = output
                        
                except FileNotFoundError:
                    return f"{command}: command not found"
                except subprocess.TimeoutExpired:
                    return f"{command}: command timed out"
                except Exception as e:
                    return f"{command}: {str(e)}"
        
        return ""
    
    def _execute_single(self, parts):
        """
        Execute a single command (not a pipeline).
        
        Args:
            parts (list): Command tokens
            
        Returns:
            str: Command output
        """
        command = parts[0]
        args = parts[1:] if len(parts) > 1 else []
        
        # Check if it's a built-in command
        if command in BUILT_IN_COMMANDS:
            return self.builtin_commands.execute(command, args)
        
        # Not a built-in, try to run as external command
        else:
            try:
                result = subprocess.run(
                    parts,
                    capture_output=True,
                    text=True,
                    timeout=SUBPROCESS_TIMEOUT
                )
                
                output = result.stdout
                if result.stderr:
                    output += result.stderr
                
                return output.strip() if output else f"Command completed (exit code: {result.returncode})"
            except FileNotFoundError:
                return f"{command}: command not found"
            except subprocess.TimeoutExpired:
                return f"{command}: command timed out"
            except Exception as e:
                return f"{command}: {str(e)}"
"""
Command line parser for the Interactive Python Shell.
Handles quote parsing, escape characters, and tokenization.
"""


class CommandParser:
    """
    Parses command input handling quotes and escape characters.
    Example: 'echo "hello world"' -> ['echo', 'hello world']
    """
    
    @staticmethod
    def parse(text):
        """
        Parse command input into tokens.
        
        Args:
            text (str): Raw command input
            
        Returns:
            list: List of parsed tokens
        """
        parts = []
        token = []
        in_single_quote = False
        in_double_quote = False
        i = 0
        
        while i < len(text):
            curr_char = text[i]
            
            # Handle single quotes
            if curr_char == "'" and not in_double_quote:
                in_single_quote = not in_single_quote
                i += 1
            
            # Handle double quotes
            elif curr_char == '"' and not in_single_quote:
                in_double_quote = not in_double_quote
                i += 1
            
            # Space outside quotes = word boundary
            elif curr_char == ' ' and not in_single_quote and not in_double_quote:
                if token:
                    parts.append("".join(token))
                    token = []
                i += 1
            
            # Backslash escape outside quotes
            elif curr_char == '\\' and not in_single_quote and not in_double_quote:
                if i + 1 < len(text):
                    next_char = text[i+1]
                    token.append(next_char)
                    i += 2
                else:
                    i += 1
            
            # Backslash escape inside double quotes (only for " and \)
            elif curr_char == '\\' and not in_single_quote:
                if i + 1 < len(text):
                    next_char = text[i+1]
                    if next_char in ('"', '\\'):
                        token.append(next_char)
                        i += 2
                    else:
                        token.append(curr_char)
                        i += 1
                else:
                    token.append(curr_char)
                    i += 1
            
            # Regular character
            else:
                token.append(curr_char)
                i += 1
        
        # Don't forget last token
        if token:
            parts.append("".join(token))
        
        return parts
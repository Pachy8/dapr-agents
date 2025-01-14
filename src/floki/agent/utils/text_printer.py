from floki.types.message import BaseMessage
from typing import Optional, Any, Union, Dict
from colorama import Style

# Define your custom colors as a dictionary
COLORS = {
    "floki_teal": '\033[38;2;147;191;183m',
    "floki_mustard": '\033[38;2;242;182;128m',
    "floki_red": '\033[38;2;217;95;118m',
    "floki_pink": '\033[38;2;191;69;126m',
    "floki_purple": '\033[38;2;146;94;130m',
    "reset": Style.RESET_ALL
}

class ColorTextFormatter:
    """
    A flexible text formatter class to print colored text dynamically.
    Supports custom colors and text structures.
    """

    def __init__(self, default_color: Optional[str] = "reset"):
        """
        Initialize the formatter with a default color.

        Args:
            default_color (Optional[str]): Default color to use for text. Defaults to reset.
        """
        self.default_color = COLORS.get(default_color, COLORS["reset"])

    def format_text(self, text: str, color: Optional[str] = None) -> str:
        """
        Format text with the specified color.

        Args:
            text (str): The text to be formatted.
            color (Optional[str]): The color to apply (by name). Defaults to the default color.

        Returns:
            str: Colored text.
        """
        color_code = COLORS.get(color, self.default_color)
        return f"{color_code}{text}{COLORS['reset']}"
    
    def print_colored_text(self, text_blocks: list[tuple[str, Optional[str]]]):
        """
        Print multiple blocks of text in specified colors dynamically, ensuring that newlines
        are handled correctly.

        Args:
            text_blocks (list[tuple[str, Optional[str]]]): A list of text and color name pairs.
        """
        for text, color in text_blocks:
            # Split the text by \n to handle each line separately
            lines = text.split("\n")
            for i, line in enumerate(lines):
                formatted_line = self.format_text(line, color)
                print(formatted_line, end="\n" if i < len(lines) - 1 else "")
        
        print(COLORS['reset'])  # Ensure terminal color is reset at the end
    
    def print_separator(self):
        """
        Prints a separator line.
        """
        separator = "-" * 80
        self.print_colored_text([(f"\n{separator}\n", "reset")])
    
    def print_message(self, message: Union[BaseMessage, Dict[str, Any]], include_separator: bool = True):
        """
        Prints messages with colored formatting based on the role and message content.

        Args:
            message (Union[BaseMessage, Dict[str, Any]]): The message content, either as a BaseMessage object or 
                                                        a dictionary. If a BaseMessage is provided, it will be 
                                                        converted to a dictionary using its `model_dump` method.
            include_separator (bool): Whether to include a separator line after the message. Defaults to True.
        """
        # If message is a BaseMessage object, convert it to dict
        if isinstance(message, BaseMessage):
            message = message.model_dump()

        role = message.get("role")
        content = message.get("content", "")
        
        color_map = {
            "user": "floki_mustard",
            "assistant": "floki_teal",
            "tool_calls": "floki_red",
            "tool": "floki_pink"
        }

        # Handle tool calls
        if "tool_calls" in message and message["tool_calls"]:
            tool_calls = message["tool_calls"]
            for tool_call in tool_calls:
                function_name = tool_call["function"]["name"]
                arguments = tool_call["function"]["arguments"]
                tool_id = tool_call["id"]
                tool_call_text = [
                    (f"{role}(tool_call):\n", color_map["tool_calls"]),
                    (f"Function name: {function_name} (Call Id: {tool_id})\n", color_map["tool_calls"]),
                    (f"Arguments: {arguments}", color_map["tool_calls"]),
                ]
                self.print_colored_text(tool_call_text)
                if include_separator:
                    self.print_separator()

        elif role == "tool":
            # Handle tool messages
            tool_call_id = message.get("tool_call_id", "Unknown")
            tool_message_text = [
                (f"{role}(Id: {tool_call_id}):\n", color_map["tool"]),
                (f"{content}", color_map["tool"]),
            ]
            self.print_colored_text(tool_message_text)
            if include_separator:
                self.print_separator()

        else:
            # Handle regular user or assistant messages
            regular_message_text = [
                (f"{role}:\n", color_map.get(role, "reset")),
                (f"{content}", color_map.get(role, "reset")),
            ]
            self.print_colored_text(regular_message_text)
            if include_separator:
                self.print_separator()
    
    def print_react_part(self, part_type: str, content: str):
        """
        Prints a part of the ReAct loop (Thought, Action, Observation) with the corresponding color.

        Args:
            part_type (str): The part of the loop being printed (e.g., 'Thought', 'Action', 'Observation').
            content (str): The content to print.
        """
        color_map = {
            "Thought": "floki_red",
            "Action": "floki_pink",
            "Observation": "floki_purple"
        }

        # Get the color for the part type, defaulting to reset if not found
        color = color_map.get(part_type, "reset")

        # Print the part with the specified color
        self.print_colored_text([(f"{part_type}: {content}", color)])

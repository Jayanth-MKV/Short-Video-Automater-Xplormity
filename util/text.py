def format_text(text, max_chars_per_line):
    # Split the text into words
    words = text.split()
    
    # Initialize an empty list to store the formatted lines
    formatted_lines = []
    
    # Initialize the current line and its length
    current_line = []
    current_length = 0
    
    for word in words:
        if current_length + len(word) + len(current_line) <= max_chars_per_line:
            # If adding the word doesn't exceed the max length, add it to the current line
            current_line.append(word)
            current_length += len(word)
        else:
            # If the current line is not empty, add it to the formatted lines
            if current_line:
                formatted_lines.append(" ".join(current_line))
            # Start a new line with the current word
            current_line = [word]
            current_length = len(word)
    
    # Add the last line if there are words left
    if current_line:
        formatted_lines.append(" ".join(current_line))
    
    # Balance lines to have almost equal width
    balanced_lines = []
    current_line = formatted_lines[0]
    for next_line in formatted_lines[1:]:
        if len(current_line) + 1 + len(next_line) <= max_chars_per_line:
            current_line += " " + next_line
        else:
            balanced_lines.append(current_line)
            current_line = next_line
    balanced_lines.append(current_line)
    
    return balanced_lines
def get_input(prompt):
    """
    Get user input with a prompt.
    """
    return input(prompt)

def display_message(message):
    """
    Display a message to the user.
    """
    print(message)

def clear_console():
    """
    Clear the console screen.
    """
    import os
    os.system('cls' if os.name == 'nt' else 'clear')
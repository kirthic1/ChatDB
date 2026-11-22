total_tokens = 0

#Standard/Built-in python library
from datetime import datetime

def add_tokens(n:int) -> None:
    """
    A function to add n tokens to the total_tokens variable as llm model is used during the user session
    :param n: n is the number of tokens that we should add to the total_tokens variable
    :return: None
    """
    global total_tokens
    total_tokens += n

def return_total_tokens() -> int:
    """
    A function to return the total_tokens variable value
    :return: total_tokens value
    """
    global total_tokens
    return total_tokens

def save_session_token_log() -> None:
    """
    A function to save the total tokens value per user session into a file
    :return: None
    """
    with open("token_usage_log.csv", "a") as f:
        timestamp = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        tokens = return_total_tokens()
        f.write(f"{timestamp},{tokens}\n")
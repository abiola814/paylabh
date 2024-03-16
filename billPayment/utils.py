# utils.py (create a new file for utility functions)

from user.models import User

def check_transaction_pin(user, transaction_pin):
    # Check if the provided transaction pin matches the user's actual transaction pin
    return user.transaction_pin == transaction_pin

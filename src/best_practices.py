import logging
from typing import List, Tuple

# Logging configuration
logging.basicConfig(level=logging.DEBUG,
                   format='%(asctime)s %(levelname)s %(message)s')

# Constants
MIN_LENGTH = 8

# Function to check password strength
def check_password_strength(password: str) -> Tuple[bool, str]:
   """
   Check the strength of a password and return a tuple indicating whether the password is strong enough
   and a message indicating the reasons if it's not strong enough.
   """
   # Check password length
   if len(password) < MIN_LENGTH:
       return (False, f"Password must be at least {MIN_LENGTH} characters long.")

   # Check if password contains a digit
   if not any(char.isdigit() for char in password):
       return (False, "Password must contain at least one digit.")

   # Check if password contains an uppercase letter
   if not any(char.isupper() for char in password):
       return (False, "Password must contain at least one uppercase letter.")

   # Check if password contains a lowercase letter
   if not any(char.islower() for char in password):
       return (False, "Password must contain at least one lowercase letter.")

   return (True, "Password is strong.")

# Function to validate passwords
def validate_passwords(passwords: List[str]) -> None:
   """
   Validate a list of passwords and log the results.
   """
   for password in passwords:
       is_strong, message = check_password_strength(password)
       if is_strong:
           logging.info(f"Password '{password}' is strong.")
       else:
           logging.warning(f"Password '{password}' is weak. Reason: {message}")

# Test data
passwords = ['Password123', 'password123', 'password', 'P@ssword123']

# Main function
def main():
   validate_passwords(passwords)

# Entry point
if __name__ == "__main__":
   main()


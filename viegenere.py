import argparse
from collections.abc import Callable
from math import ceil, floor

# There exist special cases (variants) of Vigenère which are called Autokey, Beaufort,
# Gronsfeld, Porta, and Trithemius, whose algorithms are implemented separately below.

# Function to run the original Vigenère algorithm
def run_vigenere(message:str, key:str, alphabet:str, operation:Callable[[int, int], int]):
  # Repeat key until it has the same length as the message
  key_numbers = []
  for i in range(len(message)):
    # Get the letter of the key at the current position (% repeats the key)
    key_letter = key[i % len(key)]
    # Convert the key letter into a number (based on the character's position in the alphabet)
    key_number = alphabet.index(key_letter)
    # Add the number to the list
    key_numbers.append(key_number)
  # Use a list comprehension to convert message into numbers (based on the character's position in the alphabet)
  message_numbers = [alphabet.index(char) for char in message]
  # Return applied Vigenère operation
  return apply_operation(message_numbers, key_numbers, operation, alphabet)


# Function to run the Autokey algorithm (variant of Vigenère)
def run_autokey(message:str, key:str, alphabet:str, operation:Callable[[int, int], int]):
  # Add message to the end of key and trim to the correct length
  combined_key = (key + message)[0:len(message)]
  # Convert the combined key into numbers
  key_numbers = []
  for key_letter in combined_key:
    # Convert the key letter into a number (based on the character's position in the alphabet)
    key_number = alphabet.index(key_letter)
    # Add the number to the list
    key_numbers.append(key_number)
  # Use a list comprehension to convert message into numbers
  message_numbers = [alphabet.index(char) for char in message]
  # Return applied Vigenère operation
  return apply_operation(message_numbers, key_numbers, operation, alphabet)


# Function to run the Gronsfeld algorithm (variant of Vigenère)
def run_gronsfeld(message:str, key:str, alphabet:str, operation:Callable[[int, int], int]):
  # Convert the combined key into numbers
  key_numbers = [int(n) for n in key]
  # Use a list comprehension to convert message into numbers
  message_numbers = [alphabet.index(char) for char in message]
  # Return applied Vigenère operation
  return apply_operation(message_numbers, key_numbers, operation, alphabet)


# Function to run the Porta algorithm (variant of Vigenère)
def run_porta(message:str, key:str, alphabet:str):
  # Repeat key until it has the same length as the message
  key_numbers = []
  for i in range(len(message)):
    # Get the letter of the key at the current position (% repeats the key)
    key_letter = key[i % len(key)]
    # Convert the key letter into a number (based on the character's position in the alphabet)
    key_number = alphabet.index(key_letter)
    # Add the number to the list
    key_numbers.append(key_number)
  # Convert the message letters into numbers (based on the character's position in the alphabet)
  result = ""
  for index,char in enumerate(message):
    char_number = alphabet.index(char)
    key_number = key_numbers[index]
    # Ignore characters that did not appear in the alphabet
    if char_number < 0 or key_number < 0:
      continue
    # Split the alphabet in two halves to alter the resulting numbers
    # (that's Porta specific) depending on the current key number
    first_half,second_half = splitAlphabet(key_number, alphabet)
    if char in first_half:
      result += second_half[first_half.index(char)]
    if char in second_half:
      result += first_half[second_half.index(char)]
  return result


# Function to generally execute an operation for all Vigenère variants
def apply_operation(message:list[int], key:list[int], operation:Callable[[int, int], int], alphabet:str):
  # Perform encryption or decryption (by using the operation)
  result = ""
  # Use enumerate to get the index in a loop
  for char_index, char_number in enumerate(message):
    key_number = key[char_index % len(key)]
    if char_number >= 0 and key_number >= 0:
      alphabet_number = operation(char_number, key_number) % len(alphabet)
      result += alphabet[alphabet_number]
  return result

# Function to produce split alphabet for Porta algorithm
def splitAlphabet(key_index:int, alphabet:str):
  # Half the length of the alphabet string
  half_len = ceil(len(alphabet)/2)
  # First half of the alphabet
  first_half = alphabet[0:half_len]
  # Second half of the alphabet which is shifted to the right by half of the key_index
  second_half = alphabet[half_len:len(alphabet)]
  half_key_index = floor(key_index/2)
  shifted_second_half = ""
  for i,c in enumerate(second_half):
    shifted_second_half += second_half[(half_key_index + i) % half_len]
  return (first_half, shifted_second_half)

# Function for encrypting
def encrypt(message, key, variant, alphabet):
  # Standard Vigenère encryption ADDs the key and character
  operation = lambda char_num, key_num: char_num + key_num

  # Execute the selected algorithm variant
  match variant:
    case 'porta':
      return run_porta(message, key, alphabet)
    case 'gronsfeld':
      return run_gronsfeld(message, key, alphabet, operation)
    case 'autokey':
      return run_autokey(message, key, alphabet, operation)
    case 'beaufort':
      # Beaufort encryption subtracts the character from the key
      operation = lambda char_num, key_num: key_num - char_num
      return run_vigenere(message, key, alphabet, operation)
    case _:
      return run_vigenere(message, key, alphabet, operation)

# Function for decrypting
def decrypt(message, key, variant, alphabet):
  # Encrypt operation SUBTRACTs the key
  operation = lambda char_num, key_num: char_num - key_num

  # Execute the selected algorithm variant
  match variant:
    case 'porta':
      return run_porta(message, key, alphabet)
    case 'gronsfeld':
      return run_gronsfeld(message, key, alphabet, operation)
    case 'autokey':
      return run_autokey(message, key, alphabet, operation)
    case 'beaufort':
      # Beaufort decryption is simple addition
      operation = lambda char_num, key_num: key_num + char_num
      return run_vigenere(message, key, alphabet, operation)
    case _:
      return run_vigenere(message, key, alphabet, operation)

if __name__ == '__main__':

  # ArgumentParser with description and examples
  parser = argparse.ArgumentParser(
      description="Vigenère Cipher encryption/decryption tool.",
      epilog="""Examples:
    - Encrypt a message:
      python VigenereAlgorithm.py --encrypt --message='FRANZJAGTIMKOMPLETTVERWAHRLOSTENTAXIQUERDURCHBAYERN' --variant='vigenère' --key='ABCDE' --alphabet='ABCDEFGHIJKLMNOPQRSTUVWXYZ'

    - Show help:
      python VigenereAlgorithm.py --help
      """,
      formatter_class=argparse.RawTextHelpFormatter  # Keeps line breaks in the epilog
  )

  # Parse the arguments (args) given via the command line
  encryptDecryptGroup = parser.add_mutually_exclusive_group(required=True)
  encryptDecryptGroup.add_argument("-e", "--encrypt", dest="encrypt_or_decrypt", action="store_true")
  encryptDecryptGroup.add_argument("-d", "--decrypt", dest="encrypt_or_decrypt", action="store_false")
  parser.add_argument("-m", "--message", help="message for encrypt / decrypt", required=True, type=str)
  parser.add_argument("-k", "--key", help="key for encrypt / decrypt", required=True, type=str)
  parser.add_argument("-v", "--variant", help="Vigenère variant to use", required=True, type=str)
  parser.add_argument("-a", "--alphabet", help="defined alphabet", required=True, type=str)
  args = parser.parse_args()

  # If --encrypt flag -> call encrypt function
  if(args.encrypt_or_decrypt == True):
    print(encrypt(args.message, args.key, args.variant, args.alphabet))

  # If --decrypt flag -> call decrypt function
  else:
    print(decrypt(args.message, args.key, args.variant, args.alphabet))

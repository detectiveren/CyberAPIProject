# Name: Eduardo Manuel Costa Moreira
# Student ID: MOR21500097
# Date: 31/01/2024
from cryptography.fernet import Fernet


def decryptData(user_key, user_token):
    try: # Attempt to put key into Fernet
        data_key = Fernet(user_key)  # Inserts the key into Fernet
        token_decrypted = data_key.decrypt(user_token)  # Decrypts the token using the key
        return token_decrypted
    except: # If the token / key is invalid print to the user that it is invalid
        print("INVALID TOKEN/KEY")
        return "The data could not be decrypted due to a false token / key"
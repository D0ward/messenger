import encryption
from socket import socket

class Session:

    def __init__(self) -> None:
        p_key1, p_key2 = encryption.create_public_keys()

        self.human1 = encryption.Encryption(p_key1, p_key2)
        self.human2 = encryption.Encryption(p_key1, p_key2)

        part_key1 = self.human1.create_partial_key()
        part_key2 = self.human2.create_partial_key()
    
        self.human1.create_full_key(part_key2)
        self.human2.create_full_key(part_key1)
        
    def send_message(self, message: str, sender: bool):
        if sender:
            encrypted_message = self.human1.encrypt_message(message)
        else:
            encrypted_message = self.human2.encrypt_message(message)

    def get_message(self, human2: encryption.Encryption, encrypted_message: str):
        decrypted_message = self.human2.decrypt_message(encrypted_message)
        
from random import randint

prime_numbers = [983, 991, 997, 1009, 1013, 1019, 1021, 1031, 1033, 1039, 1049, 1051, 1061,	1063, 1069, 1087, 1091, 1093, 1097, 1103, 1109, 1117, 1123, 1129, 1151, 1153, \
                1163, 1171,	1181, 1187, 1193, 1201, 1213, 1217, 1223, 1229, 1231, 1237,	1249, 1259,	1277, 1279,	1283, 1289, 1291, 1297, 1301, \
            	1303, 1307,	1319, 1321,	1327, 1361, 1367, 1373, 1381, 1399,	1409, 1423,	1427, 1429,	1433, 1439,	1447, 1451,	1453, 1459, 1471, 1481, 1483]

class Encryption:

    def __init__(self, public_key1: int = 0, public_key2: int = 0) -> None:
        self.public_key1 = public_key1
        self.public_key2 = public_key2
        self.private_key = randint(10000, 100000)

    def set_public_keys(self, public_key1: int, public_key2: int) -> None:
        self.public_key1 = public_key1
        self.public_key2 = public_key2

    def create_partial_key(self) -> int:
        return pow(self.public_key1, self.private_key, self.public_key2)

    def create_full_key(self, partial_key: int) -> None:
        self.full_key = pow(partial_key, self.private_key, self.public_key2)

    def encrypt_message(self, message: str) -> str:
        encrypted_message = ''
        key = self.full_key
        for s in message:
            encrypted_message += chr(ord(s) + key)
        return encrypted_message

    def decrypt_message(self, message: str) -> str:
        decrypted_message = ''
        key = self.full_key
        for s in message:
            decrypted_message += chr(ord(s) - key)
        return decrypted_message
    
    

def create_public_keys():
    return prime_numbers[randint(0, len(prime_numbers) - 1)], prime_numbers[randint(0, len(prime_numbers) - 1)]

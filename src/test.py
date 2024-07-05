import encryption
from random import randint
def test1():
    p_key1, p_key2 = encryption.create_public_keys()

    human1 = encryption.Encryption(p_key1, p_key2)
    human2 = encryption.Encryption(p_key1, p_key2)

    
    #print('Public keys\n', p_key1, p_key2)


    part_key1 = human1.create_partial_key()
    part_key2 = human2.create_partial_key()
    #print('Partial keys\n', human1.partial_key, human2.partial_key)

    human1.create_full_key(part_key2)
    human2.create_full_key(part_key1)
    #print('Full keys\n', human1.full_key, human2.full_key)

    message = 'Hello world'

    #print('Message:', message)

    encrypt_message = human1.encrypt_message(message)
    #print('Encrypt_message:', encrypt_message)

    decrypt_message = human2.decrypt_message(encrypt_message)
    #print('Decrypt_message:', decrypt_message)

    if message == decrypt_message:
        print('Good')
    else:
        print('Public keys\n', p_key1, p_key2)
        print('Partial keys\n', human1.partial_key, human2.partial_key)
        print('Full keys\n', human1.full_key, human2.full_key)
        print('Message:', message)
        print('Encrypt_message:', encrypt_message)
        print('Decrypt_message:', decrypt_message)
        print('Bad')

for _ in range(5):
    test1()
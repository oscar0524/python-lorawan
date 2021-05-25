from Crypto.Hash import CMAC
from Crypto.Cipher import AES


def aesEncrypt(key, data, mode=None):
    """AES encryption function

    Args:
        key (str): packed 128 bit key
        data (str): packed plain text data
        mode (str): Optional mode specification (CMAC)

    Returns:
        Packed encrypted data string
    """
    if mode == 'CMAC':
        # Create AES cipher using key argument, and encrypt data
        return CMAC.new(key, msg=data, ciphermod=AES).digest()
    elif mode == None:
        return AES.new(key, AES.MODE_ECB).encrypt(data)


def aesDecrypt(key, data):
    """AES decryption fucnction

    Args:
        key (str): packed 128 bit key
        data (str): packed encrypted data

    Returns:
        Packed decrypted data string
    """
    return AES.new(key, AES.MODE_ECB).decrypt(data)

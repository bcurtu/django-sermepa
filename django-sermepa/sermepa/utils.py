# -*- encoding: utf-8 -*-
import hashlib, json, base64, hmac
from Crypto.Cipher import DES3
from django.conf import settings


"""
    Method to generate Ds_MerchantParameters & Ds_Signature needed by Redsys

    @var merchant_parameters: Dict with all merchant parameters
    @return Ds_MerchantParameters: Redsys ready encoded parameters
    @return Ds_Signature: Redsys 256 valid signature
"""
def redsys_generate_request(merchant_parameters):
    Ds_MerchantParameters = encode_parameters(merchant_parameters)
    order_encrypted = encrypt_order_with_3DES(merchant_parameters['Ds_Merchant_Order'])
    Ds_Signature = sign_hmac256(order_encrypted, Ds_MerchantParameters)

    return Ds_MerchantParameters, Ds_Signature



"""
    Method to check received Ds_Signature with the one we extract from Ds_MerchantParameters data.
    We remove non alphanumeric characters before doing the comparison

    @return Ds_Signature: Received signature
    @return Ds_MerchantParameters: Received parameters
    @return: True if signature is confirmed, False if not 
"""
def redsys_check_response(Ds_Signature, Ds_MerchantParameters):
    import re

    merchant_parameters = decode_parameters(Ds_MerchantParameters)
    order = merchant_parameters['Ds_Order']
    order_encrypted = encrypt_order_with_3DES(order)
    Ds_Signature_calculated = sign_hmac256(order_encrypted, Ds_MerchantParameters)

    alphanumeric_characters = re.compile('[^a-zA-Z0-9]')
    Ds_Signature_safe = re.sub(alphanumeric_characters, '', Ds_Signature)
    Ds_Signature_calculated_safe = re.sub(alphanumeric_characters, '', Ds_Signature_calculated)
    if Ds_Signature_safe  == Ds_Signature_calculated_safe:
        return True
    else:
        return False



"""
    Given a dict; create a json object, codify it in base64 and delete their carrier returns

    @var merchant_parameters: Dict with all merchant parameters
    @return Ds_MerchantParameters: Encoded json structure with all parameters
"""
def encode_parameters(merchant_parameters):
    parameters = (json.dumps(merchant_parameters)).encode()
    return ''.join(unicode(base64.encodestring(parameters), 'utf-8').splitlines())



"""
    Given the Ds_MerchantParameters from Redsys, decode it and eval the json file

    @var Ds_MerchantParameters: Encoded json structure returned from Redsys
    @return merchant_parameters: Json structure with all parameters 
"""
def decode_parameters(Ds_MerchantParameters):
    import ast

    Ds_MerchantParameters_decoded = base64.standard_b64decode(Ds_MerchantParameters)
    return ast.literal_eval(Ds_MerchantParameters_decoded)



"""
    This method creates a unique key for every request, 
    based on the Ds_Merchant_Order and in the shared secret (SERMEPA_SECRET_KEY).
    This unique key is Triple DES ciphered.
    @var merchant_parameters: Dict with all merchant parameters
    @return order_encrypted: The encrypted order
"""
def encrypt_order_with_3DES(Ds_Merchant_Order):
    pycrypto = DES3.new(base64.standard_b64decode(settings.SERMEPA_SECRET_KEY), DES3.MODE_CBC, IV=b'\0\0\0\0\0\0\0\0')
    order_padded = Ds_Merchant_Order.ljust(16, b'\0')
    return pycrypto.encrypt(order_padded)



"""
    Use the order_encrypted we have to sign the merchant data using a HMAC SHA256 algorithm 
    and encode the result using Base64
    @var order_encrypted: Encrypted Ds_Merchant_Order
    @var Ds_MerchantParameters: Redsys aleready encoded parameters
    @return Ds_Signature: Generated signature encoded in base64
"""
def sign_hmac256(order_encrypted, Ds_MerchantParameters):
    hmac_value = hmac.new(order_encrypted, Ds_MerchantParameters, hashlib.sha256).digest()
    return base64.b64encode(hmac_value)



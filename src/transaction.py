from collections import OrderedDict

import binascii
import json
import hashlib

import Crypto
import Crypto.Random
from Crypto.Hash import SHA
from Crypto.PublicKey import RSA
from Crypto.Signature import PKCS1_v1_5

import requests
from flask import Flask, jsonify, request, render_template

class Transaction:

    def __init__(self, sender_address, sender_private_key, recipient_address, value, transaction_inputs, sum):
        self.sender_address = sender_address
        self.receiver_address = recipient_address
        self.value = value
        self.transaction_inputs = transaction_inputs
        self.transaction_id = self.compute_id()
        self.transaction_outputs = [{'value': self.value,   # receiver
                                    'address': self.receiver_address,
                                    'transaction_id': self.transaction_id},
                                    {'value': sum - self.value, # sender RESTA
                                    'address': self.sender_address,
                                    'transaction_id': self.transaction_id}]
        self.signature = ""

    def compute_id(self):
        #calculate self.id which is the hash value of some fields
        temp = {'sender_address': self.sender_address, 'receiver_address': self.receiver_address, 'value': self.value, 'transaction_inputs' : self.transaction_inputs}
        string = json.dumps(temp, sort_keys=True).encode()
        self.id = hashlib.sha224(string).hexdigest()
        return self.id

    def to_dict(self):
        return OrderedDict({'sender_address': self.sender_address, 'receiver_address': self.receiver_address, 'value': self.value, 'transaction_id': self.transaction_id, 'transaction_inputs' : self.transaction_inputs, 'transaction_outputs': self.transaction_outputs, 'signature' : self.signature})

    def sign_transaction(self):
        """
        Sign transaction with private key
        """
        private_key = RSA.importKey(binascii.unhexlify(self.sender_private_key))
        signer = PKCS1_v1_5.new(private_key)
        mydict = OrderedDict({
            'sender_address': self.sender_address, 
            'receiver_address': self.receiver_address, 
            'value': self.value, 
            'itransaction_id': self.transaction_id, 
            'transaction_inputs' : self.transaction_inputs, 
            'transaction_outputs': self.transaction_outputs
            })
        h = SHA.new(str(mydict).encode('utf8'))
        self.signature = binascii.hexlify(signer.sign(h)).decode('ascii')
        return self


        #h = SHA.new(str(self.to_dict()).encode('utf8'))
        #return binascii.hexlify(signer.sign(h)).decode('ascii')
        
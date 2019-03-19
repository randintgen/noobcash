import sys
import hashlib
import json
from time import time
from urllib.parse import urlparse
from uuid import uuid4
#import wallet
import block
import myblockchain

import requests
from flask import Flask, jsonify, request



class node:
    def __init__(self, bootstrap, number_of_nodes):
        self.number_of_nodes = number_of_nodes
        self.chain=myblockchain.Blockchain()
        self.current_id_count = 0
        #self.wallet = wallet.wallet()
        self.ring = ["http://0.0.0.0:5000"]
        if (bootstrap == "0"):
            self.node_id = 0
            self.chain.create_genesis(self.number_of_nodes, self.ring[0]) # 100 *number_of_nodes from wallet 0   
        else:
            self.register_self()    

    def send_init_info(self, i, address): # used by bootstrap to send node id and ring
        message = {
            'node_id': i,
            'ring': self.ring
        }
        print (message)
        r = requests.post(address + '/nodes/register_ack', data = message)
        
        print (r)
        return self
    
    def receive_init_info(self, i, ring):
        self.ring = copy.deepcopy(ring)
        self.node_id = i

    def register_self(self): # used by others to register their self to bootstrap
        message = {
            'address' : "http://0.0.0.0:5001"
        }
        print(self.ring[0] + "/nodes/register")
        r= requests.post(self.ring[0] + "/nodes/register", data = message)
        print(message)
        print(r)
        return r

    def register_node(self, address): # used by boostrap to handle incoming registers
        self.ring.append(address)
        self.current_id_count = self.current_id_count + 1
        if (self.current_id_count == self.number_of_nodes):
            print("yes")
            for i, address in enumerate(self.ring[1:]):
                self.send_init_info(i+1, address)
            for address in self.ring[1:]:
                continue
                # self.add_transaction(...)

    def create_new_block():
        print(1)


    def create_transaction(sender, receiver, signature):
    #remember to broadcast it
        print(1)


    def broadcast_transaction():
        print(1)


    def validdate_transaction():
    #use of signature and NBCs balance
        print(1)


    def add_transaction_to_block():
    #if enough transactions  mine
        print(1)



    def mine_block():
        print(1)



    def broadcast_block():
        print(1)




    #def valid_proof(.., difficulty=MINING_DIFFICULTY):
      #	print(1)

        #concencus functions

    def valid_chain(self, chain):
        #check for the longer chain accroose all nodes
        print(1)


    def resolve_conflicts(self):
        #resolve correct chain
        print(1)

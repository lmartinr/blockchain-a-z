#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Fri Sep 30 17:12:13 2022

@author: lmartinr
"""

# Módulo 1 - Crear una Cadena de Bloques

# Para instalar:
# Flask==0.12.2: pip install Flask==0.12.2
# Cliente HTTP Postman: https://www.getpostman.com/

# Importar las librerías
import datetime    # libreria para manejo de fechas y horas
import hashlib     # libreria de hash 
import json        # libreria para el manejo de objetos json
from flask import Flask, jsonify  # el primero es el constructor y el segundo es para convertir a json


# Parte 1 - Crear la Cadena de Bloques
class Blockchain:
    
    def __init__(self):
        self.chain = []       # aqui es donde almacenamos la cadena
        self.create_block(proof = 1, previous_hash = '0')


    def create_block(self, proof, previous_hash):
        block = {'index' : len(self.chain)+1,
                 'timestamp' : str(datetime.datetime.now()),
                 'proof' : proof,
                 'previous_hash' : previous_hash}
        self.chain.append(block)
        return block
    

    def get_previous_block(self):
        return self.chain[-1]       # esto devuelve el último eslabón de la cadena


    def proof_of_work(self, previous_proof):
        new_proof = 1
        check_proof = False
        while check_proof is False:
            #esto puede ser cualquier fórmula siempre que no sea simétrica, es decir A operacion B debe ser diferente que B operacion A
            #el parametro debe ser un string codificado en binario, por eso usamos el .encode
            #el resultado lo pasamos a hexadecimal para poder ver el numero de 0 que hay al principio
            hash_operation = hashlib.sha256(str(new_proof**2 - previous_proof**2).encode()).hexdigest()  
            
            if hash_operation[:4] == '0000':   # esto comprueba los primeros caracteres del hash obtenido
                check_proof = True
            else:
                new_proof += 1    # esto podría ser algo random
                
        return new_proof    
        

    def hash(self, block):
        encoded_block = json.dumps(block, sort_keys=True).encode() # el segundo parametro es importante para asegurar que el diccionario siempre se convierte de la misma forma
        return hashlib.sha256(encoded_block).hexdigest()
    
    
    def is_chain_valid(self, chain):
        previous_block = chain[0]
        block_index = 1
        while block_index < len(chain):
            current_block = chain[block_index]
            #primera validación
            if current_block['previous_hash'] != self.hash(previous_block):
                return False
            
            current_proof = current_block['proof']
            previous_proof = previous_block['proof']
            hash_operation = hashlib.sha256(str(current_proof**2 - previous_proof**2).encode()).hexdigest()
            #segunda validación
            if hash_operation[:4] != '0000':
                return False
            #actualizamos las variables del bloque
            previous_block = current_block
            block_index += 1
        
        return True  #si hemos pasado por toda la cadena y no ha dado error, es que la cadena es válida
        
        
# Parte 2 - Minado de un Bloque de la Cadena

# Primero vamos a crear una aplicación web con Flask
app = Flask(__name__)
# Si se obtiene un error 500, actualizar Flask, reiniciar spyder y ejecutar la siguiente línea
#app.config['JSONIFY_PRETTYPRINT_REGULAR'] = False

# Y ahora creamos una cadena de bloques - Blockchain
blockchain = Blockchain()


# Ahora vamos a hacer el minado de datos
@app.route("/mine_block", methods=['GET'])   #por delante de la barra / irá la URL base
# el @app.route puede tener otro parametro que es el Método, que podria ser GET (para leer) o POST (para actualizar)

def mine_block():  #le podria haber puesto cualquier otro nombre
    previous_block = blockchain.get_previous_block()
    previous_proof = previous_block['proof']
    current_proof = blockchain.proof_of_work(previous_proof)
    previous_hash = blockchain.hash(previous_block)
    current_block = blockchain.create_block(current_proof, previous_hash)

    response = {'message' : 'Enhorabuena, has minado un nuevo bloque!',
                'index' : current_block['index'],
                'timestamp': current_block['timestamp'],
                'proof' : current_block['proof'],
                'previous_hash' : current_block['previous_hash']
                }
    
    return jsonify(response), 200   # el 200 es el codigo de resultado http, y significa que todo ha ido OK


# Ahora obtenemos la cadena de bloques al completo
@app.route("/get_chain", methods=['GET'])   #por delante de la barra / irá la URL base

def get_chain():
    response = {'chain' : blockchain.chain,
                'length' : len(blockchain.chain)
        }
    
    return jsonify(response), 200


# Ahora añadimos el metodo is_valid
@app.route("/is_valid", methods=['GET'])   #por delante de la barra / irá la URL base

def is_valid():
    if blockchain.is_chain_valid(blockchain.chain):
        response = {'message' : 'Genial, la cadena es válida!'}
    else:
        response = {'message' : 'Lo siento, la cadena no es válida!'}

    return jsonify(response), 200



# Ejecutar la app

app.run(host = '0.0.0.0', port = 5000)






















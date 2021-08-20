
# importaciones
import hashlib
import datetime
import json
import pprint
from time import time


# Clase de Bloque
class Block:

    # construtor
    def __init__(self, timeStamp, transactions, previousBlock=''):
        self.timeStamp = timeStamp
        self.transactions = transactions
        self.previousBlock = previousBlock
        self.difficultyIncrement = 5
        self.hash = self.calculateHash(
            transactions, timeStamp, self.difficultyIncrement)

    # Funcion para calcular el hash de un bloque
    def calculateHash(self, transactions, timeStamp, difficultyIncrement):
        data = str(transactions) + str(timeStamp) + str(difficultyIncrement)
        data = data.encode()
        hash = hashlib.sha256(data).hexdigest()
        return hash

    # funcion para el minado de bloques

    def mineBlock(self, difficultyIncrement):

        difficultyChecks = "0" * difficultyIncrement
        while(self.hash[:difficultyIncrement] != difficultyChecks):
            self.hash = self.calculateHash(
                self.transactions, self.timeStamp, self.difficultyIncrement)
            self.difficultyIncrement += 1

# Clase de blockchain


class Blockchain:

    # constructor
    def __init__(self):
        self.chain = [self.GenesisBlock()]
        self.difficultyIncrement = 5
        self.pendingTransactions = []
        self.reward = 20

    # funcion para crear el primer bloque  bloque a la cadena
    def GenesisBlock(self):
        genesisBlock = Block(str(datetime.datetime.now()),
                             "Soy el Bloque 0 de la Cadena de Bloques")
        return genesisBlock

    # funcion para obtener el ultimo bloque de la cadena
    def getLastBlock(self):
        return self.chain[len(self.chain) - 1]

    def minePendingTransactions(self, minerRewardAddress):

        newblock = Block(str(datetime.datetime.now()),
                         self.pendingTransactions)

        newblock.mineBlock(self.difficultyIncrement)
        newblock.previousBlock = self.getLastBlock().hash
        print(f"Hash del bloque previo: {newblock.previousBlock}")

        testchain = []
        for trans in newblock.transactions:
            temp = json.dumps(trans.__dict__, indent=5, separators=(',', ':'))
            testchain.append(temp)

        pprint.pprint(testchain)

        self.chain.append(newblock)
        print(f"Hash del bloque: {newblock.hash}")
        print("¡NUEVO BLOQUE AÑADIDO!")

        rewardTrans = Transaction("Sistema", minerRewardAddress, self.reward)
        self.pendingTransactions.append(rewardTrans)
        self.pendingTransactions = []

    def isChainValid(self):
        for x in range(1, len(self.chain)):
            currentBlock = self.chain[x]
            previousBlock = self.chain[x-1]

            if (currentBlock.previousBlock != previousBlock.hash):
                print("La cadena no es válida!")

        print("¡La cadena es válida y segura!")

    def createTransaccion(self, transaction):
        self.pendingTransactions.append(transaction)

    def getBalance(self, walletAddress):
        balance = 0
        for block in self.chain:
            if block.previousBlock == "":
                continue
            for transaction in block.transactions:
                print("walletAddress", walletAddress)
                print("transaction.fromWallet", transaction.fromWallet)
                print("transaction.fromWallet", transaction.toWallet)

                if transaction.fromWallet == walletAddress:
                    balance -= transaction.amount
                if transaction.toWallet == walletAddress:
                    balance += transaction.amount
        return balance

# Clase de transaccion


class Transaction:

    # construtor
    def __init__(self, fromWallet, toWallet, amount):
        self.fromWallet = fromWallet
        self.toWallet = toWallet
        self.amount = amount

# Zona de pruebas


my_crypto = Blockchain()

print("Junior Minero empezo a minar")
my_crypto.createTransaccion(Transaction("Mineria 1", "Junior 1", 0.1))
my_crypto.createTransaccion(Transaction("Mineria 2", "Junior 2", 0.1))
my_crypto.createTransaccion(Transaction("Junior 3", "Mineria 2", 0.1))
my_crypto.createTransaccion(Transaction("Junior 2", "Mineria 1", 0.1))
tiempo_inicio = time()
my_crypto.minePendingTransactions("JuniorMinero")
tiempo_final = time()
print(f"El tiempo de minado es de: {tiempo_final - tiempo_inicio}")


print("pedroMinero empezo a minar")
my_crypto.createTransaccion(Transaction("Mineria 1", "Junior 1", 0.1))
my_crypto.createTransaccion(Transaction("Mineria 2", "Junior 2", 0.1))
my_crypto.createTransaccion(Transaction("Junior 3", "Mineria 2", 0.1))
my_crypto.createTransaccion(Transaction("Junior 2", "Mineria 1", 0.1))
tiempo_inicio = time()
my_crypto.minePendingTransactions("pedroMinero")
tiempo_final = time()
print(f"El tiempo de minado es de: {tiempo_final - tiempo_inicio}")

print("anaMinero empezo a minar")
my_crypto.createTransaccion(Transaction("Mineria 1", "Junior 1", 0.1))
my_crypto.createTransaccion(Transaction("Mineria 2", "Junior 2", 0.1))
my_crypto.createTransaccion(Transaction("Junior 3", "Mineria 2", 0.1))
my_crypto.createTransaccion(Transaction("Junior 2", "Mineria 1", 0.1))
tiempo_inicio = time()
my_crypto.minePendingTransactions("anaMinero")
tiempo_final = time()
print(f"El tiempo de minado es de: {tiempo_final - tiempo_inicio}")



print('-'*20)
print("JuniorMinero tiene " +
      str(my_crypto.getBalance("JuniorMinero")) + " JoanCoins en su Wallet")
print("pedroMinero tiene " + str(my_crypto.getBalance("pedroMinero")) +
      " JoanCoins en su Wallet")
print("anaMinero tiene " + str(my_crypto.getBalance("anaMinero")) +
      " JoanCoins en su Wallet")
print('-'*20)

# Hash de los bloques de la cadena
for x in range(len(my_crypto.chain)):
    print(f"Hash del Bloque {x}: {my_crypto.chain[x].hash}")

print(my_crypto.isChainValid())

from web3 import Web3


def w3():
    return Web3(Web3.HTTPProvider('https://rpc.fantom.network/'))

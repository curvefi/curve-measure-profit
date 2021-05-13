from web3 import Web3


def w3():
    from web3.middleware import geth_poa_middleware
    w3 = Web3(Web3.HTTPProvider('https://polygon-mainnet.infura.io/v3/fac98e56ea7e49608825dfc726fab703'))
    # w3 = Web3(Web3.HTTPProvider('https://rpc-mainnet.maticvigil.com/v1/04b6f9e1657ce09ba6b2f73649eacf1c073972ba'))
    w3.middleware_onion.inject(geth_poa_middleware, layer=0)
    return w3

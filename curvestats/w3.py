from web3 import Web3


def w3():
    from web3.middleware import geth_poa_middleware
    w3 = Web3(Web3.HTTPProvider('https://api.avax.network/ext/bc/C/rpc'))
    w3.middleware_onion.inject(geth_poa_middleware, layer=0)
    return w3

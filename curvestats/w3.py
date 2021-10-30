from web3 import Web3


def w3():
    from web3.middleware import geth_poa_middleware
    # w3 = Web3(Web3.HTTPProvider('https://arbitrum-mainnet.infura.io/v3/fac98e56ea7e49608825dfc726fab703'))
    w3 = Web3(Web3.HTTPProvider('https://arb-mainnet.g.alchemy.com/v2/D5O-iVrTJhd_coUFfsPFrcX5RFaJ0LIa'))
    # w3 = Web3(Web3.HTTPProvider('https://arb1.arbitrum.io/rpc'))
    w3.middleware_onion.inject(geth_poa_middleware, layer=0)
    return w3

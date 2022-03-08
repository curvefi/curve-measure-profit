#!/usr/bin/env python3

import lmdb
import json
import time
from time import sleep
from multiprocessing import Pool
from functools import partial

from curvestats.tricrypto import Pool as CryptoPool
from curvestats.forexmeta import Pool as ForexPool
from curvestats.forex import Pool as ForexPlain
from curvestats.ethbase import Pool as EthPool

MPOOL_SIZE = 25

pools = {
        'tricrypto': (CryptoPool, ('0x80466c64868E1ab14a1Ddf27A676C3fcBE638Fe5', '0xcA3d75aC011BF5aD07a98d02f18225F9bD9A6BDF'), 12521539),
        'tricrypto2': (CryptoPool, ('0xD51a44d3FaE010294C616388b506AcdA1bfAAE46', '0xc4AD29ba4B3c580e6D59105FFf484999997675Ff'), 12821149),
        'eurtusd': (ForexPool, ('0x9838eCcC42659FA8AA7daF2aD134b53984c9427b', '0x3b6831c0077a1e44ED0a21841C3bC4dC11bCE833', '0xbEbc44782C7dB0a1A60Cb6fe97d0b483032FF1C7'), 13526620),
        'eursusd': (ForexPlain, ('0x98a7F18d4E56Cfe84E3D081B40001B3d5bD3eB8B', '0x3D229E1B4faab62F621eF2F6A610961f7BD7b23B'), 13530680),
        'crveth': (EthPool, ('0x8301AE4fc9c624d1D396cbDAa1ed877821D7C511', '0xEd4064f376cB8d68F770FB1Ff088a3d0F3FF5c4d'), 13676996),
        'cvxeth': (EthPool, ('0xB576491F1E6e5E62f1d8F26062Ee822B40B0E0d4', '0x3A283D9c08E8b55966afb64C515f5143cf907611'), 13783426),
        'xautusd': (ForexPool, ('0xAdCFcf9894335dC340f6Cd182aFA45999F45Fc44', '0x8484673cA7BfF40F82B041916881aeA15ee84834', '0xbEbc44782C7dB0a1A60Cb6fe97d0b483032FF1C7'), 13854277),
        'spelleth': (EthPool, ('0x98638FAcf9a3865cd033F36548713183f6996122', '0x8282BD15dcA2EA2bDf24163E8f2781B30C43A2ef'), 13931747),
        'teth': (EthPool, ('0x752eBeb79963cf0732E9c0fec72a49FD1DEfAEAC', '0xCb08717451aaE9EF950a2524E33B6DCaBA60147B'), 13931850),
}
start_blocks = {}

DB_NAME = 'crypto.lmdb'  # <- DB [block][pool#]{...}


def init_pools():
    for i, p in pools.items():
        if isinstance(p, tuple):
            pools[i] = p[0](*p[1])
            start_blocks[i] = p[2]


def fetch_stats(block, i='compound'):
    try:
        init_pools()
        return pools[i].fetch_stats(block)
    except ValueError as e:
        if 'missing trie node' in str(e):
            print('missing trie node for', block)
            return {}
        else:
            raise


def int2uid(value):
    return int.to_bytes(value, 4, 'big')


def pools_not_in_block(tx, b):
    # if b > 13943232 and b < 13953232:
    #     return list(pools)
    out = []
    block = tx.get(int2uid(b))
    if block:
        block = json.loads(block)
    if block:
        for k in pools:
            if k not in block:
                out.append(k)
    else:
        out = list(pools)
    return out


mpool = Pool(MPOOL_SIZE)
init_pools()


if __name__ == '__main__':
    from curvestats.w3 import w3 as our_w3
    w3 = our_w3()
    init_pools()

    db = lmdb.open(DB_NAME, map_size=(2 ** 35))

    start_block = 13943232
    print('Monitor started')

    # Initial data
    with db.begin(write=True) as tx:
        if pools_not_in_block(tx, 0):  # XXX
            tx.put(int2uid(0), json.dumps(
                        {k: {
                            'N': pool.N,
                            'decimals': pool.decimals,
                            'token': pool.token.address, 'pool': pool.pool.address,
                            'coins': [pool.coins[j].address for j in range(pool.N)]}
                         for k, pool in pools.items()}).encode())

    while True:
        while True:
            try:
                current_block = w3.eth.getBlock('latest')['number'] + 1
                break
            except Exception:
                time.sleep(10)

        if current_block - start_block > MPOOL_SIZE:
            blocks = range(start_block, start_block + MPOOL_SIZE)
            with db.begin(write=True) as tx:
                pools_to_fetch = pools_not_in_block(tx, blocks[-1])
                if pools_to_fetch:
                    stats = {}
                    for p in pools_to_fetch:
                        if blocks[0] >= start_blocks[p]:
                            newstats = mpool.map(partial(fetch_stats, i=p), blocks)
                            for b, s in zip(blocks, newstats):
                                if b not in stats:
                                    stats[b] = {}
                                stats[b][p] = s
                    for b, v in stats.items():
                        block = tx.get(int2uid(b))
                        if block:
                            block = json.loads(block)
                            v.update(block)
                        tx.put(int2uid(b), json.dumps(v).encode())
                    pools_fetched = [p for p in pools_to_fetch
                                     if blocks[-1] in stats and p in stats[blocks[-1]]]
                    print('...', start_block, pools_fetched)
                else:
                    print('... already in DB:', start_block)
            start_block += MPOOL_SIZE

        else:
            if current_block > start_block:
                for block in range(start_block, current_block):
                    with db.begin(write=True) as tx:
                        if pools_not_in_block(tx, block):
                            stats = {}
                            for p, pool in pools.items():
                                if block >= start_blocks[p]:
                                    stats[p] = pool.fetch_stats(block)
                            print(block, [len(s['trades']) for s in stats.values()])
                            tx.put(int2uid(block), json.dumps(stats).encode())
                start_block = current_block

            sleep(15)

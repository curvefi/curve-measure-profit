#!/usr/bin/env python3

import lmdb
import json
import time
import config_infura  # noqa
from time import sleep
from multiprocessing import Pool
from functools import partial

from curvestats.compound import CompoundPool
from curvestats.y import YPool
from curvestats.btc import BtcPool, NewBtcPool
from curvestats.newpool import NewPool
from curvestats.meta import MetaPool
from curvestats.metaf import MetaPoolU
from curvestats.idle import IDLEPool
from curvestats.ankr import ANKRPool
from curvestats.yv2 import YV2Pool
from curvestats.reth import RETHPool

MPOOL_SIZE = 20

pools = {
        'compound': (CompoundPool, ("0xA2B47E3D5c44877cca798226B7B8118F9BFb7A56", "0x845838DF265Dcd2c412A1Dc9e959c7d08537f8a2"), 9554041),
        'usdt': (CompoundPool, ("0x52EA46506B9CC5Ef470C5bf89f17Dc28bB35D85C", "0x9fC689CCaDa600B6DF723D9E47D84d76664a1F23"), 9456294),
        'y': (YPool, ("0x45F783CCE6B7FF23B2ab2D70e416cdb7D6055f51", "0xdF5e0e81Dff6FAF3A7e52BA697820c5e32D806A8"), 9476469),
        'busd': (YPool, ("0x79a8C46DeA5aDa233ABaFFD40F3A0A2B1e5A4F27", "0x3B3Ac5386837Dc563660FB6a0937DFAa5924333B"), 9567296),
        'susd': (CompoundPool, ('0xA5407eAE9Ba41422680e2e00537571bcC53efBfD', '0xC25a3A3b969415c80451098fa907EC722572917F'), 9906599),
        'pax': (YPool, ("0x06364f10B501e868329afBc005b3492902d6C763", "0xD905e2eaeBe188fc92179b6350807D8bd91Db0D8"), 10041041),
        'ren2': (BtcPool, ("0x93054188d876f558f4a66B2EF1d97d16eDf0895B", "0x49849C98ae39Fff122806C06791Fa73784FB3675"), 10151386),
        'rens': (BtcPool, ("0x7fC77b5c7614E1533320Ea6DDc2Eb61fa00A9714", "0x075b1bb99792c9E1041bA13afEf80C91a1e70fB3"), 10276945),
        'hbtc': (NewBtcPool, ("0x4CA9b3063Ec5866A4B82E437059D2C43d1be596F", "0xb19059ebb43466C323583928285a49f558E572Fd"), 10732330),
        '3pool': (NewPool, ("0xbEbc44782C7dB0a1A60Cb6fe97d0b483032FF1C7", "0x6c3F90f043a72FA612cbac8115EE7e52BDe6E490"), 10809482),
        'gusd': (MetaPool, ("0x4f062658EaAF2C1ccf8C8e36D6824CDf41167956", "0xD2967f45c4f384DEEa880F807Be904762a3DeA07"), 11005605),
        'husd': (MetaPool, ("0x3eF6A01A0f81D6046290f3e2A8c5b843e738E604", "0x5B5CFE992AdAC0C9D48E05854B2d91C73a003858"), 11010071),
        'usdn': (MetaPool, ("0x0f9cb53Ebe405d49A0bbdBD291A65Ff571bC83e1", "0x4f3E8F405CF5aFC05D68142F3783bDfE13811522"), 11010515),
        'usdk': (MetaPool, ("0x3E01dD8a5E1fb3481F0F589056b428Fc308AF0Fb", "0x97E2768e8E73511cA874545DC5Ff8067eB19B787"), 11010306),
        'linkusd': (MetaPool, ("0xE7a24EF0C5e95Ffb0f6684b813A78F2a3AD7D171", "0x6D65b498cb23deAba52db31c93Da9BFFb340FB8F"), 11011557),
        'musd': (MetaPool, ("0x8474DdbE98F5aA3179B3B3F5942D724aFcdec9f6", "0x1AEf73d49Dedc4b1778d0706583995958Dc862e6"), 11011941),
        'rsv': (MetaPool, ("0xC18cC39da8b11dA8c3541C598eE022258F9744da", "0xC2Ee6b0334C261ED60C72f6054450b61B8f18E35"), 11037532),
        'tbtc': (MetaPool, ("0xC25099792E9349C7DD09759744ea681C7de2cb66", "0x64eda51d3Ad40D56b9dFc5554E06F94e1Dd786Fd"), 11095929),
        'dusd': (MetaPool, ("0x8038C01A0390a8c547446a0b2c18fc9aEFEcc10c", "0x3a664Ab939FD8482048609f652f9a0B0677337B9"), 11187277),
        'pbtc': (MetaPool, ("0x7F55DDe206dbAD629C080068923b36fe9D6bDBeF", "0xDE5331AC4B3630f94853Ff322B66407e0D6331E8"), 11421596),
        'bbtc': (MetaPool, ("0x071c661B4DeefB59E2a3DdB20Db036821eeE8F4b", "0x410e3E86ef427e30B9235497143881f717d93c2A"), 11455023),
        'obtc': (MetaPool, ("0xd81dA8D904b52208541Bade1bD6595D8a251F8dd", "0x2fE94ea3d5d4a175184081439753DE15AeF9d614"), 11459239),
        'ust': (MetaPool, ("0x890f4e345B1dAED0367A877a1612f86A1f86985f", "0x94e131324b6054c0D789b190b2dAC504e4361b53"), 11466569),
        'eurs': (NewPool, ("0x0Ce6a5fF5217e38315f87032CF90686C96627CAA", "0x194eBd173F6cDacE046C53eACcE9B953F28411d1"), 11466872),
        'seth': (NewPool, ("0xc5424B857f758E906013F3555Dad202e4bdB4567", "0xA3D87FffcE63B53E0d54fAa1cc983B7eB0b74A9c"), 11491949),
        'aave': (NewPool, ("0xDeBF20617708857ebe4F679508E7b7863a8A8EeE", "0xFd2a8fA60Abd58Efe3EeE34dd494cD491dC14900"), 11497107),
        'idle': (IDLEPool, ("0x83f252f036761a1E3d10DACa8e16D7b21E3744D7", "0x09f4B84A87FC81FC84220fD7287b613B8A9D4c05"), 11503377),
        'steth': (NewPool, ("0xDC24316b9AE028F1497c275EB9192a3Ea0f67022", "0x06325440D014e39736583c165C2963BA99fAf14E"), 11592552),
        'saave': (NewPool, ("0xEB16Ae0052ed37f479f7fe63849198Df1765a733", "0x02d341CcB60fAaf662bC0554d13778015d1b285C"), 11772501),
        'ankreth': (ANKRPool, ("0xA96A65c051bF88B4095Ee1f2451C2A9d43F53Ae2", "0xaA17A236F2bAdc98DDc0Cf999AbB47D47Fc0A6Cf"), 11774140),
        'ib': (YV2Pool, ("0x2dded6Da1BF5DBdF597C45fcFaa3194e53EcfeAF", "0x5282a4eF67D9C33135340fB3289cc1711c13638C"), 11831120),
        'link': (NewPool, ("0xF178C0b5Bb7e7aBF4e12A4838C7b7c5bA2C623c0", "0xcee60cFa923170e4f8204AE08B4fA6A3F5656F3a"), 11875216),
        'usdp': (MetaPool, ("0x42d7025938bEc20B69cBae5A77421082407f053A", "0x7Eb40E450b9655f4B3cC4259BCC731c63ff55ae6"), 11922058),
        'tusd': (MetaPoolU, ("0xEcd5e75AFb02eFa118AF914515D6521aaBd189F1", "0xEcd5e75AFb02eFa118AF914515D6521aaBd189F1"), 12007000),
        'frax': (MetaPoolU, ("0xd632f22692FaC7611d2AA1C0D552930D43CAEd3B", "0xd632f22692FaC7611d2AA1C0D552930D43CAEd3B"), 11968731),
        'lusd': (MetaPoolU, ("0xEd279fDD11cA84bEef15AF5D39BB4d4bEE23F0cA", "0xEd279fDD11cA84bEef15AF5D39BB4d4bEE23F0cA"), 12184844),
        'busdv2': (MetaPoolU, ("0x4807862AA8b2bF68830e4C8dc86D0e9A998e085a", "0x4807862AA8b2bF68830e4C8dc86D0e9A998e085a"), 12237710),
        'alusd': (MetaPoolU, ("0x43b4FdFD4Ff969587185cDB6f0BD875c5Fc83f8c", "0x43b4FdFD4Ff969587185cDB6f0BD875c5Fc83f8c"), 11955334),
        'reth': (RETHPool, ("0xF9440930043eb3997fc70e1339dBb11F341de7A8", "0x53a901d48795C58f485cBB38df08FA96a24669D5"), 12463577),
        'mim': (MetaPoolU, ("0x5a6A4D54456819380173272A5E8E9B9904BdF41B", "0x5a6A4D54456819380173272A5E8E9B9904BdF41B"), 12557140),
        'eurt': (MetaPoolU, ("0xFD5dB7463a3aB53fD211b4af195c5BCCC1A03890", "0xFD5dB7463a3aB53fD211b4af195c5BCCC1A03890"), 12914705),
}
start_blocks = {}

DB_NAME = 'curvestats.lmdb'  # <- DB [block][pool#]{...}


def init_pools():
    for i, p in pools.items():
        if isinstance(p, tuple):
            pools[i] = p[0](*p[1])
            start_blocks[i] = p[2]


def fetch_stats(block, i='compound'):
    init_pools()
    return pools[i].fetch_stats(block)


def int2uid(value):
    return int.to_bytes(value, 4, 'big')


def pools_not_in_block(tx, b):
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
    from web3.auto.infura import w3
    init_pools()

    db = lmdb.open(DB_NAME, map_size=(2 ** 35))

    start_block = 12914705
    # start_block = w3.eth.getBlock('latest')['number'] - 1000
    print('Monitor started')

    # Initial data
    with db.begin(write=True) as tx:
        if pools_not_in_block(tx, 0) or True:  # XXX
            tx.put(int2uid(0), json.dumps(
                        {k: {
                            'N': pool.N,
                            'underlying_N': pool.underlying_N if hasattr(pool, 'underlying_N') else pool.N,
                            'decimals': pool.decimals,
                            'underlying_decimals': pool.underlying_decimals if hasattr(pool, 'underlying_decimals') else pool.decimals,
                            'token': pool.token.address, 'pool': pool.pool.address,
                            'coins': [pool.coins[j].address for j in range(pool.N)],
                            'underlying_coins': [pool.underlying_coins[j].address for j in range(getattr(pool, 'underlying_N', pool.N))]}
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

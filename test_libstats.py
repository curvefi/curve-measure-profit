import os
from pprint import pprint
from curvestats.compound import CompoundPool


os.environ['WEB3_INFURA_PROJECT_ID'] = 'efd35366fc0445f98df93cc418832774'


if __name__ == '__main__':
    pool = CompoundPool("0xA2B47E3D5c44877cca798226B7B8118F9BFb7A56", "0x845838DF265Dcd2c412A1Dc9e959c7d08537f8a2")
    pprint(pool.N)
    pprint(pool.decimals)
    stats = pool.fetch_stats()
    pprint(stats)
    pprint([stats['balances'][i] * stats['rates'][i] / 1e36 for i in range(pool.N)])

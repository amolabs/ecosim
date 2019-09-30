# vim: set sw=4 ts=4 expandtab :

from const import *

def users(state):
    chain = state['chain']
    market = state['market']
    # txs
    newtxs = int(param['txgenbase'] * market['liveness'] * config['stepblks'])
    # TODO: desires to sell or buy
    chain['txgen'] += newtxs
    chain['txpending'] += newtxs

def validators(state):
    chain = state['chain']
    # augment with tx fee
    upstake = int(chain['txpending'] * (chain['txfee'] + param['txreward']))
    upstake = min(upstake, chain['coins_active'])
    chain['stakes'] += upstake
    chain['coins_active'] -= upstake

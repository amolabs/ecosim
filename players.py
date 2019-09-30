# vim: set sw=4 ts=4 expandtab :

from const import *

def users(state):
    chain = state['chain']
    market = state['market']
    # txs
    newtxs = int(param['txgenbase'] * market['liveness'] * config['stepblks'])
    # TODO: desires to sell or buy
    chain['stat_txgen'] = newtxs
    chain['txpending'] += newtxs

def validators(state):
    chain = state['chain']
    market = state['market']

    global debug1, debug2

    #upstake = int((market['interest_chain'] - market['interest_world'])*oneamo)
    if market['interest_chain'] > market['interest_world']:
        upstake = int((chain['stakes'] + DELTA_MOTE) * 0.1) # 10% up
    elif market['interest_chain'] < market['interest_world']:
        upstake = -int(chain['stakes'] * 0.1) # 10% down
    else:
        upstake = 0

    upstake = min(upstake, chain['coins_active'])
    upstake = max(upstake, -chain['stakes'])
    debug1 = upstake
    chain['stakes'] += upstake
    chain['coins_active'] -= upstake

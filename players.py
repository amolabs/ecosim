# vim: set sw=4 ts=4 expandtab :

from const import *
from scipy import stats

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

    ic = market['interest_chain']
    iw = market['interest_world']
    sc = chain['stakes']
    upforce = (ic * (sc + DELTA_MOTE) / iw) - sc

    upforce = min(upforce, param['max_stakechange']*config['stepblks'])
    upforce = max(upforce, -param['max_stakechange']*config['stepblks'])

    # mimic human unpredictability using random variable
    rv = stats.norm()
    upstake = upforce / 2 * rv.rvs() + upforce

    upstake = min(upstake, chain['coins_active'])
    upstake = max(upstake, -chain['stakes'])
    debug1 = upstake
    chain['stakes'] += upstake
    chain['coins_active'] -= upstake

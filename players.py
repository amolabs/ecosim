# vim: set sw=4 ts=4 expandtab :

from const import *
import math
from scipy import stats
#import numpy as np
#import matplotlib as mpl

import nplayers

def users(state):
    chain = state['chain']
    market = state['market']
    hist = nplayers.hist

    avg_txfee = sum(hist['txfee']) / len(hist['txfee'])

    # update liveness
    tmp = market['liveness']
    # increase by growth factor
    f = param['growth_factor']
    ## suppress by tx fee
    fee_usd = avg_txfee / oneamo * market['exchange_rate']
    f *= param['feescale'] / (fee_usd + param['feescale'])
    #fee_factor = math.log10(fee_factor) + 1
    tmp *= f
    # range check
    tmp = min(tmp, 1.)
    tmp = max(tmp, 0.00001)
    # update
    market['liveness'] = tmp
    # smoothing
    #smooth = config['smooth'] / config['stepblks']
    #market['liveness'] = (tmp + (smooth-1)*market['liveness']) / smooth

    # generate txs depending on market value
    txforce = param['txpervalue'] * market['value'] * config['stepblks']
    # adjust by tx fee
    fee_usd = avg_txfee / oneamo * market['exchange_rate']
    txforce *= param['feescale'] / (fee_usd**2 + param['feescale'])
    #txforce /= math.pow(1.1, fee_usd / param['feescale'])
    # mimic human unpredictability using random variable
    rv = stats.norm()
    newtxs = txforce / 2 * rv.rvs() + txforce
    # range check
    newtxs = max(newtxs, param['txgenbase'] * config['stepblks'])
    newtxs = int(newtxs)

    chain['stat_txgen'] = newtxs
    chain['txpending'] += newtxs

    # TODO: desires to sell or buy

def validators(state):
    chain = state['chain']
    market = state['market']
    hist = nplayers.hist

    avg_txfee = sum(hist['txfee']) / len(hist['txfee'])

    # projected yearly interest of the chain
    # (augment with very small bias to chain)
    # yearly coin gain for validator nodes
    gain_usd_year = chain['stat_txproc'] \
            * (avg_txfee + param['txreward']) \
            * BLKSYEAR / config['stepblks']
    # yearly running cost for validator nodes
    cost_usd_year = 1000 * chain['stakes'] / 10000
    interest = (gain_usd_year - cost_usd_year) \
            / (chain['stakes'] + DELTA_MOTE)
    interest = max(interest, 0)
    #market['interest_stake'] = min(interest, 100)
    market['interest_stake'] = interest

    ic = market['interest_stake']
    iw = market['interest_world']
    sc = chain['stakes']
    upforce = (ic * (sc + DELTA_MOTE) / iw) - sc

    # limit by max stake change
    upforce = min(upforce, param['max_stakechange']*config['stepblks'])
    upforce = max(upforce, -param['max_stakechange']*config['stepblks'])

    # mimic human unpredictability using random variable
    rv = stats.norm()
    upstake = upforce / 2 * rv.rvs() + upforce
    upstake = int(upstake)

    # limit by asset status
    upstake = min(upstake, chain['coins_active'])
    upstake = max(upstake, -chain['stakes'])
    chain['stakes'] += upstake
    chain['coins_active'] -= upstake

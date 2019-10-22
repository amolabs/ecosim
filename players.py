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
    txforce = param['txpervalue'] * market['value'] \
            * config['stepblks'] / BLKSMONTH
    # adjust by tx fee
    fee_usd = avg_txfee / oneamo * market['exchange_rate']
    txforce *= param['feescale'] / (fee_usd**2 + param['feescale'])

    # mimic human unpredictability using random variable
    df = 32
    rv = stats.chi2(df)
    newtxs = txforce / df * rv.rvs()
    newtxs = int(newtxs)

    chain['stat_txgen'] = newtxs
    chain['txpending'] += newtxs

    # TODO: desires to sell or buy

def validators(state):
    chain = state['chain']
    market = state['market']
    hist = nplayers.hist

    avg_txproc = sum(hist['txproc']) / len(hist['txproc'])
    avg_txfee = sum(hist['txfee']) / len(hist['txfee'])

    # projected yearly interest of the chain
    # (augment with very small bias to chain)
    # yearly coin gain for validator nodes
    gain_year = avg_txproc * (avg_txfee + param['txreward']) \
            * BLKSYEAR / config['stepblks']
    # yearly running cost for validator nodes
    cost_year = 1000 * math.log10(chain['stakes'] / 10000 + 1)
    net_gain_year = gain_year - cost_year

    #ic = market['interest_stake']
    #ic = avg_interest
    iw = market['interest_world']
    sc = chain['stakes']
    upforce = net_gain_year / iw - sc

    # opportunity cost by keeping stakes
    oppcost = chain['stakes'] / 2
    downforce = oppcost

    # mimic human unpredictability using random variable
    df = 32
    rv = stats.chi2(df)
    upstake = (upforce - downforce) / df * rv.rvs()
    upstake = int(upstake)

    # update interest rate
    interest = net_gain_year / (chain['stakes'] + DELTA_MOTE)
    interest = max(interest, 0)
    market['interest_stake'] = interest

    # limit by asset status
    upstake = min(upstake, chain['coins_active'])
    upstake = max(upstake, -(chain['stakes'] - param['fixed_stakes']))
    chain['stakes'] += upstake
    chain['coins_active'] -= upstake

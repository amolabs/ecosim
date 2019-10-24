# vim: set sw=4 ts=4 expandtab :

from const import *
import math
from scipy import stats

import nplayers

def users(state, nstate):
    chain = state['chain']
    market = state['market']
    hist = nplayers.hist

    avg_txfee = sum(hist['txfee']) / len(hist['txfee'])

    # generate txs depending on market value
    txforce = param['txpervalue'] * market['value'] \
            * config['stepblks'] / BLKSMONTH
    # adjust by tx fee
    fee_usd = avg_txfee / oneamo * market['exchange_rate']
    txforce *= param['feecap'] / (fee_usd + param['feecap'])

    # mimic human unpredictability using random variable
    df = 32
    rv = stats.chi2(df)
    newtxs = txforce / df * rv.rvs()
    newtxs = int(newtxs)

    nstate['chain']['stat_txgen'] = newtxs
    nstate['chain']['txpending'] += newtxs

    # TODO: desires to sell or buy

def validators(state, nstate):
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
    upstake = (upforce - downforce) / 10 * rv.rvs() / df
    if upstake < 0:
        upstake /= 10
    upstake = int(upstake)

    # limit by asset status
    upstake = min(upstake, chain['coins_active'])
    upstake = max(upstake, -(chain['stakes'] - param['fixed_stakes']))
    nstate['chain']['stakes'] += upstake
    nstate['chain']['coins_active'] -= upstake

    # update interest rate
    interest = net_gain_year / (chain['stakes'] + DELTA_MOTE)
    interest = max(interest, 0)
    nstate['market']['interest_stake'] = interest

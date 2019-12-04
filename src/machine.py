# -*- coding: utf-8 -*-
# vim: set sw=4 ts=4 expandtab :

import math
import numpy as np
from scipy import stats

from const import *

tau_short  = BLKSDAY
tau_medium = BLKSMONTH
tau_long   = BLKSYEAR

def delta_unit(t):
    return math.pow(100, -t)

def run_delta(target, tau):
    delta = target * (1 - delta_unit(config['stepblks']/tau))
    return delta

def run_approach(target, history, trend):
    if trend == 'short':
        tau = tau_short
        att_factor = 1
    elif trend == 'medium':
        tau = tau_medium
        att_factor = 2
    elif trend == 'long':
        tau = tau_long
        att_factor = 3
    else:
        return

    delta = run_delta(target, tau)
    l = len(history)
    if l < 2:
        momentum = 0
    else:
        momentum = history[l-1] - history[l-2]
    if momentum == 0:
        momentum = SMALL
    ratio = np.abs(delta) / np.abs(momentum)
    ratio = max(1, ratio)
    att = np.log10(ratio) / 2
    delta_att = delta / math.pow(10, att)
    if delta > 0:
        momentum = min(momentum + delta_att, delta)
    else:
        momentum = max(momentum + delta_att, delta)
    return momentum

def update_output(state, output, history):
    excess = output - state.output
    excess = max(-state.output, excess)
    delta = run_approach(excess, history, 'long')
    state.output += delta

def update_stakes(state, money_demand, history):
    excess = state.coins_active - money_demand
    delta = run_approach(excess, history, 'medium')
    # limit check
    if delta >= 0:
        delta = min(delta, state.coins_active)
    else:
        delta = -min(state.stakes, -delta)
    #if state.steps > 24*900:
    #    print(f'stake excess:{excess:.3e}, delta:{delta:.3e}')
    state.stakes += delta
    state.coins_active -= delta # compenstate

def update_dormant(state, money_demand, history):
    excess = state.coins_active - money_demand
    delta = run_approach(excess, history, 'short')
    # limit check
    if delta >= 0:
        #delta = min(delta, state.coins_active)
        return
    else:
        delta = -min(state.coins_dormant, -delta)
    state.coins_dormant += delta
    state.coins_active -= delta # compenstate

def update_price(state, price_level, history):
    excess = price_level - state.price_level
    excess = max(-state.price_level, excess)
    delta = run_approach(excess, history, 'long')
    #print(f'price {state.price_level:.3e}, {price_level:.3e}, {excess:.3e}, {delta:.3e}')
    state.price_level += delta

def update_txs(state):
    # dep:
    # state.output
    # state.txfee
    # state.usdperamo
    # update:
    # state.txpending

    tx_wanted = param['txpervalue'] * state.output \
            * config['stepblks'] / BLKSYEAR # scale by step size
    fee_real = state.txfee / state.price_level
    txs = int(tx_wanted * param['feecap'] / (fee_real + param['feecap']))
    #txs = int(tx_wanted)
    state.step_txgen = txs
    state.txpending += txs
    lazy_txs = int(0.1 * txs)
    state.step_txproc = min(state.txpending - lazy_txs,
            param['blktxsize']*config['stepblks'])
    state.txpending -= state.step_txproc

def update_txfee(state, history):
    # dep:
    # state.txpending
    # state.price_level
    # update:
    # state.txfee

    waiting_blks = state.txpending / param['blktxsize'] # in real money
    wanted_fee = param['feescale'] * state.price_level * waiting_blks
    excess = wanted_fee - state.txfee
    delta = run_approach(excess, history, 'short')
    state.txfee += delta

def update_incentive(state):
    reward = state.step_txproc * param['txreward']
    if config['dormant']:
        state.coins_dormant += reward
    else:
        state.coins_active += reward
    state.coins += reward
    if config['dormant']:
        fees = state.step_txproc * state.txfee
        fees = min(fees, state.coins_active)
        state.coins_dormant += fees
        state.coins_active -= fees

def deplete(state):
    depletion = state.coins_active * param['deplete_coin'] \
            * config['stepblks'] / BLKSMONTH
    depletion = min(depletion, state.coins_active)
    state.coins_active -= depletion
    state.coins_lost += depletion

def update_interest_amo(state):
    # dep:
    # state.step_txproc
    # state.stakes
    # update:
    # state.interest_amo
    return_amo = state.step_txproc * (param['txreward'] + state.txfee) \
            * BLKSYEAR / config['stepblks'] # projected yearly income
    invest_amo = state.stakes
    invest_amo = max(invest_amo, TINY)
    state.interest_amo = return_amo/invest_amo
    #print(state.interest_amo, return_amo, invest_amo)

def update_exrate(state, exrate, history):
    excess = exrate - state.usdperamo
    delta = run_approach(excess, history, 'short')
    state.usdperamo += delta

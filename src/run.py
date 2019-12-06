#!/usr/bin/env python3
# -*- coding: utf-8 -*-
# vim: set sw=4 ts=4 expandtab :

import copy
import numpy as np
import matplotlib.pyplot as plt

from const import *
import economy
import machine

config = {
        'stepblks': 60*60*24, # in blocks
        'steps': 5000,
        #'steps': 24*200,
        #'steps': 10,
        'dormant': False,
        }
param = {
        # chain parameters
        'txreward': 0.1,
        'blktxsize': 500,
        'feescale': 0.00001,
        'feecap': 0.1,
        # market parameters
        #'f_gdp_month': [1000.], # higher order first
        #'f_gdp_month': [10000000.], # higher order first
        'f_gdp_month': [10000, 10000, 1000.], # higher order first
        'velocity': 1,
        'transfer_cost_factor': 1,
        'txpervalue': 100., # one tx per one USD
        # depeletion rates
        'deplete_coin': 0.01,
        'deplete_tx': 0.001,
        }

state_dtype = [
        # simulation
        ('steps', 'i4'),
        # tx dynamics
        ('step_txgen', 'i8'),
        ('step_txproc', 'i8'),
        ('txlost', 'i8'),
        ('txpending', 'i8'),
        # assets
        ('txfee', 'f8'),
        ('coins', 'f8'),
        ('coins_active', 'f8'),
        ('coins_dormant', 'f8'),
        ('coins_lost', 'f8'),
        ('stakes', 'f8'),
        # pseudo-assets
        ('output', 'f8'),
        # metrics
        ('money_demand', 'f8'),
        ('real_money_demand', 'f8'),
        ('interest_amo', 'f8'),
        ('interest_usd', 'f8'),
        ('price_level', 'f8'),
        ('price_usd', 'f8'),
        ('usdperamo', 'f8'),
        ('ex_long', 'f8'),
        ]

if config['dormant']:
    coins_active = 0
    coins_dormant = 20000000000 - 100000000
else:
    coins_active = 20000000000 - 100000000
    coins_dormant = 0

history = np.array([(
    0,               # steps #
    0,               # step_txgen #
    0,               # step_txproc #
    0,               # txlost
    0,               # txpending #
    0,               # txfee #
    20000000000,     # coins
    coins_active,    # coins_active
    coins_dormant,   # coins_dormant
    0,               # coins_lost
    100000000,       # stakes #
    0,               # output #
    1000,            # money_demand #
    1000,            # real_money_demand #
    0.1,             # interest_amo #
    0.02,            # interest_usd # constant
    1,               # price_level #
    1,               # price_usd # constant
    0.0005,          # usdperamo #
    0.0005,          # ex_long #
    )],
    dtype = state_dtype
    )

def display_state(state):
    n = state.steps
    days = n*config['stepblks']/60/60/24
    print(f'run steps: {n}, {n*config["stepblks"]} blocks = {days:.2f} days')
    print(f'tx: {state.step_txgen:-12,d}(+) {state.step_txproc:-12,d}(-)  {state.txlost:-7,d} lost  {state.txpending:-6,d} pending')
    # chain stat
    amo = state.txfee
    print(f'  tx fee:               {amo:-20,.3e} AMO / tx')
    usd = amo * state.usdperamo
    print(f'                        {usd:-20,.3e} USD / tx')
    # assets
    amo = state.coins
    print(f'  coins:  total         {amo:-20,.3f} AMO')
    amo = state.coins_active
    ratio = state.coins_active / state.coins * 100
    print(f'          active        {amo:-20,.3f} AMO ({ratio:.3f}%)')
    amo = state.coins_dormant
    ratio = state.coins_dormant / state.coins * 100
    print(f'          dormant       {amo:-20,.3f} AMO ({ratio:.3f}%)')
    amo = state.coins_lost
    ratio = state.coins_lost / state.coins * 100
    print(f'          lost          {amo:-20,.3f} AMO ({ratio:.3f}%)')
    amo = state.stakes
    ratio = state.stakes / state.coins * 100
    print(f'          stakes        {amo:-20,.3f} AMO ({ratio:.3f}%)')
    # market
    print(f'  market: output        {state.output:-20,.3f} goods / year')
    print(f'          price level   {state.price_level:-20,.3f} AMO / good')
    print(f'          exchange      {state.usdperamo:-20,.3e} USD/AMO')
    print(f'          interest      {state.interest_amo:-21,.4f}')

def step(history):
    recarr = np.rec.array(history)
    state = recarr[len(history)-1]
    nstate = copy.deepcopy(state)
    ################
    nstate.steps += 1
    output = economy.get_output(nstate)
    machine.update_output(nstate, output, recarr.output)
    (money_demand, real_demand) = economy.get_money_demand(state)
    nstate.money_demand = money_demand
    nstate.real_money_demand = real_demand
    #print(money_demand)
    machine.update_stakes(nstate, money_demand, recarr.stakes)
    if config['dormant']:
        machine.update_dormant(nstate, money_demand, recarr.coins_dormant)
    price_level = economy.get_price_amo(state)
    #print(price_level)
    machine.update_price(nstate, price_level, recarr.price_level)
    machine.update_txs(nstate)
    machine.update_txfee(nstate, recarr.txfee)
    machine.update_incentive(nstate)
    machine.deplete(nstate)
    machine.update_interest_amo(nstate)
    exrate_long = economy.get_exrate_long(state)
    nstate.ex_long = exrate_long
    exrate_short = economy.get_exrate_short(state, exrate_long)
    machine.update_exrate(nstate, exrate_short, recarr.usdperamo)
    ################
    return nstate

def run(history):
    economy.init_gdp(param['f_gdp_month'])
    history[0]['output'] = economy.gdp_func(0)
    machine.config = config
    machine.param = param
    economy.config = config
    economy.param = param
    for i in range(config['steps']):
        nstate = step(history)
        history = np.append(history, nstate)
    display_state(np.rec.array(history)[len(history)-1])
    return history

print('simulation start')
history = run(history)

# plot
recarr = np.rec.array(history[1:])
#print(recarr.price_level)
xarr = recarr.steps * config['stepblks'] / BLKSDAY

fig, axs = plt.subplots(2, 1, figsize=[7,9.5], sharex=True, tight_layout=True)
ass = axs[0]
eco = axs[1]
ass.set_yscale('log')
eco.set_yscale('log')

ass.plot(xarr, recarr.coins_active, label='active coins (AMO)',
        color='red', linestyle='solid')
ass.plot(xarr, recarr.coins_dormant, #label='dormant coins (AMO)',
        color='grey', linestyle='solid')
ass.plot(xarr, recarr.stakes, label='stakes (AMO)',
        color='blue', linestyle='solid')
ass.plot(xarr, recarr.money_demand, label='money demand (AMO)',
        color='red', linestyle='solid', linewidth=6, alpha=0.3)
ass.plot(xarr, recarr.real_money_demand, #label='real money demand (REAL)',
        color='yellow', linestyle='solid', linewidth=6, alpha=0.3)
ass.plot(xarr, recarr.output, label='economy output (REAL)',
        color='black', linestyle='solid')

eco.plot(xarr, recarr.price_level, label='price level (AMO / unit)',
        color='cyan', linestyle='solid')
eco.plot(xarr, recarr.txfee, label='tx fee (AMO / tx)',
        color='red', linestyle='dashed')
eco.plot(xarr, recarr.interest_amo, label='interest rate',
        color='blue', linestyle='dashed')
eco.plot(xarr, recarr.ex_long, label='long-run exchange rate (USD / AMO)',
        color='green', linestyle='solid', linewidth=6, alpha=0.3)
eco.plot(xarr, recarr.usdperamo, label='current exchange rate (USD / AMO)',
        color='green', linestyle='solid')
eco.plot(xarr, recarr.step_txgen, #label='new txs',
        color='black', linestyle='solid', linewidth=6, alpha=0.3)
eco.plot(xarr, recarr.step_txproc, #label='processed txs',
        color='black', linestyle='dashed')
eco.plot(xarr, recarr.txpending, #label='pending txs',
        color='darkgray', linestyle='dashed')

ass.legend(loc='best')
eco.legend(loc='lower right')

plt.show()

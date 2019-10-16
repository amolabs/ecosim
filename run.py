#!/usr/bin/env python3
# -*- coding: utf-8 -*-
# vim: set sw=4 ts=4 expandtab :

from const import *
import players
import nplayers
import matplotlib.pyplot as plt

config = {
        'stepblks': 60*60*24, # in blocks
        #'steps': 24*365,
        #'steps': 24*150,
        'steps': 2000,
        'smooth': 50000,
        }
param = {
        # chain parameters
        'initial_coins': 20000000000*oneamo,
        'initial_stakes': 1000000*oneamo,
        'txreward': 0.1*oneamo,
        'blktxsize': 1000,
        'feescale': 0.1,
        'max_stakechange': 10000*oneamo,
        # market parameters
        'initial_liveness': 0,
        'f_gdp_month': [10000., 500, 5000, 10],
        'initial_exchrate': 0.0005, # USD for one AMO
        'initial_interest_world': 0.02,
        'txpervalue': 0.1, # one tx per one USD
        'txgenbase': 0.1, # one tx per block
        'growth_factor': 1.01,
        # depeletion rates
        'deplete_coin': 0.0001,
        'deplete_tx': 0.001,
        }
state = {
        'steps': 0,
        'chain': {
            # tx statistics
            'stat_txgen': 0,
            'stat_txproc': 0,
            'stat_txlost': 0,
            # tx dynamics
            'blks': 0,
            'txpending': 0,
            'txfee': 0,
            # assets
            'coins': param['initial_coins'],
            'coins_active': param['initial_coins'] - param['initial_stakes'],
            'coins_lost': 0,
            'stakes': param['initial_stakes'],
            },
        'market': {
            'liveness': param['initial_liveness'],
            'value': param['f_gdp_month'][0],
            'exchange_rate': param['initial_exchrate'], # in AMO, not mote
            'interest_stake': 0,
            'interest_world': param['initial_interest_world'],
            }
        }

def display_state(state):
    chain = state['chain']
    market = state['market']
    days = chain['blks']/60/60/24
    print(f'run steps: {state["steps"]}, {chain["blks"]} blocks = {days:.2f} days')
    # chain stat
    print(f'tx: {chain["stat_txgen"]:-12,d}(+) {chain["stat_txproc"]:-12,d}(-)  {chain["stat_txlost"]:-7,d} lost  {chain["txpending"]:-6,d} pending')
    coinsamo = chain['txfee']/oneamo
    print(f'  tx fee:               {coinsamo:-20,.3f} AMO / tx')
    usd = coinsamo * market['exchange_rate']
    print(f'                        {usd:-20,.3f} USD / tx')
    # assets
    coinsamo = chain['coins']/oneamo
    print(f'  coins:  total         {coinsamo:-20,.3f} AMO')
    coinsamo = chain['coins_active']/oneamo
    ratio = chain['coins_active'] / chain['coins'] * 100
    print(f'          active        {coinsamo:-20,.3f} AMO ({ratio:.3f}%)')
    coinsamo = chain['coins_lost']/oneamo
    ratio = chain['coins_lost'] / chain['coins'] * 100
    print(f'          lost          {coinsamo:-20,.3f} AMO ({ratio:.3f}%)')
    coinsamo = chain['stakes']/oneamo
    ratio = chain['stakes'] / chain['coins'] * 100
    print(f'          stakes        {coinsamo:-20,.3f} AMO ({ratio:.3f}%)')
    #print(f'          stakes(mote)  {chain["stakes"]:-20,} mote')
    # market
    print(f'  market: value         {market["value"]:-20,.3f} USD')
    print(f'          exchange      {market["exchange_rate"]:-21,.4f} USD/AMO')
    print(f'          liveness      {market["liveness"]:-21,.4f}')
    print(f'          interest      {market["interest_stake"]:-21,.4f}')
    #print(f'  debug1 = {players.debug1:,}')
    #print(f'  debug1 = {nplayers.debug1:,}')

def step(state):
    state['steps'] += 1
    state['chain']['blks'] += config['stepblks']
    players.users(state)
    players.validators(state)
    nplayers.teller(state['chain'])
    nplayers.depleter(state['chain'])
    nplayers.invisible(state)
    nplayers.historian(state)

def run(state):
    steps = []
    y_txgen = []
    y_txpen = []
    y_coins = []
    y_txfee_usd = []
    y_interest = []
    y_liveness = []
    y_exchange = []
    y_value = []
    y_active = []
    y_stakes = []
    for i in range(config['steps']):
        step(state)
        steps.append(state['steps'])
        y_txgen.append(state['chain']['stat_txgen'])
        y_txpen.append(state['chain']['txpending'])
        y_coins.append(state['chain']['coins']/oneamo)
        y_txfee_usd.append(state['chain']['txfee']/oneamo \
                * state['market']['exchange_rate'])
        y_interest.append(state['market']['interest_stake'])
        y_liveness.append(state['market']['liveness'])
        y_exchange.append(state['market']['exchange_rate'])
        y_value.append(state['market']['value'])
        y_active.append(state['chain']['coins_active']/oneamo)
        y_stakes.append(state['chain']['stakes']/oneamo)
    display_state(state)
    plt.plot(steps, y_txgen, '--k')
    plt.plot(steps, y_txpen, '--g')
    #plt.plot(steps, y_coins)
    plt.plot(steps, y_txfee_usd, '--r')
    plt.plot(steps, y_interest, '-y', 'interest')
    plt.plot(steps, y_liveness, '-m')
    plt.plot(steps, y_exchange, '-g')
    plt.plot(steps, y_value, '-k')
    plt.plot(steps, y_active, '-r')
    plt.plot(steps, y_stakes, '-b')
    print()

coinsamo = param['initial_coins']/oneamo
print(f'init coins:    {coinsamo:-20,.3f} AMO')
coinsamo = param['txreward']/oneamo
print(f'tx reward:     {coinsamo:-20,.3f} AMO / tx')
print(f'blks in step:  {config["stepblks"]:-20,d} blks / step')

players.config = config
nplayers.config = config
players.param = param
nplayers.param = param
nplayers.hist_size = int(BLKSMONTH / config['stepblks'])

print( '==================================================================')
#for i in range(5):
run(state)

plt.xlabel('steps')
#plt.ylabel('ylabel')
plt.yscale('log')
plt.show()

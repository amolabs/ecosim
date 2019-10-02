#!/usr/bin/env python3
# -*- coding: utf-8 -*-
# vim: set sw=4 ts=4 expandtab :

from const import *
import players
import nplayers
import matplotlib.pyplot as plt

config = {
        'stepblks': 60*60, # in blocks
        #'steps': 24*365,
        'steps': 24*50,
        }
param = {
        # chain parameters
        'initial_coins': 20000000000*oneamo,
        'initial_stakes': 10000000*oneamo,
        'txreward': 0.1*oneamo,
        'blktxsize': 100,
        'feescale': 1.0,
        'max_stakechange': 10000*oneamo,
        # market parameters
        'initial_liveness': 0,
        'initial_value': 0, # TODO
        'initial_exchrate': 0.0005, # USD for one AMO
        'txgenbase': 1, # per block
        'growth_factor': 1.1,
        'initial_interest_world': 0.02,
        # depeletion rates
        'deplete_coin': 0.000001,
        'deplete_tx': 0.000001,
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
            'value': param['initial_exchrate'] * param['initial_coins'] / oneamo,
            'exchange_rate': param['initial_exchrate'], # in AMO, not mote
            'interest_chain': 0,
            'interest_world': param['initial_interest_world'],
            }
        }

def display_state(state):
    chain = state['chain']
    days = chain['blks']/60/60/24
    print(f'run steps: {state["steps"]}, {chain["blks"]} blocks = {days:.2f} days')
    # chain stat
    print(f'tx: {chain["stat_txgen"]:-12,d}(+) {chain["stat_txproc"]:-12,d}(-)  {chain["stat_txlost"]:-7,d} lost  {chain["txpending"]:-6,d} pending')
    coinsamo = chain['txfee']/oneamo
    print(f'  tx fee:               {coinsamo:-20,.3f} AMO / tx')
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
    market = state['market']
    print(f'  market: value         {market["value"]:-20,.3f} USD')
    print(f'          exchange      {market["exchange_rate"]:-21,.4f} USD/AMO')
    print(f'          liveness      {market["liveness"]:-21,.4f}')
    print(f'          interest      {market["interest_chain"]:-21,.4f}')
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

def run(state):
    steps = []
    y_txgen = []
    y_coins = []
    y_txfee = []
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
        y_coins.append(state['chain']['coins']/oneamo)
        y_txfee.append(state['chain']['txfee']/oneamo)
        y_interest.append(state['market']['interest_chain'])
        y_liveness.append(state['market']['liveness'])
        y_exchange.append(state['market']['exchange_rate'])
        y_value.append(state['market']['value'])
        y_active.append(state['chain']['coins_active']/oneamo)
        y_stakes.append(state['chain']['stakes']/oneamo)
    display_state(state)
    #plt.plot(steps, y_txgen)
    #plt.plot(steps, y_coins)
    #plt.plot(steps, y_txfee, '.-r')
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

print( '==================================================================')
#for i in range(5):
run(state)

plt.xlabel('steps')
#plt.ylabel('ylabel')
plt.yscale('log')
plt.show()

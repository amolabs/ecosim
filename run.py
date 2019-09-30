#!/usr/bin/env python3
# -*- coding: utf-8 -*-
# vim: set sw=4 ts=4 expandtab :

from const import *
import players
import nplayers

config = {
        'stepblks': 60*60, # in blocks
        'steps': 24*365,
        }
param = {
        # chain parameters
        'initial_coins': 20000000000*oneamo,
        'txreward': 0.1*oneamo,
        'blktxsize': 100,
        'feecap': 10000*oneamo,
        # market parameters
        'initial_liveness': 0,
        'initial_value': 0,
        'initial_exchrate': 0, # USD for one AMO
        'txgenbase': 1, # per block
        'growth_factor': 1.1,
        }
state = {
        'steps': 0,
        'chain': {
            # tx statistics
            'txgen': 0,
            'txproc': 0,
            'txlost': 0,
            # tx dynamics
            'blks': 0,
            'txpending': 0,
            'txfee': 0,
            # assets
            'coins': param['initial_coins'],
            'coins_active': param['initial_coins'],
            'coins_lost': 0,
            'stakes': 0,
            },
        'market': {
            'liveness': param['initial_liveness'],
            'value': param['initial_value'],
            'exchange_rate': param['initial_exchrate'], # in AMO, not mote
            }
        }

def display_state(state):
    chain = state['chain']
    days = chain['blks']/60/60/24
    print(f'run steps: {state["steps"]}, {chain["blks"]} blocks = {days} days')
    # chain stat
    print(f'tx: {chain["txgen"]:-12,d}(+) {chain["txproc"]:-12,d}(-)  {chain["txlost"]:-7,d} lost  {chain["txpending"]:-6,d} pending')
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
    # market
    market = state['market']
    print(f'  market: value         {market["value"]:-20,.3f} USD')
    print(f'          exchange      {market["exchange_rate"]:-21,.4f} USD/AMO')
    print(f'          liveness      {market["liveness"]:-21,.4f}')

def step(state):
    state['steps'] += 1
    state['chain']['blks'] += config['stepblks']
    players.users(state)
    players.validators(state)
    nplayers.teller(state['chain'])
    nplayers.depleter(state['chain'])
    nplayers.invisible(state)

def run(state, param):
    for i in range(config['steps']):
        step(state)
    display_state(state)
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
for i in range(5):
    run(state, {})

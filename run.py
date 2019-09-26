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
        'initialcoins': 20000000000*oneamo,
        'txreward': 0.1*oneamo,
        'blktxsize': 100,
        # market parameters
        'txgenbase': 1, # per block
        'growth_factor': 1.1,
        'initialliveness': 0.1,
        }
state = {
        'steps': 0,
        'chain': {
            'blks': 0,
            # tx dynamics
            'txgen': 0,
            'txproc': 0,
            'txlost': 0,
            'txpending': 0,
            'txfee': 0,
            # assets
            'coins': param['initialcoins'],
            'activecoins': param['initialcoins'],
            'lostcoins': 0,
            'stakes': 0,
            },
        'market': {
            'liveness': param['initialliveness'],
            'value': 0,
            }
        }

def display_state(state):
    chain = state['chain']
    days = chain['blks']/60/60/24
    print(f'run steps: {state["steps"]}, {chain["blks"]} blocks = {days} days')
    # chain stat
    print(f'tx: {chain["txgen"]:-12,d}(+) {chain["txproc"]:-12,d}(-)  {chain["txlost"]:-7,d} lost  {chain["txpending"]:-6,d} pending')
    coinsamo = chain['txfee']/oneamo
    print(f'  tx fee:            {coinsamo:-20,.3f} AMO / tx')
    # assets
    coinsamo = chain['coins']/oneamo
    print(f'  coins:  total      {coinsamo:-20,.3f} AMO')
    coinsamo = chain['activecoins']/oneamo
    ratio = chain['activecoins'] / chain['coins'] * 100
    print(f'          active     {coinsamo:-20,.3f} AMO ({ratio:.3f}%)')
    coinsamo = chain['lostcoins']/oneamo
    ratio = chain['lostcoins'] / chain['coins'] * 100
    print(f'          lost       {coinsamo:-20,.3f} AMO ({ratio:.3f}%)')
    coinsamo = chain['stakes']/oneamo
    ratio = chain['stakes'] / chain['coins'] * 100
    print(f'          stakes     {coinsamo:-20,.3f} AMO ({ratio:.3f}%)')
    # market
    market = state['market']
    print(f'  market: value      {market["value"]:-20,.3f} USD')
    print(f'          liveness   {market["liveness"]:-21,.4f}')

def step(state):
    state['steps'] += 1
    state['chain']['blks'] += config['stepblks']
    players.users(state)
    players.validators(state)
    nplayers.invisible(state)
    nplayers.teller(state['chain'])
    nplayers.depleter(state['chain'])

def run(state, steps, param):
    for i in range(steps):
        step(state)
    display_state(state)
    print()

coinsamo = param['initialcoins']/oneamo
print(f'init coins:    {coinsamo:-20,.3f} AMO')
coinsamo = param['txreward']/oneamo
print(f'tx reward:     {coinsamo:-20,.3f} AMO / tx')
print(f'blks in step:  {config["stepblks"]:-20,d} blks / step')

players.config = config
nplayers.config = config
players.param = param
nplayers.param = param

print()
for i in range(5):
    run(state, config['steps'], {})

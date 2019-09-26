#!/usr/bin/env python3
# -*- coding: utf-8 -*-
# vim: set sw=4 ts=4 expandtab :

import nplayers

# const
oneamo = 1000000000000000000

config = {
        'stepblks': 60*60*24, # in blocks
        'steps': 100,
        }
param = {
        'initialcoins': 20000000000*oneamo,
        'txreward': 0.1*oneamo,
        'blktxsize': 1000,
        }
state = {
        'steps': 0,
        'chain': {
            'blks': 0,
            # assets
            'coins': 0,
            'activecoins': 0,
            'lostcoins': 0,
            'stakes': 0,
            'delstakes': 0,
            # tx dynamics
            'txgen': 0,
            'txpending': 0,
            'txfee': 0,
            },
        }

def display_state(state):
    chain = state['chain']
    days = chain['blks']/60/60/24
    print(f'run steps: {state["steps"]}, {chain["blks"]} blocks = {days} days')

    coinsamo = chain['coins']/oneamo
    print(f'  coins: total  {coinsamo:-20.3f} AMO')
    coinsamo = chain['activecoins']/oneamo
    print(f'         active {coinsamo:-20.3f} AMO')
    coinsamo = chain['lostcoins']/oneamo
    ratio = chain['lostcoins'] / chain['coins'] * 100
    print(f'         lost   {coinsamo:-20.3f} AMO ({ratio:.3f}%)')

def step(state):
    state['steps'] += 1
    state['chain']['blks'] += config['stepblks']
    state['chain'] = nplayers.teller(state['chain'])
    state['chain'] = nplayers.depleter(state['chain'])
    return state

def run(state, steps, param):
    for i in range(steps):
        state = step(state)
    display_state(state)
    print()
    return state

txrewardamo = param['txreward']/oneamo
print(f'tx reward: {txrewardamo} AMO / tx')
state['chain']['activecoins'] = param['initialcoins']
state['chain'] = nplayers.sum_up_coins(state['chain'])

nplayers.param = param

print()
for i in range(10):
    state = run(state, config['steps'], {})

#!/usr/bin/env python3
# -*- coding: utf-8 -*-
# vim: set sw=4 ts=4 expandtab :

import players
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
        'blktxsize': 100,
        }
state = {
        'steps': 0,
        'chain': {
            'blks': 0,
            # assets
            'coins': param['initialcoins'],
            'activecoins': param['initialcoins'],
            'lostcoins': 0,
            'stakes': 0,
            'delstakes': 0,
            # tx dynamics
            'txgen': 0,
            'txpending': 0,
            'txfee': 0,
            },
        'market': {
            'liveness': 0,
            'value': 0,
            }
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
    players.invisible(state)
    players.users(state)
    nplayers.teller(state['chain'])
    nplayers.depleter(state['chain'])

def run(state, steps, param):
    for i in range(steps):
        step(state)
    display_state(state)
    print()

txrewardamo = param['txreward']/oneamo
print(f'tx reward: {txrewardamo} AMO / tx')

players.config = config
nplayers.config = config
players.param = param
nplayers.param = param

print()
for i in range(10):
    run(state, config['steps'], {})

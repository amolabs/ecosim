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
domain = {
        'initialcoins': 20000000000*oneamo,
        'txreward': 0.1*oneamo,
        'blktxsize': 1000,
        }
state = {
        # time
        'steps': 0,
        'blks': 0,
        # assets
        'coins': 0,
        'activecoins': 0,
        'lostcoins': 0,
        'stakes': 0,
        'delstakes': 0,
        # dynamic parameters
        'txgen': 0,
        'txpending': 0,
        'txfee': 0,
        }

def display_state(state):
    coinsamo = state['coins']/oneamo
    print(f'  coins: total  {coinsamo:-20.3f} AMO')
    coinsamo = state['activecoins']/oneamo
    print(f'         active {coinsamo:-20.3f} AMO')
    coinsamo = state['lostcoins']/oneamo
    ratio = state['lostcoins'] / state['coins'] * 100
    print(f'         lost   {coinsamo:-20.3f} AMO ({ratio:.3f}%)')

def step(state):
    state['steps'] += 1
    state['blks'] += config['stepblks']
    state = nplayers.teller(state)
    state = nplayers.depleter(state)
    return state

def run(state, steps, param):
    for i in range(steps):
        state = step(state)
    days = state['blks']/60/60/24
    print(f'run steps: {steps}, {state["blks"]} blocks = {days} days')
    display_state(state)
    print()
    return state

txrewardamo = domain['txreward']/oneamo
print(f'tx reward: {txrewardamo} AMO / tx')
state['activecoins'] = domain['initialcoins']
state['coins'] = state['activecoins'] + state['lostcoins'] + state['stakes'] + state['delstakes']

nplayers.domain = domain

print()
for i in range(10):
    state = run(state, config['steps'], {})

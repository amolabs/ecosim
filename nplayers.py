# vim: set sw=4 ts=4 expandtab :

from const import *

FEECAP = 10000*oneamo

def sum_up_coins(chain):
    chain['coins'] = chain['activecoins'] + chain['lostcoins'] + chain['stakes']

def teller(chain):
    tx_to_process = min(
            chain['txpending'],
            param['blktxsize'] * config['stepblks']
            )
    chain['txproc'] += tx_to_process
    chain['txpending'] -= tx_to_process
    # reward
    reward = int(tx_to_process * param['txreward'])
    chain['activecoins'] += reward
    # TODO: use more plausible formula
    chain['txfee'] = int(chain['txpending'] * oneamo * 0.01)
    #chain['txfee'] = 0
    # sum up
    sum_up_coins(chain)

def depleter(chain):
    # asset loss
    depletion = int(chain['activecoins'] * 0.0001) # TODO: depletion rate
    chain['activecoins'] -= depletion
    chain['lostcoins'] += depletion
    # tx loss
    txlost = int(chain['txpending'] * 0.0001) # TODO: tx lost rate
    chain['txlost'] += txlost
    chain['txpending'] -= txlost
    # sum up
    sum_up_coins(chain)

# invisible hand
def invisible(state):
    # update liveness
    fee_factor = FEECAP / (state['chain']['txfee'] + FEECAP)
    tmp = state['market']['liveness'] * fee_factor * param['growth_factor']
    tmp = max(tmp, 0.001) # TODO: minimum liveness
    state['market']['liveness'] = tmp


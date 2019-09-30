# vim: set sw=4 ts=4 expandtab :

from const import *

def teller(chain):
    global tx_to_process ### used in invisible
    tx_to_process = min(
            chain['txpending'],
            param['blktxsize'] * config['stepblks']
            )
    chain['stat_txproc'] = tx_to_process
    chain['txpending'] -= tx_to_process
    # reward
    reward = int(tx_to_process * param['txreward'])
    chain['coins'] += reward
    chain['coins_active'] += reward

def depleter(chain):
    # asset loss
    depletion = int(chain['coins_active'] * param['deplete_coin'])
    chain['coins_active'] -= depletion
    chain['coins_lost'] += depletion
    # tx loss
    txlost = int(chain['txpending'] * param['deplete_tx'])
    chain['stat_txlost'] += txlost
    chain['txpending'] -= txlost

# invisible hand
def invisible(state):
    chain = state['chain']
    market = state['market']

    global debug1, debug2

    # update tx fee
    # TODO: use more plausible formula
    fee_usd = chain['txpending'] * param['feescale'] * 0.0001
    #print(f'fee_use ={fee_usd}')
    chain['txfee'] = int(fee_usd / market['exchange_rate'] * oneamo)
    #chain['txfee'] = 0

    # update liveness
    tmp = market['liveness']
    # inflation by growth factor
    tmp *= param['growth_factor']
    # suppression by tx fee
    fee_factor = param['feescale'] / (fee_usd + param['feescale'])
    tmp *= fee_factor
    # TODO: minimum liveness
    tmp = max(tmp, 0.001)
    market['liveness'] = tmp

    # interest rate of the chain
    # (augment with very small bias to chain)
    gain_chain = tx_to_process \
            * (chain['txfee'] + param['txreward']) \
            * BLKSYEAR / config['stepblks'] \
            / (chain['stakes'] + DELTA_MOTE)
    market['interest_chain'] = gain_chain


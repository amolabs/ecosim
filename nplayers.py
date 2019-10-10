# vim: set sw=4 ts=4 expandtab :

from const import *
import math

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

    # update market value
    tmp = market['value']
    tmp += market['liveness'] * config['stepblks']
    #tmp *= math.log10(market['liveness'] + 1) + 1
    #tmp *= param['growth_factor']
    # XXX: minimum liveness
    tmp = max(tmp, 0.001)
    market['value'] = tmp

    # update tx fee
    # estimate remaining blocks until all of the currently pending txs would be
    # processed
    # one param['feescale'] USD for one day
    blks = chain['txpending'] / param['blktxsize']
    fee_usd = param['feescale'] * blks / (60*60*24) # in USD
    fee = int(fee_usd / market['exchange_rate'] * oneamo) # in mote
    # update
    smooth = config['smooth'] / config['stepblks']
    chain['txfee'] = int((fee + (smooth-1)*chain['txfee']) / smooth)

    # update liveness
    tmp = market['liveness']
    # increase by growth factor
    f = math.pow(param['growth_factor'], config['stepblks'])
    ## suppress by tx fee
    fee_usd = chain['txfee'] / oneamo * market['exchange_rate']
    f *= param['feescale'] / (fee_usd * config['stepblks'] + param['feescale'])
    #fee_factor = math.log10(fee_factor) + 1
    tmp *= f
    # TODO: minimum liveness
    tmp = max(tmp, 0.001)
    smooth = config['smooth'] / config['stepblks']
    market['liveness'] = (tmp + (smooth-1)*market['liveness']) / smooth

    # projected yearly interest of the chain
    # (augment with very small bias to chain)
    gain_chain = tx_to_process \
            * (chain['txfee'] + param['txreward']) \
            * BLKSYEAR / config['stepblks'] \
            / (chain['stakes'] + DELTA_MOTE)
    market['interest_chain'] = min(gain_chain, 100)
    #market['interest_chain'] = gain_chain

    # update exchange rate
    exch = market['value'] \
            / (chain['coins_active'] + chain['stakes'] * 0.0001) \
            * oneamo
    # update
    smooth = config['smooth'] / config['stepblks']
    market['exchange_rate'] = (exch + (smooth-1)*market['exchange_rate']) / smooth
    #market['exchange_rate'] = exch

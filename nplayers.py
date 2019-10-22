# vim: set sw=4 ts=4 expandtab :

from const import *

def teller(chain):
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

# invisible hand to intermediate supply and demand
def invisible(state):
    chain = state['chain']
    market = state['market']

    # update tx fee
    # estimate remaining blocks until all of the currently pending txs would be
    # processed
    # one param['feescale'] USD for one hour
    avg_pending = sum(hist['txpending']) / len(hist['txpending'])
    blks = avg_pending / param['blktxsize']
    fee_usd = param['feescale'] * blks / BLKSHOUR # in USD
    fee = int(fee_usd / market['exchange_rate'] * oneamo) # in mote
    # update
    chain['txfee'] = fee
    #smooth = config['smooth'] / config['stepblks']
    #chain['txfee'] = int((fee + (smooth-1)*chain['txfee']) / smooth)

    # update exchange rate
    exch = market['value'] \
            / (chain['coins_active'] + chain['stakes'] * 0.0001) \
            * oneamo
    # update
    smooth = max(int(config['smooth'] / config['stepblks']), 2)
    market['exchange_rate'] = (exch + (smooth-1)*market['exchange_rate']) / smooth

hist_size = 1
hist = {
        'txproc': [0],
        'txpending': [0],
        'txfee': [0],
        'stakes': [0],
        'exch': [],
        }
def historian(state):
    hist['txproc'].append(state['chain']['stat_txproc'])
    hist['txpending'].append(state['chain']['txpending'])
    hist['txfee'].append(state['chain']['txfee'])
    hist['stakes'].append(state['chain']['stakes'])
    hist['exch'].append(state['market']['exchange_rate'])
    l = len(hist['txpending'])
    if l > hist_size:
        hist['txproc'] = hist['txproc'][l-hist_size:]
        hist['txpending'] = hist['txpending'][l-hist_size:]
        hist['txfee'] = hist['txfee'][l-hist_size:]
        hist['stakes'] = hist['stakes'][l-hist_size:]
        hist['exch'] = hist['exch'][l-hist_size:]

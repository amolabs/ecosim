# vim: set sw=4 ts=4 expandtab :

from const import *
import math

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

    # update market value
    tmp = market['value']
    ## method 1
    #tmp *= math.pow(param['growth_factor'], config['stepblks'] / BLKSDAY)
    #tmp = max(tmp, 0.001)
    #market['value'] = tmp
    ## method 2
    #tmp *= math.pow(0.3, chain['blks'] / BLKSMONTH)
    #market['value'] += tmp
    ## method 3
    x = chain['blks'] / BLKSMONTH
    market['value'] = \
            param['f_gdp_month'][3] * x**3 \
            + param['f_gdp_month'][2] * x**2 \
            + param['f_gdp_month'][1] * x \
            + param['f_gdp_month'][0]
    ## others
    #tmp *= math.log10(market['liveness'] + 1) + 1
    #tmp *= param['growth_factor']
    #tmp *= param['growth_factor'] / (fee_usd + param['feescale'])
    #tmp *= math.pow(param['growth_factor'], config['stepblks'] / BLKSMONTH)

    # update tx fee
    # estimate remaining blocks until all of the currently pending txs would be
    # processed
    # one param['feescale'] USD for one hour
    avg_pending = sum(hist['txpending']) / len(hist['txpending'])
    blks = avg_pending / param['blktxsize']
    fee_usd = param['feescale'] * blks / BLKSHOUR # in USD
    fee = int(fee_usd / market['exchange_rate'] * moteperamo)
    # update
    chain['txfee'] = fee
    #smooth = config['smooth'] / config['stepblks']
    #chain['txfee'] = int((fee + (smooth-1)*chain['txfee']) / smooth)

    # update exchange rate
    if len(hist['exch']) == 0:
        avg_exch = market['exchange_rate']
    else:
        avg_exch = sum(hist['exch']) / len(hist['exch'])
    usdperamo = avg_exch
    demand = 0
    supply = 0
    ## money demand for market trade
    v = param['velocity']
    coin_value = chain['coins_active'] / moteperamo * usdperamo
    market_value = market['value']
    demand += market_value / v
    supply += coin_value
    ## money demand for storing value
    #sc = chain['stakes']
    #demand += (market['interest_stake'] * sc) / market['interest_world'] - sc
    ## money demand for staking
    h = hist['stakes']
    l = len(h)
    change = (h[l-1] - h[l-2]) / moteperamo * usdperamo
    if change > 0:
        demand += change
    else:
        supply += change
    ## money demand from short-term compensation
    demand += chain['coins_active'] / moteperamo * (avg_exch - usdperamo)
    ## money demand from long-term expectation
    demand += chain['coins'] / moteperamo * (usdperamo - avg_exch)
    ## sum up
    exch = demand / supply 
    ## smoothing
    smooth = max(int(config['smooth'] / config['stepblks']), 2)
    old = market['exchange_rate']
    market['exchange_rate'] = (exch + (smooth-1)*old) / smooth

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

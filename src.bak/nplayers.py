# vim: set sw=4 ts=4 expandtab :

from const import *
import math
from scipy import stats

def teller(state, nstate):
    nchain = nstate['chain']

    # mimic network unpredictability using random variable
    df = int(math.log10(nchain['txpending'] + 10))
    rv = stats.chi2(df)
    #lazy_txs = int(0.01 * nchain['txpending'] * rv.rvs() / df)
    lazy_txs = int(0.1 * nchain['txpending'])
    #lazy_txs = min(lazy_txs, nchain['txpending']) # compensate rv.rvs()
    tx_to_process = min(
            nchain['txpending'] - lazy_txs,
            param['blktxsize'] * config['stepblks']
            )
    nchain['stat_txproc'] = tx_to_process
    nchain['txpending'] -= tx_to_process
    # reward
    reward = int(tx_to_process * param['txreward'])
    #reward = int(tx_to_process * param['txreward'] * 10)
    #reward = int(config['stepblks']*10*moteperamo)
    nchain['coins'] += reward
    nchain['coins_active'] += reward

def depleter(state, nstate):
    chain = state['chain']
    # asset loss
    depletion = int(chain['coins_active'] * param['deplete_coin'])
    nstate['chain']['coins_active'] -= depletion
    nstate['chain']['coins_lost'] += depletion
    # tx loss
    txlost = int(chain['txpending'] * param['deplete_tx'])
    nstate['chain']['accum_txlost'] += txlost
    nstate['chain']['txpending'] -= txlost

# invisible hand to intermediate supply and demand
def invisible(state, nstate):
    chain = state['chain']
    market = state['market']

    # get usdperamo
    if len(hist['exch']) == 0:
        avg_exch = market['exchange_rate']
    else:
        avg_exch = sum(hist['exch']) / len(hist['exch'])
    usdperamo = avg_exch

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
    value = param['f_gdp_month'][3] * x**3 \
            + param['f_gdp_month'][2] * x**2 \
            + param['f_gdp_month'][1] * x \
            + param['f_gdp_month'][0]
    ## others
    #tmp *= math.log10(market['liveness'] + 1) + 1
    #tmp *= param['growth_factor']
    #tmp *= param['growth_factor'] / (fee_usd + param['feescale'])
    #tmp *= math.pow(param['growth_factor'], config['stepblks'] / BLKSMONTH)
    nstate['market']['value'] = max(value, 0)

    # update tx fee
    # estimate remaining blocks until all of the currently pending txs would be
    # processed
    # one param['feescale'] USD for one hour
    avg_pending = sum(hist['txpending']) / len(hist['txpending'])
    blks = avg_pending / param['blktxsize']
    fee_usd = param['feescale'] * blks / BLKSHOUR
    fee = int(fee_usd / usdperamo * moteperamo)
    # update
    nstate['chain']['txfee'] = fee
    #smooth = max(int(config['smooth'] / config['stepblks']), 2)
    #chain['txfee'] = int((fee + (smooth-1)*chain['txfee']) / smooth)

    # TODO: consider these (when assessing demand):
    # - expected (real) rate of return
    #   - current exchage rate
    #   - expected exchange rate in the future
    #   - current interest rate
    # - risk and uncertainty
    # - liquidity

    # update exchange rate
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
    ## money demand from short-term negative feedback
    fb = chain['coins_active'] / moteperamo / 10 \
            * (avg_exch - market['exchange_rate'])
    if fb > 0:
        demand += fb
    else:
        supply += -fb
    ## money demand from long-term expectation
    #f = chain['coins'] / moteperamo \
    #        * (market['exchange_rate'] - avg_exch)
    #if f > 0:
    #    demand += f
    #else:
    #    supply += -f
    ## sum up
    # avoid infinity
    demand = min(demand, chain['coins'] / moteperamo * usdperamo)
    # avoid divide-by-zero error
    supply = max(supply, DELTA_AMO)
    exch = demand / supply 
    ## smoothing
    smooth = max(int(config['smooth'] / config['stepblks']), 2)
    old = market['exchange_rate']
    nstate['market']['exchange_rate'] = (exch + (smooth-1)*old) / smooth

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

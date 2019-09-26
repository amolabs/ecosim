# vim: set sw=4 ts=4 expandtab :

def sum_up_coins(chain):
    chain['coins'] = chain['activecoins'] + chain['lostcoins'] + chain['stakes'] + chain['delstakes']
    return chain

def teller(chain):
    tx_to_process = min(chain['txpending'], param['blktxsize'])
    chain['txpending'] -= tx_to_process
    reward = int(tx_to_process * param['txreward'])
    chain['activecoins'] += reward

    # TODO: calc chain['txfee'] from chain['txpending']

    return sum_up_coins(chain)

def depleter(chain):
    depletion = int(chain['activecoins'] * 0.00005) # TODO: depletion rate
    chain['activecoins'] -= depletion
    chain['lostcoins'] += depletion

    lost = int(chain['txpending'] * 0.01) # TODO: tx lost rate
    chain['txpending'] -= lost

    return sum_up_coins(chain)

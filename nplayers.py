# vim: set sw=4 ts=4 expandtab :

def sum_up_coins(chain):
    chain['coins'] = chain['activecoins'] + chain['lostcoins'] + chain['stakes'] + chain['delstakes']

def teller(chain):
    tx_to_process = min(
            chain['txpending'],
            param['blktxsize'] * config['stepblks']
            )
    chain['txpending'] -= tx_to_process
    # reward
    reward = int(tx_to_process * param['txreward'])
    chain['activecoins'] += reward
    # TODO: calc chain['txfee'] from chain['txpending']
    # sum up
    sum_up_coins(chain)

def depleter(chain):
    # asset loss
    depletion = int(chain['activecoins'] * 0.00005) # TODO: depletion rate
    chain['activecoins'] -= depletion
    chain['lostcoins'] += depletion
    # tx loss
    lost = int(chain['txpending'] * 0.01) # TODO: tx lost rate
    chain['txpending'] -= lost
    # sum up
    sum_up_coins(chain)

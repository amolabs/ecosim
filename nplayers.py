# vim: set sw=4 ts=4 expandtab :

def sum_up_coins(state):
    state['coins'] = state['activecoins'] + state['lostcoins'] + state['stakes'] + state['delstakes']
    return state

def teller(state):
    tx_to_process = min(state['txpending'], domain['blktxsize'])

    state['txpending'] -= tx_to_process
    reward = int(tx_to_process * domain['txreward'])
    state['activecoins'] += reward

    # TODO: calc state['txfee'] from state['txpending']

    return sum_up_coins(state)

def depleter(state):
    depletion = int(state['activecoins'] * 0.00005) # TODO: depletion rate
    state['activecoins'] -= depletion
    state['lostcoins'] += depletion

    lost = int(state['txpending'] * 0.01) # TODO: tx lost rate
    state['txpending'] -= lost

    return sum_up_coins(state)

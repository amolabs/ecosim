# vim: set sw=4 ts=4 expandtab :

# invisible hand
def invisible(state):
    # update market liveness
    pass

def users(state):
    live = state['market']['liveness']
    txs = 0 # TODO
    state['chain']['txpending'] = txs

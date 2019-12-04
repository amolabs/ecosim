# -*- coding: utf-8 -*-
# vim: set sw=4 ts=4 expandtab :

from numpy import poly1d
import math

from const import *

def init_gdp(gdp_coeff):
    global gdp_func
    gdp_func = poly1d(gdp_coeff)

def get_output(state):
    y0 = gdp_func(state.steps)
    if config['dormant']:
        ms = state.coins_active + state.coins_dormant
    else:
        ms = state.coins_active
    p = state.price_level
    r = state.interest_amo
    v = param['velocity']
    c = param['transfer_cost_factor']

    y = 2 * r / c * (ms * v / p)**2
    output = min(y0, y)
    #print(y0, y, output)
    #output = y0

    return output

def get_money_demand(state):
    p = state.price_level
    y = state.output
    r = state.interest_amo
    v = param['velocity']
    c = param['transfer_cost_factor']
    r = max(r, TINY)
    y = max(y, TINY)
    L = math.sqrt((c * y) / (2 * r))
    d = p / v * L
    return (d, L)

def get_price_amo(state):
    if config['dormant']:
        ms = state.coins_active + state.coins_dormant
    else:
        ms = state.coins_active
    p = state.price_level
    y = state.output
    r = state.interest_amo
    v = param['velocity']
    c = param['transfer_cost_factor']
    #L = math.sqrt((c * y) / (2 * r))
    #p = ms * v / L
    #p = ms * v / y
    #p = ms * v / y * (1 + r)
    p = ms * v / y * (1 - r)
    #p = ms * v / y * (1 - r + state.txfee/p)
    #p = 1/state.usdperamo
    return p

def get_exrate_long(state):
    p_usd = state.price_usd
    p_amo = state.price_level
    p_amo = max(p_amo, TINY)
    exrate_long = p_usd / p_amo
    return exrate_long

def get_exrate_short(state, exrate_long):
    global debug
    r_usd = state.interest_usd
    r_amo = state.interest_amo
    # XXX: this formula breaks when the denominator goes to negative
    # exrate_short = exrate_long / (r_usd - r_amo + 1)
    den = max(r_usd - r_amo + 1, TINY)
    exrate_short = exrate_long / den
    return exrate_short

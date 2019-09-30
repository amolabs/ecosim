# AMO economy simulation

## Configuration
### Simulation config
- simulation step size (in blocks or seconds)
- simulation steps

### Fixed domain parameters
The domain parameters are static and read-only. They are fixed unless there is
a fork of the chain. They affect behavior of both players and non-players.

chain parameters:
- initial amount of active coins
- block and tx reward
- max number of txs in a block

market parameters:
- initial market liveness
- initial market value
- initial coin exchange rate
- tx generate factor: controls the number of newly generated txs
- market growth factor: controls dynamics of market liveness

## Simulation Steps
The simulation runs a model in steps. A model is a state machine and keeps its
internal state which consists of blockchain state and market state. In every
step, the state is changed by the state transition function, which consists of
severral actors as defined in later sections in this document.

## Simulation state
### General
Simulation statistics:
- total number of simulation steps elapsed

### Blockchain state
Simulation statistics for tx processing:
- total number of blocks generated (this measures time elapsed)
- total number of txs generated
- total number of txs processed and included in blocks
- total number of txs lost due to computing environment

Tx status:
- current number of txs pending in blockchain nodes
- current tx fee

Asset status:
- sum of all coins = sum of all active, lost and locked coins(stakes)
- sum of all active coins
- sum of all lost coins due to lost account keys and etc.
- sum of all stakes including delegated stakes


### Market state
- market liveness: controls the number of newly generated txs
- <s>market value: total value of all goods ready to be sold in the market (in
  USD)</s>
- coin exchange rate (in USD for one AMO)

*NOTE: This is the only place where we use the unit USD.*

## Player actors
Players have their own desires and decision making principles. Each *player*
represents all entities of the same type, and appears as a single function in
the simulation.

### User
CURRENT

- increase the number of generated txs based on the current market liveness

DRAFT

User represents the whole set of users.

#### desires
- <s>want to sell coins (in USD)</s>
- <s>want to buy coins (in USD)</s>
- want to sell goods (in AMO)
- want to buy goods (in AMO)
- want to delegate/retract coins

#### conditions
- tx fee

#### decisions
- <s>sell coins</s>
- <s>buy coins</s>
- sell goods
- buy goods
- delegate/retract coins

#### effect
- increase/decrease tx generation rate (txs per second)
- increase/decrease delegated stakes

### Validator
CURRENT

Calculate the following:
- gain per one AMO from chain: expected income in USD from stakes
- gain per one AMO from market: expected income in USD by selling coins

If the gain from the chain is higher than the gain from the market, increase
stakes and decrease active coins. Otherwise, decrease stakes and increase
active coins.


- increase/decrease staked coins based on the number of pending txs, tx fee and
  tx reward
- increase/decrease the sum of active coins accordingly

DRAFT

Validator represents the whole set of validators.

#### desires
- want to increase/decrease stake (in AMO)

#### conditions
- tx fee
- tx generation rate

#### decisions
- increase/decrease stake

#### effect
- increase/decrease stake

## Non-player actors
Non-players don't have their own desires. Each non-player just calculate its
output from the input based on the pre-determined rules. Non-players represents
activities from AMO blockchain protocol execution or some environmental change.

### Teller
- decrease the number of pending txs based on block size
- calculate block and tx reward and increase active coins accordingly

### Depleter
- convert small amount of active coins to lost coins (asset loss due to lost
  account keys)
- decrease small number of pending txs (tx loss due to network problem or block
  limit)

### Invisible hand
- update market liveness based on the current tx fee and market growth factor
- calculate tx fee based on the number of pending txs<br/>
  *NOTE: Tx fee is zero when there is no pending txs.*

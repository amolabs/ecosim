# AMO economy simulation

## Configuration
### Simulation config
- simulation step size (in blocks or seconds)
- simulation steps
- smoothing factor

### Fixed domain parameters
The domain parameters are static and read-only. They are fixed unless there is
a fork of the chain. They affect behavior of both players and non-players.

chain parameters:
- initial amount of active coins
- block and tx reward
- max number of txs in a block
- scale factor for tx fee dynamics
- maximum stake change
- maximum stake ratio

market parameters:
- initial market liveness
- initial market value
- initial coin exchange rate
- initial interest rate of the outer world
- tx generate factor: controls the number of newly generated txs
- base number of txs for each block
- market growth factor: controls dynamics of market liveness

depletion parameters:
- depletion rate for active coins
- depletion rate for pending txs

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
- number of newly generated txs in the last step
- number of processed txs in the last step
- number of lost txs in the last step

Tx status:
- current number of txs pending in blockchain nodes
- current tx fee

Chain asset status:
- sum of all coins = sum of all active, lost and locked coins(stakes)
- sum of all active coins
- sum of all lost coins due to lost account keys and etc.
- sum of all stakes and delegated stakes

### Market state
- market liveness: controls the number of newly generated txs
- market value: total value of all goods ready to be traded in the market (in
  USD)
- coin exchange rate (in USD for one AMO)
- interest rate of the chain
- interest rate of the outer world

*NOTE: This is the only place where we use the unit USD.*

## Player actors
Players have their own desires and decision making principles. To mimic
real-world human decisions, a few random variables are used when calculating
their decisions. Each *player* represents all entities of the same type, and
appears as a single function in the simulation.

### User
Represents user activities in the chain and market.
- update market liveness
- update market value
- generates txs

#### conditions
- recent tx fee

<img src="/tex/dad2781bbd2dc042c5799137bcdc46ed.svg?invert_in_darkmode&sanitize=true" align=middle width=100.62865229999998pt height=34.8495345pt/>,

where <img src="/tex/9fc047b08afaea3d40c2896fa64857ad.svg?invert_in_darkmode&sanitize=true" align=middle width=28.99259879999999pt height=22.831056599999986pt/> is the average fee during the recent <img src="/tex/55a049b8f161ae7cfeb0197d75aff967.svg?invert_in_darkmode&sanitize=true" align=middle width=9.86687624999999pt height=14.15524440000002pt/> blocks.

#### TODO
- desires
	- <s>want to sell coins (in USD)</s>
	- <s>want to buy coins (in USD)</s>
	- want to sell goods (in AMO)
	- want to buy goods (in AMO)
	- want to delegate/retract coins
- decisions
	- <s>sell coins</s>
	- <s>buy coins</s>
	- sell goods
	- buy goods
	- delegate/retract coins

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
Non-players don't have their own desires, so no random variable is used when
calculating their actions. Each non-player just calculate its output from the
input based on the pre-determined rules. Non-players represents activities from
AMO blockchain protocol execution or some environmental change.

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

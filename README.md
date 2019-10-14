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
- tx generation factor: controls the number of newly generated txs
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

The recent tx fee is the average fee during the recent <img src="/tex/55a049b8f161ae7cfeb0197d75aff967.svg?invert_in_darkmode&sanitize=true" align=middle width=9.86687624999999pt height=14.15524440000002pt/> blocks:<br/>
<img src="/tex/ca19c79ddce1a75b1a8ea4bf5c4530be.svg?invert_in_darkmode&sanitize=true" align=middle width=100.62865229999998pt height=34.8495345pt/>.

The suppressing factor <img src="/tex/3e18a4a28fdee1744e5e3f79d13b9ff6.svg?invert_in_darkmode&sanitize=true" align=middle width=7.11380504999999pt height=14.15524440000002pt/> by the tx fee is:<br/>
<img src="/tex/ff2f17f31efade69b738b5b5340c9c78.svg?invert_in_darkmode&sanitize=true" align=middle width=100.93170944999999pt height=30.648287999999997pt/>.

#### state change
The market liveness <img src="/tex/5acce2d88b3044bc6cbf5d7b0860db2b.svg?invert_in_darkmode&sanitize=true" align=middle width=9.55577369999999pt height=22.831056599999986pt/> for the step <img src="/tex/77a3b857d53fb44e33b53e4c8b68351a.svg?invert_in_darkmode&sanitize=true" align=middle width=5.663225699999989pt height=21.68300969999999pt/> is <img src="/tex/674588ef0a0704240d287f43381221a9.svg?invert_in_darkmode&sanitize=true" align=middle width=75.0436764pt height=22.831056599999986pt/>, where
<img src="/tex/3cf4fbd05970446973fc3d9fa3fe3c41.svg?invert_in_darkmode&sanitize=true" align=middle width=8.430376349999989pt height=14.15524440000002pt/> is the growing factor and <img src="/tex/3e18a4a28fdee1744e5e3f79d13b9ff6.svg?invert_in_darkmode&sanitize=true" align=middle width=7.11380504999999pt height=14.15524440000002pt/> is the suppressing factor.

The market value <img src="/tex/f93b76600ef1549fec19f91026179698.svg?invert_in_darkmode&sanitize=true" align=middle width=12.61896569999999pt height=14.15524440000002pt/> for the step <img src="/tex/77a3b857d53fb44e33b53e4c8b68351a.svg?invert_in_darkmode&sanitize=true" align=middle width=5.663225699999989pt height=21.68300969999999pt/> is <img src="/tex/191e1fdecb88064067cf81080faa2a1f.svg?invert_in_darkmode&sanitize=true" align=middle width=108.09074265pt height=29.190975000000005pt/>, where <img src="/tex/3cf4fbd05970446973fc3d9fa3fe3c41.svg?invert_in_darkmode&sanitize=true" align=middle width=8.430376349999989pt height=14.15524440000002pt/> is the growing factor, <img src="/tex/9e0f245dc3cfa0eafdd01fc2a09cc282.svg?invert_in_darkmode&sanitize=true" align=middle width=13.259167349999991pt height=22.831056599999986pt/> is the number of blocks in one
step, and <img src="/tex/091e69068b5b8ca1da78c4d6427002cf.svg?invert_in_darkmode&sanitize=true" align=middle width=18.156910199999988pt height=22.831056599999986pt/> is the number blocks in one day. The market value is adjusted
to <img src="/tex/2eb51615c6366a28eb5c1ec91d3bc91c.svg?invert_in_darkmode&sanitize=true" align=middle width=32.40983954999999pt height=14.15524440000002pt/>, the minimum market value, if it is less than <img src="/tex/2eb51615c6366a28eb5c1ec91d3bc91c.svg?invert_in_darkmode&sanitize=true" align=middle width=32.40983954999999pt height=14.15524440000002pt/>.

The number of txs newly generated <img src="/tex/4b3df27b02447b02ec8ccfe5432e6f38.svg?invert_in_darkmode&sanitize=true" align=middle width=10.58699729999999pt height=20.221802699999984pt/> for the step <img src="/tex/77a3b857d53fb44e33b53e4c8b68351a.svg?invert_in_darkmode&sanitize=true" align=middle width=5.663225699999989pt height=21.68300969999999pt/> is <img src="/tex/7209992aa3ece9e70949351cad6fd695.svg?invert_in_darkmode&sanitize=true" align=middle width=88.96846529999998pt height=23.388043799999995pt/>, where <img src="/tex/01b0465185bb384080bdb4a21f4697d9.svg?invert_in_darkmode&sanitize=true" align=middle width=11.83700594999999pt height=14.15524440000002pt/> is the tx generation
force and <img src="/tex/6dec54c48a0438a5fcde6053bdb9d712.svg?invert_in_darkmode&sanitize=true" align=middle width=8.49888434999999pt height=14.15524440000002pt/> is a random variable from the normal distribution. The number
of newly generated txs is adjusted to the base tx number for each block times
the number of blocks in one step if it is too small.

The tx generation force <img src="/tex/0fe1677705e987cac4f589ed600aa6b3.svg?invert_in_darkmode&sanitize=true" align=middle width=9.046852649999991pt height=14.15524440000002pt/> is <img src="/tex/93a321dfcba4d1310995676da8995e8a.svg?invert_in_darkmode&sanitize=true" align=middle width=82.79624264999998pt height=22.831056599999986pt/>, where <img src="/tex/f4da4daa1670931b39e93a753c99e1c2.svg?invert_in_darkmode&sanitize=true" align=middle width=12.76206689999999pt height=20.221802699999984pt/> is tx generation factor, <img src="/tex/f93b76600ef1549fec19f91026179698.svg?invert_in_darkmode&sanitize=true" align=middle width=12.61896569999999pt height=14.15524440000002pt/> is the market value for the step <img src="/tex/77a3b857d53fb44e33b53e4c8b68351a.svg?invert_in_darkmode&sanitize=true" align=middle width=5.663225699999989pt height=21.68300969999999pt/>, <img src="/tex/6182105e328f9f63f1a3794f894df2be.svg?invert_in_darkmode&sanitize=true" align=middle width=13.259167349999991pt height=22.831056599999986pt/> is the number of blocks in one step, and <img src="/tex/3e18a4a28fdee1744e5e3f79d13b9ff6.svg?invert_in_darkmode&sanitize=true" align=middle width=7.11380504999999pt height=14.15524440000002pt/> is the suppressing factor.

#### TODO
- desires
	- want to sell coins (in USD)
	- want to buy coins (in USD)
	- want to sell goods (in AMO)
	- want to buy goods (in AMO)
	- want to delegate/retract coins
- decisions
	- sell coins
	- buy coins
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

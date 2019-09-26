# AMO economy simulation

## Model
The model comprises of the domain, players and non-players.

## Configuration
- simulation step size (in blocks or seconds)
- simulation steps

## Domain
### Domain parameters
The domain parameters are static and read-only. They are fixed unless there is
a fork of the chain. They affect behavior of the players.
- initial amount of active coins
- block and tx reward
- block size
- block interval

These parameters may appear in modified forms.

### Domain input
The domain input is dynamic but read-only. It is controlled outside of the
simulation.
- market liveness: appears as a rational number between 0 and 1
- market value: total value of all goods ready to be sold in the market (in
  USD)

### Domain variables
The domain variables are dynamic and can be change in the simulation. They are
input and also output of the players.
- sum of all coins = sum of all active, lost and locked coins
	- sum of all active coins
	- sum of all lost coins
	- sum of all locked coins = sum of all stakes and delegated stakes
		- sum of all stakes
		- sum of all delegated stakes
- tx generation rate
- number of pending txs
- tx fee

### Derived domain variables
calculated directly from the domain input and domain variables
- coin exchange rate (in USD per one AMO)

NOTE: As in classic textbooks, coin exchange rate would be determined in some
time by supply and demand. But, we assume this process completes almost
instantly in the early versions of this simulation.

## Players
Players have their own desires and decision making principles. Each *player*
represents all entities of the same type, and appears as a single function in
the simulation.

### User
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

## Non-players
Non-players don't have their own desires and don't decide anything. Each
non-player just calculate its output from the input based on the pre-determined
rules. Non-players represents activities from AMO blockchain protocol execution
or some plausible environmental change.

### Teller
- decrease the number of pending txs based on block size
- calculate tx fee based on the number of pending txs
- calculate block and tx reward and increase active coins accordingly

### Depleter
- convert small amount of active coins to lost coins (asset loss due to user
  key loss)
- decrease small number of pending txs (tx loss due to network problem or block
  limit)

## Simulation Steps
The simulation runs in steps. The model is a state machine and keeps its
internal state which consists of various variables and the set of state
transfer functions.

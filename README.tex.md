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
- sum of all coins = sum of all active, dormant, lost and locked coins(stakes)
- sum of all active coins
- sum of all dormant coins
- sum of all lost coins due to lost account keys and etc.
- sum of all stakes and delegated stakes

### Market state
- market liveness: controls the number of newly generated txs
- market value: total value of all goods ready to be traded in the market (in
  USD)
- coin exchange rate (in USD for one AMO)
- interest rate of the stake
- interest rate of the outer world

*NOTE: This is the only place where we use the unit USD.*

## Player actors
Players have their own desires and decision making principles. To mimic
real-world human decisions, a few random variables are used when calculating
their decisions. Each *player* represents all entities of the same type, and
appears as a single function in the simulation.

### User
Represents user activities in the chain and market.
- generates txs (increase the number of pending txs)

#### conditions
- tx fee trend

The recent tx fee is the average fee during the recent $n$ blocks:
$$
f _ {avg}= \frac{\sum _ {i=1}^{n}{f _ i}}{n},
$$

where $f _ i$ is the tx fee for the step $i$.

The suppressing factor $c$ by the tx fee is:
$$
c = \frac{f _ {scale}}{f _ {avg} ^ 2 + f _ {scale}},
$$

where $f _ {scale}$ is a scaling constant.

#### state change
The number of txs newly generated $t _ i$ for the step $i$ is
$$
t _ i = \frac{\tau _ i}{k} \rho,
$$

where $\tau _ i$ is the tx generation force and $\rho$ is a random variable
from the chi-square distribution with the degree of freedom $k = 32$.

The tx generation force $\tau$ is
$$
\tau _ i = t _ g v _ i b _ s / b _ M c,
$$

where $t _ g$ is tx generation factor per month, $v _ i$ is the market value
for the step $i$, $b _ s$ is the number of blocks in one step, $b _ M$ is the
number of blocks in one month, and $c$ is the suppressing factor.

#### TODO
More complex currency dynamics:
- conditions
	- tx fee trend
	- exchange rate expectation
- desires (affected by exchange rate expectation)
	- want to sell out coins (in USD) (lower money demand)
	- want to stock coins (in USD) (raise money demand)
	- want to sell goods (in AMO) (lower money demand)
	- want to buy goods (in AMO) (raise money demand)
- decisions (affected by tx fee trend)
	- sell coins (lower exchange rate)
	- buy coins (raise exchange rate)
	- sell goods
	- buy goods

### Validator
Represents validator activities in the chain and market.
- update stakes
- update interest rate of the chain

#### conditions
- recent tx fee
- number of processed txs in the last step

The recent tx fee is dealt with as in [user actor](#user) section.

#### state change
The yearly gain $g _ Y$ from the stakes is
$$
g _ Y = t _ {avg} (f _ {avg} + w) b _ Y / b _ s,
$$

where $t _ {avg}$ is average number of processed txs in recent blocks, $w$ is
the reawrd for each tx, $b _ Y$ is the number of blocks in one year, and $b _
s$ is the number of blocks in one step.

The yearly cost for keeping the stakes is
$$
c _ Y = 1000 \log _ {10} \left(\frac {s _ i}{10000} + 1\right).
$$

It means it takes roughly 1,000 USD to keep the stake worth of 100,000 AMO, and
the running cost decreases in log scale. The yearly net gain is $g _ Y - c _
Y$.

The total amount of stakes $s _ i$ for the step $i$ is $s _ i = s _ {i - 1} +
\Delta _ s$, and $\Delta _ s$ is a stake change for the step $i$. The stake
change for the step $i$ is
$$
\Delta _ s = \frac{\sigma _ i - c _ o}{k} \rho,
$$

where $\sigma _ i$ is the stake increase force and $\rho$ is a random variable
from the chi-square distribution with the degree of freedom $k = 32$. $c _ o$
is an opportunity cost by keeping stakes. $\Delta _ s$ is adjusted according to
the total amount of coins. An opportunity cost is half of $s _ {i - 1}$.

The stake increase force $\sigma$ is
$$
\sigma _ i = \frac{g _ Y - c _ Y}{i _ w} - s _ {i - 1},
$$

where $i _ w$ is the interest rate of the outer world.

The interest rate $i _ i$ of the chain for the step $i$ is
$$
i _ i = \frac{g _ Y - c _ Y}{s _ i}.
$$

#### TODO
- desires
	- want to sell coins (in USD)
	- want to buy coins (in USD)

## Non-player actors
Non-players don't have their own desires, so no random variable is used when
calculating their actions. Each non-player just calculate its output from the
input based on the pre-determined rules. Non-players represents activities from
AMO blockchain protocol execution or some environmental change.

### Teller
Represents block generation process of the AMO blockchain protocol.
- process txs (decrease the number of pending txs)
- calculate block and tx reward and increase active coins accordingly

#### state change
The number of processed txs is the mininum of the number of pending txs and
maximum tx capacity of one simulation step.

### Depleter
- convert small amount of active coins to lost coins (asset loss due to lost
  account keys)
- decrease small number of pending txs (tx loss due to network problem or block
  limit)

### Invisible hand
Represents the supply-demand effect of the chain and amrket.
- update market value
- update tx fee
- update coin exchange rate

#### conditions
- the number of pending txs
- the amount of stakes and the amount of active coins

#### state change
TODO

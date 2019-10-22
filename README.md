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

The recent tx fee is the average fee during the recent <img src="/tex/55a049b8f161ae7cfeb0197d75aff967.svg?invert_in_darkmode&sanitize=true" align=middle width=9.86687624999999pt height=14.15524440000002pt/> blocks:
<p align="center"><img src="/tex/44e3b82332f31896f8763d5a1bfa01b9.svg?invert_in_darkmode&sanitize=true" align=middle width=115.9723389pt height=35.837632049999996pt/></p>

where <img src="/tex/c36aec8fe0f01b5750777bb772c5e87f.svg?invert_in_darkmode&sanitize=true" align=middle width=12.69888674999999pt height=22.831056599999986pt/> is the tx fee for the step <img src="/tex/77a3b857d53fb44e33b53e4c8b68351a.svg?invert_in_darkmode&sanitize=true" align=middle width=5.663225699999989pt height=21.68300969999999pt/>.

The suppressing factor <img src="/tex/3e18a4a28fdee1744e5e3f79d13b9ff6.svg?invert_in_darkmode&sanitize=true" align=middle width=7.11380504999999pt height=14.15524440000002pt/> by the tx fee is:
<p align="center"><img src="/tex/b157911ab967a33ba9177ad20c918b48.svg?invert_in_darkmode&sanitize=true" align=middle width=125.988489pt height=40.11336945pt/></p>

where <img src="/tex/282612e439053665bb1226ff4956699b.svg?invert_in_darkmode&sanitize=true" align=middle width=37.71809744999999pt height=22.831056599999986pt/> is a scaling constant.

#### state change
The number of txs newly generated <img src="/tex/4b3df27b02447b02ec8ccfe5432e6f38.svg?invert_in_darkmode&sanitize=true" align=middle width=10.58699729999999pt height=20.221802699999984pt/> for the step <img src="/tex/77a3b857d53fb44e33b53e4c8b68351a.svg?invert_in_darkmode&sanitize=true" align=middle width=5.663225699999989pt height=21.68300969999999pt/> is
<p align="center"><img src="/tex/055e42b396910460bee3edf2a4066590.svg?invert_in_darkmode&sanitize=true" align=middle width=62.99571135pt height=29.47417935pt/></p>

where <img src="/tex/01b0465185bb384080bdb4a21f4697d9.svg?invert_in_darkmode&sanitize=true" align=middle width=11.83700594999999pt height=14.15524440000002pt/> is the tx generation force and <img src="/tex/6dec54c48a0438a5fcde6053bdb9d712.svg?invert_in_darkmode&sanitize=true" align=middle width=8.49888434999999pt height=14.15524440000002pt/> is a random variable
from the chi-square distribution with the degree of freedom <img src="/tex/e22736d49a06f33738cb98ea7cd74076.svg?invert_in_darkmode&sanitize=true" align=middle width=47.43141149999999pt height=22.831056599999986pt/>.

The tx generation force <img src="/tex/0fe1677705e987cac4f589ed600aa6b3.svg?invert_in_darkmode&sanitize=true" align=middle width=9.046852649999991pt height=14.15524440000002pt/> is
<p align="center"><img src="/tex/1a961adf5e360e5bcf325a168a8a08ba.svg?invert_in_darkmode&sanitize=true" align=middle width=98.87270745000001pt height=36.2778141pt/></p>

where <img src="/tex/4a3ffb0f9c9dfb20850580c316fbafdf.svg?invert_in_darkmode&sanitize=true" align=middle width=12.76206689999999pt height=20.221802699999984pt/> is tx generation factor per month, <img src="/tex/f93b76600ef1549fec19f91026179698.svg?invert_in_darkmode&sanitize=true" align=middle width=12.61896569999999pt height=14.15524440000002pt/> is the market value
for the step <img src="/tex/77a3b857d53fb44e33b53e4c8b68351a.svg?invert_in_darkmode&sanitize=true" align=middle width=5.663225699999989pt height=21.68300969999999pt/>, <img src="/tex/9e0f245dc3cfa0eafdd01fc2a09cc282.svg?invert_in_darkmode&sanitize=true" align=middle width=13.259167349999991pt height=22.831056599999986pt/> is the number of blocks in one step, <img src="/tex/d5d2534bdb7c9a1a3a95534dc6df45ad.svg?invert_in_darkmode&sanitize=true" align=middle width=20.82425399999999pt height=22.831056599999986pt/> is the
number of blocks in one month, and <img src="/tex/3e18a4a28fdee1744e5e3f79d13b9ff6.svg?invert_in_darkmode&sanitize=true" align=middle width=7.11380504999999pt height=14.15524440000002pt/> is the suppressing factor.

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
The yearly gain <img src="/tex/7be0f1e15e3fbce9837f235de523b280.svg?invert_in_darkmode&sanitize=true" align=middle width=18.39889094999999pt height=14.15524440000002pt/> from the stakes is
<p align="center"><img src="/tex/71b2d3caa030d6988c5d56b24e48a378.svg?invert_in_darkmode&sanitize=true" align=middle width=189.04448804999998pt height=17.031940199999998pt/></p>

where <img src="/tex/4810117a188cc4fd0ea9b08a78637084.svg?invert_in_darkmode&sanitize=true" align=middle width=26.88070934999999pt height=20.221802699999984pt/> is average number of processed txs in recent blocks, <img src="/tex/31fae8b8b78ebe01cbfbe2fe53832624.svg?invert_in_darkmode&sanitize=true" align=middle width=12.210846449999991pt height=14.15524440000002pt/> is
the reawrd for each tx, <img src="/tex/b102ea7af0287ccf0249911fa1533a34.svg?invert_in_darkmode&sanitize=true" align=middle width=17.613104849999992pt height=22.831056599999986pt/> is the number of blocks in one year, and <img src="/tex/6182105e328f9f63f1a3794f894df2be.svg?invert_in_darkmode&sanitize=true" align=middle width=13.259167349999991pt height=22.831056599999986pt/> is the number of blocks in one step.

The yearly cost for keeping the stakes is
<p align="center"><img src="/tex/ba3c90ff40cdae83e77cef93ca99d378.svg?invert_in_darkmode&sanitize=true" align=middle width=214.2199158pt height=30.1801401pt/></p>

It means it takes roughly 1,000 USD to keep the stake worth of 100,000 AMO, and
the running cost decreases in log scale. The yearly net gain is <img src="/tex/cb57d641cda92b0ac3784e12b989e1a3.svg?invert_in_darkmode&sanitize=true" align=middle width=56.984091449999994pt height=19.1781018pt/>.

The total amount of stakes <img src="/tex/0edbe35c37603976231156391f9e2492.svg?invert_in_darkmode&sanitize=true" align=middle width=12.35637809999999pt height=14.15524440000002pt/> for the step <img src="/tex/77a3b857d53fb44e33b53e4c8b68351a.svg?invert_in_darkmode&sanitize=true" align=middle width=5.663225699999989pt height=21.68300969999999pt/> is <img src="/tex/ed2b6732bd137a68d5675583f0835b3b.svg?invert_in_darkmode&sanitize=true" align=middle width=105.09495644999998pt height=22.465723500000017pt/>, and <img src="/tex/9b025253096a6cf2b081034abcf110b8.svg?invert_in_darkmode&sanitize=true" align=middle width=19.90304249999999pt height=22.465723500000017pt/> is a stake change for the step <img src="/tex/77a3b857d53fb44e33b53e4c8b68351a.svg?invert_in_darkmode&sanitize=true" align=middle width=5.663225699999989pt height=21.68300969999999pt/>. The stake
change for the step <img src="/tex/77a3b857d53fb44e33b53e4c8b68351a.svg?invert_in_darkmode&sanitize=true" align=middle width=5.663225699999989pt height=21.68300969999999pt/> is
<p align="center"><img src="/tex/0c2f6849aadb4b1a65cd783167681ca9.svg?invert_in_darkmode&sanitize=true" align=middle width=109.03425225000001pt height=31.985609699999994pt/></p>

where <img src="/tex/f9c324e7e50e0f16f2de35c791986a03.svg?invert_in_darkmode&sanitize=true" align=middle width=14.04400634999999pt height=14.15524440000002pt/> is the stake increase force and <img src="/tex/6dec54c48a0438a5fcde6053bdb9d712.svg?invert_in_darkmode&sanitize=true" align=middle width=8.49888434999999pt height=14.15524440000002pt/> is a random variable
from the chi-square distribution with the degree of freedom <img src="/tex/e22736d49a06f33738cb98ea7cd74076.svg?invert_in_darkmode&sanitize=true" align=middle width=47.43141149999999pt height=22.831056599999986pt/>. <img src="/tex/fc8f1a70b250a489ab72b5f2a9d3824c.svg?invert_in_darkmode&sanitize=true" align=middle width=13.602406949999992pt height=14.15524440000002pt/>
is an opportunity cost by keeping stakes. <img src="/tex/9b025253096a6cf2b081034abcf110b8.svg?invert_in_darkmode&sanitize=true" align=middle width=19.90304249999999pt height=22.465723500000017pt/> is adjusted according to
the total amount of coins. An opportunity cost is half of <img src="/tex/05c4826da9cf44a960b209aab9ae11bf.svg?invert_in_darkmode&sanitize=true" align=middle width=29.182946099999988pt height=14.15524440000002pt/>.

The stake increase force <img src="/tex/8cda31ed38c6d59d14ebefa440099572.svg?invert_in_darkmode&sanitize=true" align=middle width=9.98290094999999pt height=14.15524440000002pt/> is
<p align="center"><img src="/tex/5520b7cb5ffd822830f9cb5fdad30085.svg?invert_in_darkmode&sanitize=true" align=middle width=153.19693125pt height=34.45133834999999pt/></p>

where <img src="/tex/0d255faee4aa69be1186992f1f423a25.svg?invert_in_darkmode&sanitize=true" align=middle width=15.48254894999999pt height=21.68300969999999pt/> is the interest rate of the outer world.

The interest rate <img src="/tex/577d71a741297d3fefc204ac02b29d49.svg?invert_in_darkmode&sanitize=true" align=middle width=10.314125249999991pt height=21.68300969999999pt/> of the chain for the step <img src="/tex/77a3b857d53fb44e33b53e4c8b68351a.svg?invert_in_darkmode&sanitize=true" align=middle width=5.663225699999989pt height=21.68300969999999pt/> is
<p align="center"><img src="/tex/0663fe484827add76da695d635421234.svg?invert_in_darkmode&sanitize=true" align=middle width=99.37104374999998pt height=34.45133834999999pt/></p>

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

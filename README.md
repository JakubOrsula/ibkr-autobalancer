# ibkr-autobalancer

Showcase use of ib api using [ib_insync](https://ib-insync.readthedocs.io/api.html) library.

Demos and working code to implement some basic DCA like strategies are included.

Help is needed and appreciated! If you are able and willing open a pull request!
I might make some issues and specify how they should be implemented and label them as good first issue.

## Strategies

### SPY buy and hold - implemented
Check how much cash is left. More than to buy a share? Buy it. In the [demo](https://github.com/JakubOrsula/ibkr-autobalancer/blob/master/src/demos/basic_demo.ipynb) `VWCE` etf is used.
In the [script](https://github.com/JakubOrsula/ibkr-autobalancer/blob/master/src/strategies/cash_burner.py) you can specify whatever stock you want.
More configurability from command line / settings file coming later.

### Composite portfolio autobalance - not yet
A more complex version of the previous strategy. Keeps balance between assets, like 87.9% IWDA, 11.9% EMIM, 0.2% cash. 
This should be useful for people running things like [hedgies adventure](https://www.bogleheads.org/forum/viewtopic.php?t=272007)
or replicating finax portfolios. If I am not mistaken this is **the** patented finax only feature - rebalancing the portfolio once it deviates more than
the [PATENTED](https://www.finax.eu/sk/blog/rebalansing-pod-lupou-polskych-blogerov) constant.
I have partial implementation of this, but I abandoned it because I replaced the IWDA:EIMI 88:12 with VWRA which does the same thing under the hood.

### Target exposure
This should be useful for folks running slightly leveraged portfolios. Say you got 100k.
You want to get 120k exposure to SPY. You buy some SPUU or UPRO (or whatever) and balance things around as price moves up or down.
This is slightly more complex than it seems to be, you need to account for non-constant delta of leveraged etfs and currency conversion and stuff.
I have a partial implementation for this, since I use FIO (because muh us etfs) I would first implement FIO api and then this strategy.
On higher leverages this will fuck you over.

Future goals include making this versatile enough to support more than just IB but also FIO (because of the us etfs restrictions).
I have also some scripts lying around that upload results to google docs / postgres / yahoo finance, it would be nice to integrate them as well.
If you want these features, please start this repo, so I know there is some interest.

## Installation

If you are a newbie and there's more of you I'm willing to do a twitch stream where I will install this on a bare windows installation.
Tested on python 3.8 but should work on any recent version of python. If not open an issue. The steps are kinda spartan, use issues if your urn into trouble.

### So you need
1. python 3.8 - [windows (7 or newer)](https://www.python.org/downloads/release/python-3812/) (or use windows store),
    for macos use `brew install python` and for linux you already have python.
2. pip - we need to install dependencies somehow. Pip should be already installed on windows
   (just use `py -m pip install --upgrade pip` to make sure it's up-to-date) and mac,
    on ubuntu like distros use `apt install python3-pip`
3. *optional* - in order not to pollute your global installation you should install packages just for your one environment.
    Use `py -m pip install --user virtualenv` on windows and `python3 -m pip install --user virtualenv` on linux/mac
4. [tws](https://www.interactivebrokers.com/en/index.php?f=17713) - to use it with IB

### Setup

1. Clone this repository  `git clone https://github.com/JakubOrsula/ibkr-autobalancer.git` (if you use keys use the git url if you don't have git just download the files as zip)
2. open this repo in terminal `cd ibkr-autobalancer`
3. *optional* set up virtual environment - `py -m venv env` on windows and `python3 -m venv env` on linux/mac
4. *optional* activate the environment - `.\env\Scripts\activate` on windows and `source env/bin/activate` on linux/macos
5. open TWS. Go to `File -> Global configuration... -> API -> Settings`
6. check `Enable ActiveX and Socket Clients`
7. uncheck `Read-Only Api` - I highly recommend trying this on demo account first
8. see if the socket port is 7497. If not either sett it to be 7497 or change it here in code
9. run `jupyter-notebook` in terminal
10. play with code execute the cells see the interesting stuff.

## Usage

Use `python3 main.py` in the root of the project. It will run the cash burner strategy.
Use jupyter notebook in demos to experiment.

## Project structure

All source code is in src. In the demos folder you can find short self-contained demos.
In the strategies folder are strategy implementations.
In the utils folder are various helpers and shorthands.

## Q&A

1. **But why shouldn't I use more advanced strategy tool like [pltl](https://www.pairtradinglab.com/ptltrader)?**
    
    Well if you are looking for complex strategies that run fast you probably should. The pltl has a major disadvantage that it only supports USD as a base currency.
    The major advantage of running this are that it's small, free, low on dependencies and unconstrained  in power.

2. **Will this be maintained?**

    This project originates from my personal script to manage my personal portfolio. I plan to port it over here over time.
    So unless I go broke (possible) and loose my retirement funds it will be maintained

3. **Fio support when?**

    Soon^tm

## Major painpoints and future dev ideas

This section should be converted to issues.

### Support for autologin

Use [this project](https://github.com/IbcAlpha/IBC) or higher abstraction like [this](https://github.com/mvberg/ib-gateway-docker) to avoid login prompts.
Apart from the obvious advantages this has few disadvantages:
1. now you rely on more third party software, you rely on the fact that it will be kept up to date and will not scam you out of your money (they use some cdns which could be attacked)

This lib is used to rebalance long term portfolios. It should not be run more than once a week. I run it once a month.

### Dockerize

This should be fairly straightforward I just don't have the time for it right now.
This should make the setup much easier for amateurs and also make it possible to deploy it on vps.

### Use ib for prices

Currently, prices are taken from yahoo finance which is ideal if you don't pay for market data.
However, there are some folks which do, and it would be nice for them to have the prices straight from ib and not rely on yahoo.

### Other products than stocks/etfs

It would be nice if the script could manage exposure (in strategy 3) using futures as well as leveraged etfs. This involves rollover
and other derivatives specific stuff, so it needs extra work.


### Log trades to external service

I have some partial implementations for this already, I just need to clean them up and verify that they work.
I want to add support for:
1. google docs
2. yahoo finance
3. postgres (hasura and you can connect it to whatever)

## References

+ [this dockerfile](https://github.com/chepurko/IBKR-PTL/blob/master/Dockerfile)

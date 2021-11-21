# ibkr-autobalancer

Ultimate goal of this project is (was) to automate execution of simple DCA-like strategies like:
1. SPY buy and hold - check how much cash is left. More than to buy a share? Buy it. - implemented
2. [Hedgies adventure](https://www.bogleheads.org/forum/viewtopic.php?t=272007) - keep balanced exposure to two (or more) assets.
3. Target exposure - say you got 100k. You want to maintain 150k exposure to SPY. Buy/sell UPRO/SPUU/SPY to maintain it no matter the current price.

Future goals include making this versatile enough to support more than just IB but also FIO (because of the us etfs restrictions).

## Installation

If you are a newbie and there's more of you I'm willing to do a twitch stream where I will install this on a bare windows installation.
Tested on python 3.8 but should work on any recent version of python. If not open an issue. The steps are kinda spartan, use issues if your urn into trouble.

### So you need
1. python - [windows (7 or newer)](https://www.python.org/downloads/release/python-3812/) (or use windows store),
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



## Project structure

All source code is in src. In the demos folder you can find short self-contained demos.
In the strategies folder are strategy implementations.
In the utils folder are various helpers and shorthands.

## Q&A

1. **But why shouldn't I use more advanced strategy tool like ninja?**
    
    Well if you are looking for complex strategies that run fast you probably should.
    The major advantage of running this are that it's small, free, low on dependencies and unconstrained  in power.

2. **Will this be maintained?**

    This project originates from my personal script to manage my personal portfolio. I plan to port it over here over time.
    So unless I go broke (possible) and loose my retirement funds it will be maintained

3. **Fio support when?**

    Soon^tm

## References

+ [this dockerfile](https://github.com/chepurko/IBKR-PTL/blob/master/Dockerfile)
+ 

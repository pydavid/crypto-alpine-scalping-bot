# crypto-alpine-scalping-bot

A dummy scalping bot for trading cryptocurrencies in the most common exchanges.

```
python main.py --help
Usage: main.py [OPTIONS]

Options:
  --position [long|short]      position to open: long or short
  --leverage INTEGER           leverage to use. Minimum is 1.  [required]
  --symbol TEXT                Symbol to trade  [required]
  --mode [isolated]            the mode to open the order: isolated
  --price FLOAT                The price of the symbol we want to fill the
                               order at. If not set use the current market
                               price.
  --amount TEXT                Amount of the symbol to open the order with OR
                               `coin` amount you want to use for the order. In
                               this case, suffix the amount with `coin`
                               [required]
  --margin-coin TEXT           The margin coin to use. Default to USDT
  --take-profit TEXT           The value of the Take Profit. Value of the
                               symbol or percentage of PnL.Once reached, the
                               order will be closed  [required]
  --stop-loss TEXT             The value of the Stop Loss. Value of the symbol
                               or percentage of PnL. Once reached, the order
                               will be closed  [required]
  --wait INTEGER               Wait time in seconds before recreating an order
                               with the same parameter, once the previous one
                               is closed. If not set, does not wait
  --repeat INTEGER             Number of order to make before stopping the
                               script. If not set, does not end
  --exchange [bitget|binance]  Exchange to use for the order  [required]
  --help                       Show this message and exit.
```

## How to install

```
pipenv install
```

## Documentation

1. Set environment variables

```
export API_SECRET_KEY=xxx
export API_ACCESS_KEY=yyy
export API_PASSPHRASE=zzz
```

2. Usage

```
python main.py --position <long|short> --leverage <int> --symbol <symbol-to-trade> --amount <amount-of-symbol-to-buy> --take-profit <take-profit-value> --stop-loss <stop-loss-value> --wait <in-seconds-between-next-trade> --price <value-of-the-symbol-to-buy>" --exchange bitget
```

```
python main.py --position long --leverage 10 --symbol FETUSDT --amount 100 --take-profit 10% --stop-loss 50%  --exchange bitget
```
Will buy 100 FET with a TP of 10% of the Pnl and a SL of -50% of the PnL.

```
python main.py --position long --leverage 10 --symbol FETUSDT --amount 100coin --take-profit 10% --stop-loss 50%  --exchange bitget 
```
Will buy for 100 USDT of FET with a TP of 10% of the Pnl and a SL of -50% of the PnL.

```
python main.py --position long --leverage 10 --symbol FETUSDT --amount 100coin --take-profit 3 --stop-loss 2  --exchange bitget 
```

Will buy for 100 USDT of FET with a TP when 1 FET will worth 3 USDT and a SL when 1 FET will worth 2 USDT.

## Current supported cryptocurrency exchanges

- bitget

## Need help 

Please create an issue if you need a feature/exchange to be implemented.

## Support

If you wish to support the project:

- Ethereum: 0xf11B49666d3386C96Af1A496bFA5688c83B25E8e
- Solana: C7USpoN4kxEm81w3mpK7FuNQ7zcMWY9fqyuacPafRqnk
- Bitcoin (segwit): bc1qcq7fdn4khlsc5ldmlf0ezks8p9r5q2hn04lyy5

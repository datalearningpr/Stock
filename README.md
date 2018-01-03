
# Stock 

This repository holds the small application conducting stock screening.

1. Stock can cover 3 markets: Shanghai, Shenzhen and Hong Kong
2. Three frequencies: day, 30 mins, 5 mins
3. Shanghai, Shenzhen prices can easily get via library tushare, while Hong Kong prices are got from google api(30mins, 5mins), HK day prices obtained via yahoo webscraping, which is slow and unstable.
4. Stock lists are 2 txt files, only a few stocks are inside as examples.
4. Only 2 simple screening rules are demonstrated: MA crossing and Doji pattern recognition. **Hope this will help people to start up and create their own complex and sophisticated method.** Great methods are hardly open-source.
5. Screening is not auto trading, more like half auto, which helps people to pick up proper stocks easily if the rule is given clearly.


### Prerequisites
```
numpy
pandas
matplotlib
wxPython
requests
tushare
talib
```

## License
GPL

## Acknowledgments

Many thanks to different online tutorials online about wxPython, tushare etc.

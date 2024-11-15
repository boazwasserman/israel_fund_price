# israel_fund_price
A web service for obtaining Israeli fund and stock prices into your favorite investment tracking Google Sheet.

## How to use?
To get the price of Israeli funds into your Google Sheets, use the command
```
=IMPORTDATA("https://israel_fund_price.render.com/?id=FUND_ID&source=SOURCE_NAME")
```
replacing "FUND_ID" with the fund number/id on the Tel Aviv Stock Exchange, and SOURCE_NAME with one of currently supported sources:
1. [sponser](https://www.sponser.co.il)
2. [bizportal](https://www.bizportal.co.il)
3. [tase](https://www.tase.co.il)

To run locally, run `python app.py` and then use the URL `http://127.0.0.1:5000/?id=FUND_ID&source=SOURCE_NAME`. But this way you won't be able to load the prices into your Google Sheets, which is a web app that doesn't see your local network.

## What's the issue?
While the GOOGLEFINANCE() API supports most US based stocks and ETFs, for Israeli securities, not all are supported. Specifically, mutual funds seem to not be supported.  
To my knowledge, there is also no official or third party API which is suitable and affordable for personal use.
So, the way to have Israeli fund prices tracked in your favorite spreadsheet was via scraping the prices from the web somehow. People had some success obtaining them from specific spurces via careful use of IMPORTHTML or IMPORTXML, but these seem to be unstable, result in complex commands, and irrelevant for websites that use dynamic content loading.

## Solution
A Flask based Python web service. This gives the flexibility and richness of Python libraries for web parsing like BeautifulSoup and Playwright, which allows for easily getting the prices from multiple sources.  
Making it open source will hopefully allow to adopt it to changes in websites, and possibly add more supported sources.

## Disclaimer
This code and web service obtains Israeli fund prices from third party websites. The code and web service are intended for personal use only, for the purpose of reasonable monitoring of your investments. It is meant to be used in the same way you would normally browse these websites to periodically look at your investment prices.  
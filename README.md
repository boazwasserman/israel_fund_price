# israel_fund_price
A web service for obtaining Israeli fund and stock prices into your favorite investment tracking Google Sheet.

## How to use?
To get the price of Israeli funds into your Google Sheets, the service needs to be exposed to the public internet. This is demonstrated here using [ngrok](https://ngrok.com) developer tunnel service.  
1. Register at ngrok and obtain your personal authtoken. Copy it to a file called `.ngrok_auth`.  
2. If you want to use a constant, static domain for the service, like the one you can get for free with your ngrok account, copy it to a file called `.ngrok_domain`. Otherwise, a random address will be generated every time you run the app.
3. Run `python app.py`  
4. In your desired Google Sheet, use the following command

```
=IMPORTDATA("https://YOUR-STATIC-DOMAIN/?id=FUND_ID&source=SOURCE_NAME")
```
replacing "YOUR-STATIC-DOMAIN" with your ngrok static domain (or random one), "FUND_ID" with the fund number/id on the Tel Aviv Stock Exchange, and SOURCE_NAME with one of currently supported price source names:
1. [sponser](https://www.sponser.co.il)
2. [bizportal](https://www.bizportal.co.il)
3. [tase](https://www.tase.co.il)

To run locally without exposing the app to the public internet, change `RUN_WITH_NGROK` global argument in `app.py` to `False` and simply run `python app.py` and then use the URL `http://127.0.0.1:5000/?id=FUND_ID&source=SOURCE_NAME`. But this way you won't be able to load the prices into Google Sheets, which is a web app that doesn't see your local network.

## Why this is needed?
While the GOOGLEFINANCE() API supports most US based stocks and ETFs, for Israeli securities, not all are supported. Specifically, mutual funds seem to not be supported.  
To my knowledge, there is also no official or third party API which is suitable and affordable for personal use.
So, the way to have Israeli fund prices tracked in your favorite spreadsheet is possible via scraping the prices from the web somehow. People had some success obtaining them from specific spurces via careful use of IMPORTHTML or IMPORTXML, but these seem to be unstable, result in complex commands, and irrelevant for websites that use dynamic content loading.

## Solution
A Flask based Python web service. This gives the flexibility and richness of Python libraries for web parsing like BeautifulSoup and Playwright, which allows for easily getting the prices from multiple sources.  
Making it open source will hopefully allow to adapt it to changes in the source websites, and possibly add more supported sources.

## Disclaimer
This code and web service obtains Israeli fund prices from third party websites. The code and web service are intended for personal use only, for the purpose of reasonable monitoring of your investments. It is meant to be used in the same way you would normally browse these websites to periodically look at your investment prices. Due to this nature, I have no intention of deploying this service as a known website to the public. Users are free to use the proposed ngrok solution.
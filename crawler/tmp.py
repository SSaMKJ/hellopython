
txt='8.75,"threshold":60,"enableOnMuted":true,"showInfoCard":false},"enableRestoreOnNavigate":true,"enableUndockOnNavigate":true,"refreshDockingOnNavigate":true,"totalInactivePlayers":10,"videoClickSrc":["video-click","startScreen"]},"_playerConfig":{}},"QuoteAutoCompleteStore":{"clear":true},"FlyoutStore":{},"NavrailStore":{"showNavrail":false,"navTitle":"finance","navSections":"","currentUrl":"\u002Fquote\u002F005930.KS?p=005930.KS&.tsrc=fin-srch","pageType":{},"navSectionsDisplayTitle":{},"site":"finance"},"StreamDataStore":{"quoteData":{"005930.KS":{"sourceInterval":20,"quoteSourceName":"Delayed Quote","regularMarketOpen":{"raw":55700,"fmt":"55,700.00"},"exchange":"KSC","regularMarketTime":{"raw":1578357041,"fmt":"9:30AM KST"},"fiftyTwoWeekRange":{"raw":"37800.0 - 57300.0","fmt":"37,800.00 - 57,300.00"},"sharesOutstanding":{"raw":5969780224,"fmt":"6B","longFmt":"5969780224"},"regularMarketDayHigh":{"raw":56200,"fmt":"56,200.00"},"shortName":"SamsungElec","longName":"Samsung Electronics Co., Ltd.","exchangeTimezoneName":"Asia\u002FSeoul","regularMarketChange":{"raw":700,"fmt":"700.00"},"regularMarketPreviousClose":{"raw":55500,"fmt":"55,500.00"},"fiftyTwoWeekHighChange":{"raw":-1100,"fmt":"-1,100.00"},"exchangeTimezoneShortName":"KST","fiftyTwoWeekLowChange":{"raw":18400,"fmt":"18,400.00"},"exchangeDataDelayedBy":20,"regularMarketDayLow":{"raw":55600,"fmt":"55,600.00"},"priceHint":2,"currency":"KRW","regularMarketPrice":{"raw":56200,"fmt":"56,200.00"},"regularMarketVolume":{"raw":1602497,"fmt":"1.6M","longFmt":"1602497"},"isLoading":false,"triggerable":false,"gmtOffSetMilliseconds":32400000,"firstTradeDateMilliseconds":946938600000,"region":"US","marketState":"REGULAR","marketCap":{"raw":371685463162880,"fmt":"372T","longFmt":"371,685,463,162,880"},"quoteType":"EQUITY","inv'

def extract_52_high_low(txt):
    key='fiftyTwoWeekRange'
    first_index =txt.index(key)
    print(first_index)
    raw1 = txt[first_index+len(key)+2:first_index+len(key)+100]
    raw_arr1 = raw1.split(",")
    high_low = raw_arr1[0].split(":")[1].replace('"','').replace(' ','').split("-")
    print(high_low)
    low = int(high_low[0].split(".")[0])
    high =  int(high_low[1].split(".")[0])
    print(low)
    print(high)
    return high, low

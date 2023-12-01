def fetch_from_Tv(ticker,exchange,timeframe):
  import warnings
  warnings.simplefilter(action='ignore', category=FutureWarning)

  from mplfinance.original_flavor import candlestick_ohlc
  import matplotlib.dates as mpl_dates
  from tvDatafeed import TvDatafeed, Interval
  tv = TvDatafeed()
  ticker=ticker
  exchange=exchange
  interval=timeframe
  def interval_handling(interval):
    match interval:
      case "1":
        return Interval.in_1_minute
      case "5":
        return Interval.in_5_minute
      case "15":
        return Interval.in_15_minute
      case "1H":
        return Interval.in_1_hour
      case "4H":
        return Interval.in_4_hour
      case "1D":
        return Interval.in_daily
      case "1W":
        return Interval.in_weekly
      case "1M":
        return Interval.in_monthly
  interval_result=interval_handling(interval)

  index_data = tv.get_hist(symbol=ticker,exchange=exchange,interval=interval_result,n_bars=250)
  print("Finished download index_data")

  #Data Handling for TV datafeed
  #Rename of data
  index_data.columns = ["Symbol","Open","High","Low","Close","Vol"]
  #move the index to a new column
  index_data.reset_index(level=0, inplace=True)
  df = index_data.rename(columns = {'index':'date'})
  #Convert date to numdate
  df["Date"] = df["datetime"].apply(mpl_dates.date2num)
  return df

def imb_overtake_trading_signal(ticker,exchange,timeframe):
  import warnings
  warnings.simplefilter(action='ignore', category=FutureWarning)
  #Pre-installed library
  # pip install --upgrade mplfinance
  #!pip install --upgrade --no-cache-dir git+https://github.com/rongardF/tvdatafeed.git
  # pip install --upgrade mplfinance
  # pip install numpy
  #pip install pandas
  # pip install matpoltlib
  

  import pandas as pd
  import numpy as np
  import mplfinance as mpf
  from mplfinance.original_flavor import candlestick_ohlc
  import matplotlib.dates as mpl_dates
  import requests
  import json

  import matplotlib.pyplot as plt
  import matplotlib as mpl
  from matplotlib import cycler

  """# **Import Data from MT5 csv**

  To Do:
  - Get real time data instead of using CSV
  -Multi TF data handling


  ---

  # **Get feed data from TradingView**

  ---
  """


  import time

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
  print(interval_result)

  # for i in range(10000000):
  #   index_data = tv.get_hist(symbol='XAUUSD',exchange='OANDA',interval=Interval.in_5_minute,n_bars=1000000)
  #   print(index_data)
  #   time.sleep(60)

  index_data = tv.get_hist(symbol=ticker,exchange=exchange,interval=interval_result,n_bars=250)
  print("Finished download index_data")

  index_data

  #Data Handling for TV datafeed
  #Rename of data
  index_data.columns = ["Symbol","Open","High","Low","Close","Vol"]
  #move the index to a new column
  index_data.reset_index(level=0, inplace=True)
  df = index_data.rename(columns = {'index':'date'})
  df

  #Convert date to numdate
  df["Date"] = df["datetime"].apply(mpl_dates.date2num)

  #Create another date column which can read easier
  #df["DateandTime_ref"]=df["Date"]

  """# Ploting graph using mpfinance"""
  def plotting_graph(df,stop_loss):
    #Index must be date for plotting graph.
    lookback=90
    df_plot=df.tail(lookback)
    mco=df_plot["mpfColour"].tail(lookback).values
    df_plot.set_index('datetime', inplace=True)

    df_plot["mpfColour"]

    
    slvalue=stop_loss
    #slvalue

    mpf.plot(df_plot.tail(lookback),type="candle",marketcolor_overrides=mco,hlines=dict(hlines=[slvalue],colors=['r'],linestyle='-'),axtitle=f"{ticker}_{interval}",savefig='testsave.png')

  # Sending message to Telegram

  def send_results_to_tg(message,file_opened):
    import requests
    TOKEN = "6860467333:AAGx0NYGb9pb0NreLZIO3QBtUiarryzkovs"
    chat_id_str=["5718258536","2141426477","6690759056","687649922"]#["5718258536"]

    def send_message(message):
      # url = f"https://api.telegram.org/bot{TOKEN}/getUpdates"
      # print(requests.get(url).json())
      message = message
      url = f"https://api.telegram.org/bot{TOKEN}/sendMessage?chat_id={chat_id}&text={message}"
      print(requests.get(url).json()) # this sends the message

    def send_photo(chat_id, file_opened):
        
        method = "sendPhoto"
        params = {'chat_id': chat_id}
        files = {'photo': file_opened}
        resp = requests.post(f"https://api.telegram.org/bot{TOKEN}/"+ method, params, files=files)
        return resp

    for chat_id in chat_id_str:
      send_message(message)
      send_photo(chat_id, file_opened)

  # Imbalance overtaken signal creation

  # Find the imbalance overtake.
  # - To Do:
  # - Bullish / Bearlish Imb (Found)
  # - Strong(Valid) (Detected)
  # - Direction depends on Q+V imbalance overtaken
  # - Entry point (Confirmation, 0.5, 0.75)
  # - SL (Pivot)
  # - TP 1:2 50% remaining hold to reversal Q+V




  import pandas as pd

  def detect_imb_overtaken_signal(df):
      df['Bullish_Imbalance'] = False  # Initialize the new column
      df['Bearish_Imbalance'] = False  # Initialize the new column
      df["Bullish_imb_high"]= False
      df["Bullish_imb_low"]= False
      df["Bearish_imb_high"]= False
      df["Bearish_imb_low"]= False
      df['Duplicated_valid_bull_confirm']=False
      df["Strong_Bullish_overtaken_bearish_imb_signal"] = False
      df["Strong_Bearish_overtaken_bullish_imb_signal"] = False
      df["last_bear_imb"] = np.nan
      df["last_bull_imb"] = np.nan
      df["mpfColour"] = [None]*len(df)
      df["mpfColour_prev"] = [None]*len(df)

      # write a def to check recent PIVOT points - For S/L and Fib calculation
      def findPivotLow(i):
        spread = 0
        last_bear=df.at[i,"last_bear_imb"]
        PivotLow=df.loc[last_bear:i,"Low"].min()
        return PivotLow+spread
      def findPivotHigh(i):
        spread = 0
        last_bull=df.at[i,"last_bull_imb"]
        PivotHigh=df.loc[last_bull:i,"High"].max()
        return PivotHigh+spread

      # Step 1: Find Strong & Normal Bullish Imbalance
      for i in range(2, len(df) - 1):
          if df['Low'].iloc[i] > df['High'].iloc[i - 2]:
              df.at[i-1, 'Bullish_Imbalance'] = True
              df.at[i-1, 'Bullish_imb_high'] = df['Low'].iloc[i]
              df.at[i-1, 'Bullish_imb_low'] = df['High'].iloc[i - 2]
              bear_imb_i=df.loc[:i,"Bearish_Imbalance"][df["Bearish_Imbalance"]].index # The later one [df["Bearish_Imbalance"]] is using as True.
              if len(bear_imb_i)>0:
                last_bear_imb_i=bear_imb_i[-1]
                df.at[i,"last_bear_imb"] = last_bear_imb_i # index of prev. Be-Imb 4991
                # To check if it is a strong Bull-Imb. (i.e. Imb High >　prev. Bear Imb High.)
                if df.at[i-1,'Bullish_imb_high'] > df.at[last_bear_imb_i,"Bearish_imb_high"]:
                  df.at[i,"Strong_bullish_imb_confirm"] = True
                  check_bu_df=df[(df["Strong_bullish_imb_confirm"] == True) & (df["last_bear_imb"] == last_bear_imb_i)]
                  if check_bu_df.shape[0] == 1:
                    df.at[i,"Strong_Bullish_overtaken_bearish_imb_signal"] = True
                    df.at[i-1,"mpfColour"] = "green"
                    df.at[last_bear_imb_i,"mpfColour"] = "red"
                    sl=findPivotLow(i)
                    df.at[i,"Signal_S/L"] = sl
                    


          # Step 2: Find Strong & Normal Bearish Imbalance
          if df['High'].iloc[i] < df['Low'].iloc[i - 2]:
              df.at[i-1, 'Bearish_Imbalance'] = True
              df.at[i-1, 'Bearish_imb_high'] = df['Low'].iloc[i - 2]
              df.at[i-1, 'Bearish_imb_low'] = df['High'].iloc[i]
              bull_imb_i=df.loc[:i,"Bullish_Imbalance"][df["Bullish_Imbalance"]].index # The later one [df["Bullish_Imbalance"]] is using as True.
              if len(bull_imb_i)>0:
                last_bull_imb_i=bull_imb_i[-1]
                df.at[i,"last_bull_imb"] = last_bull_imb_i # index of prev. Bu-Imb 4991
                # To check if it is a strong Bear-Imb. (i.e. Imb Low <　prev. Bull Imb Low.)
                if df.at[i-1,'Bearish_imb_low'] < df.at[last_bull_imb_i,"Bullish_imb_low"]:
                  df.at[i,"Strong_bearish_imb_confirm"] = True
                  check_be_df=df[(df["Strong_bearish_imb_confirm"] == True) & (df["last_bull_imb"] == last_bull_imb_i)]
                  if check_be_df.shape[0] == 1:
                    df.at[i,"Strong_Bearish_overtaken_bullish_imb_signal"] = True
                    df.at[i-1,"mpfColour"] = "red"
                    df.at[last_bull_imb_i,"mpfColour"] = "green"
                    sl=findPivotHigh(i)
                    df.at[i,"Signal_S/L"] = sl
                    
      # print(df.tail(50))
        #3 plot graph send message
      # print(df.tail(20)["Strong_Bullish_overtaken_bearish_imb_signal"])
      # print(df.tail(20)["Strong_Bearish_overtaken_bullish_imb_signal"])
      # print(df["Strong_Bullish_overtaken_bearish_imb_signal"].iloc[-i])
      # print("BBBBB",df.tail(1)["Strong_Bearish_overtaken_bullish_imb_signal"])
      
      # for i in range (1,100):  #for de-bug
      #   print(f"SL{i}",df["Signal_S/L"].iloc[-i])
      #   if df["Strong_Bullish_overtaken_bearish_imb_signal"].iloc[-i] == True:
      #     print("Trying",i)
      #     sl=df["Signal_S/L"].iloc[-i]
      #     plotting_graph(df,sl)
      #     send_results_to_tg("Bullish Imb confirmed",open("testsave.png", 'rb'))
        # if df["Strong_Bearish_overtaken_bullish_imb_signal"].iloc[-i] == True: 
        #   sl=df["Signal_S/L"].iloc[-i]
        #   plotting_graph(df,sl)
        #   send_results_to_tg("Bearish Imb confirmed",open("testsave.png", 'rb')) 

      #==============================Mock Data to test the texting system========================================================

      # sl=df["Signal_S/L"].iloc[-5]
      # message_buy=f"BUY SIGNAL->PREV. BEAR IMB OVERTAKEN\nTicker:{ticker}\nTimeframe:{timeframe}\nS/L={sl}\nPlease check the trend direction with Q and V to decide to take or not!!"
      # message_sell=f"SELL SIGNAL->PREV. BULL IMB OVERTAKEN\nTicker:{ticker}\nTimeframe:{timeframe}\nS/L={sl}\nPlease check the trend direction with Q and V to decide to take or not!!"  
      print(df[['datetime',"Close","Signal_S/L","Strong_Bullish_overtaken_bearish_imb_signal","Strong_Bearish_overtaken_bullish_imb_signal"]].iloc[-2])
      # print(df["Strong_Bearish_overtaken_bullish_imb_signal"].iloc[-10:])
      # print(df["Signal_S/L"].iloc[-10:])
      # if df["Strong_Bullish_overtaken_bearish_imb_signal"].iloc[-6] == True:
      #   plotting_graph(df,sl)
      #   send_results_to_tg(message_buy,open("testsave.png", 'rb'))
      # if df["Strong_Bearish_overtaken_bullish_imb_signal"].iloc[-5] == True: 
      #   plotting_graph(df,sl)
      #   send_results_to_tg(message_sell,open("testsave.png", 'rb')) 

      #======================Calculation on S/L=================================
      import decimal
      sl=df["Signal_S/L"].iloc[-2]
      entry=df["Close"].iloc[-2]
      rrr=round(entry-sl,5)
      rrr2=rrr*2
      rrr3=rrr*3
      buy_ratio=f"TP ref: 1R:{entry+rrr},2R:{entry+rrr2},3R{entry+rrr3}"
      sell_ratio=f"TP Ref: 1R:{entry+rrr},2R:{entry+rrr3},3R{entry+rrr3}"

      message_buy=f"BUY SIGNAL->PREV. BEAR IMB OVERTAKEN\nTicker:{ticker}\nTimeframe:{timeframe}\nS/L={sl}\n{buy_ratio}\nPlease check the trend direction with Q and V to decide to take or not!!"
      message_sell=f"SELL SIGNAL->PREV. BULL IMB OVERTAKEN\nTicker:{ticker}\nTimeframe:{timeframe}\nS/L={sl}\n\{sell_ratio}\nPlease check the trend direction with Q and V to decide to take or not!!"  
      #======================Results Action =====================================
      if df["Strong_Bullish_overtaken_bearish_imb_signal"].iloc[-2] == True:
        sl=sl=df["Signal_S/L"].iloc[-2]
        plotting_graph(df,sl)
        send_results_to_tg(message_buy,open("testsave.png", 'rb'))
      if df["Strong_Bearish_overtaken_bullish_imb_signal"].iloc[-2] == True: 
        sl=sl=df["Signal_S/L"].iloc[-2]
        plotting_graph(df,sl)
        send_results_to_tg(message_sell,open("testsave.png", 'rb')) 
      print("finished results check")  
  
  
  
  
  
  
  detect_imb_overtaken_signal(df)

  # df.tail(50)

  # df[df["Strong_Bearish_overtaken_bullish_imb_signal"]==True][["datetime","Strong_Bearish_overtaken_bullish_imb_signal","Signal_S/L"]]




  
  


  
import time
while True:
  ticker_list=["HK33HKD","GBPJPY","EURUSD","USDJPY","AUDUSD","XAUUSD"]
  tf_list=["1"]#["1","5","15","1H","4H"]
  for m in tf_list:
    for t in ticker_list: 
      imb_overtake_trading_signal(t,"OANDA",m) 
  time.sleep(60)
    
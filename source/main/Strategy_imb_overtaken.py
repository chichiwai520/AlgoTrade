import numpy as np
import mplfinance as mpf
from Data_fetch_from_TradingView import fetch_from_Tv
from telegram_post import send_results_to_tg



def detect_imb_overtaken_signal(ticker,exchange,timeframe):
    df=fetch_from_Tv(ticker,exchange,timeframe)
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

    #Plotting graphs def
    def plotting_graph(df,stop_loss):
        #Index must be date for plotting graph.
        lookback=90
        df_plot=df.tail(lookback)
        mco=df_plot["mpfColour"].tail(lookback).values
        df_plot.set_index('datetime', inplace=True)

        df_plot["mpfColour"]


        slvalue=stop_loss
        #slvalue

        mpf.plot(df_plot.tail(lookback),type="candle",marketcolor_overrides=mco,hlines=dict(hlines=[slvalue],colors=['r'],linestyle='-'),axtitle=f"{ticker}_{timeframe}",savefig='testsave.png')
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

    
    for i in range(2, len(df) - 1):##Strategy main
        # Step 1: Find Strong & Normal Bullish Imbalance
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

    #Step 3. Calculation on S/L=================================
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




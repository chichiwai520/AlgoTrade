from imbalance_overtaken_signal import imb_overtake_trading_signal

ticker_list=["HK33HKD","GBPJPY","EURUSD","USDJPY","AUDUSD","XAUUSD"]
m="15"

def run_script(m,ticker_list):  
    
    for t in ticker_list: 
        imb_overtake_trading_signal(t,"OANDA","15")
    
    

run_script(m,ticker_list)

from imbalance_overtaken_signal import imb_overtake_trading_signal

ticker_list=["HK33HKD","GBPJPY","EURUSD","USDJPY","AUDUSD","XAUUSD"]
m="4H"

def run_script(m,ticker_list):  
    
    for t in ticker_list: 
        imb_overtake_trading_signal(t,"OANDA","4H")
    
    

run_script(m,ticker_list)

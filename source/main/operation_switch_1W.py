

from Strategy_imb_overtaken import detect_imb_overtaken_signal


ticker_list=["HK33HKD","GBPJPY","EURUSD","USDJPY","AUDUSD","XAUUSD"]
m="1W"

def run_script(m,ticker_list):  
    
    for t in ticker_list: 
        detect_imb_overtaken_signal(t,"OANDA","1W")
    
    

run_script(m,ticker_list)

from Strategy_imb_overtaken import detect_imb_overtaken_signal


ticker_list=["HK33HKD","GBPJPY","EURUSD","USDJPY","AUDUSD","XAUUSD"]
m="15"

def run_script(m,ticker_list):  
    
    for t in ticker_list: 
        detect_imb_overtaken_signal(t,"OANDA","15")
    
    

run_script(m,ticker_list)

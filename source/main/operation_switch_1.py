import time
from Strategy_imb_overtaken import detect_imb_overtaken_signal
ticker_list=["HK33HKD","GBPJPY","EURUSD","USDJPY","AUDUSD","XAUUSD"]
m="1"

def run_script(m,ticker_list):  
    
    for t in ticker_list: 
        detect_imb_overtaken_signal(t,"OANDA","1")
    
    
for _ in range(5):
    run_script(m,ticker_list)
    time.sleep(60)

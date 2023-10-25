from marketpanda import MarketPanda

if __name__ == "__main__":
    db_path = "/Users/fayssalelmofatiche/dev/dnbf/data/marketvault.db"
    mp = MarketPanda(db_path=db_path)
    print(mp.symbols)
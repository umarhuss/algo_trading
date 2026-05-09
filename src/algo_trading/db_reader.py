import sqlite3
import os

def get_prices(instrument_id):
    base_dir = os.path.dirname(os.path.abspath(__file__))
    db_path = os.path.join(base_dir, "../../dotnet/FxDataIngestor/Fx_data.db")
    conn = sqlite3.connect(db_path)
    cursor = conn.cursor()
    cursor.execute("SELECT Close FROM Prices WHERE InstrumentId = ? ORDER BY BarTime", (instrument_id,))
    rows = cursor.fetchall()
    conn.close()

    prices = [price[0] for price in rows]
    prices = [float(row[0]) for row in rows]
    return prices

prices = get_prices(1)

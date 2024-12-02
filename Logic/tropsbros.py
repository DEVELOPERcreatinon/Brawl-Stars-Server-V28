from database.DataBase import DataBase
from Logic.Player import Player
import sqlite3 as sql
from Logic.Player import Player
import json
import time
import threading

class TrophyDecrementer:
    def __init__(self, db_path):
        self.db_path = db_path

    def trophy_decrement(self):
        while True:
            conn = sql.connect(self.db_path)
            cur = conn.cursor()

            cur.execute("SELECT lowID, brawlerData, starpoints FROM plrs")
            players_data = cur.fetchall()

            for player in players_data:
                low_id = player[0]
                brawlerData = json.loads(player[1])
                current_starpoints = player[2]
                updated = False

                # Accessing the trophies in the JSON structure
                for brawler_id, trophies in brawlerData.get("brawlers_trophies", {}).items():
                    if trophies > 500:
                        decrement = int(trophies * 0.10)
                        new_trophies = max(trophies - decrement, 500)
                        brawlerData["brawlers_trophies"][brawler_id] = new_trophies

                        # Update star points
                        current_starpoints += decrement
                        updated = True

                if updated:
                    cur.execute(
                        "UPDATE plrs SET brawlerData = ?, starpoints = ? WHERE lowID = ?",
                        (json.dumps(brawlerData), current_starpoints, low_id)
                    )

            conn.commit()
            conn.close()
            time.sleep(10)  # Wait for 10 seconds before the next iteration

    def start(self):
        thread = threading.Thread(target=self.trophy_decrement)
        thread.daemon = True
        thread.start()

if __name__ == "__main__":
    db_path = "database/Player/plr.db"
    decrementer = TrophyDecrementer(db_path)
    decrementer.start()

    # Keep the main thread alive
    while True:
        time.sleep(1)

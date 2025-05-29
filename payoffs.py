import psycopg2
import random
from urllib.parse import urlparse

DATABASE_URL = "postgres://u18u3petajkfkh:pa432f0ba9164ab174c4f3f753f85f45c605880d4bfceedca2bec40bd4ea80756@ec2-18-232-21-134.compute-1.amazonaws.com:5432/d8opo5kc40iidt"  # e.g. from env var

def parse_database_url(db_url):
    result = urlparse(db_url)
    return {
        'dbname': result.path[1:],  # skip leading /
        'user': result.username,
        'password': result.password,
        'host': result.hostname,
        'port': result.port
    }

def calculate_payoffs_postgres():
    conn_params = parse_database_url(DATABASE_URL)

    with psycopg2.connect(**conn_params) as conn:
        with conn.cursor() as cur:
            cur.execute("""
                SELECT id, selected_bid1, constant, auction_value, follow_up_quiz_payment, comprehension_quiz_payment
                FROM stage_1_player
                ORDER BY id
            """)
            players = cur.fetchall()
            
            if len(players) % 2 != 0:
                raise ValueError("Number of players must be even to form pairs.")
            
            players = [
                {
                    'id': row[0],
                    'selected_bid1': row[1],
                    'constant': row[2],
                    'auction_value': row[3],
                    'follow_up_quiz_payment': row[4],
                    'comprehension_quiz_payment': row[5],
                    'game_payoff': 0
                }
                for row in players
            ]
            
            random.shuffle(players)
            
            for i in range(0, len(players), 2):
                p1 = players[i]
                p2 = players[i+1]
                
                if p1['selected_bid1'] > p2['selected_bid1']:
                    p1['game_payoff'] = p1['constant'] + (p1['auction_value'] - p2['selected_bid1']) + p1['follow_up_quiz_payment'] + p1['comprehension_quiz_payment']
                    p2['game_payoff'] = p2['constant'] + p2['follow_up_quiz_payment'] + p2['comprehension_quiz_payment']
                elif p1['selected_bid1'] < p2['selected_bid1']:
                    p1['game_payoff'] = p1['constant'] + p1['follow_up_quiz_payment'] + p1['comprehension_quiz_payment']
                    p2['game_payoff'] = p2['constant'] + (p2['auction_value'] - p1['selected_bid1']) + p2['follow_up_quiz_payment'] + p2['comprehension_quiz_payment']
                else:
                    p1['game_payoff'] = p1['constant'] + ((p1['auction_value'] - p2['selected_bid1']) // 2) + p1['follow_up_quiz_payment'] + p1['comprehension_quiz_payment']
                    p2['game_payoff'] = p2['constant'] + ((p2['auction_value'] - p1['selected_bid1']) // 2) + p2['follow_up_quiz_payment'] + p2['comprehension_quiz_payment']
            
            for p in players:
                cur.execute(
                    "UPDATE stage_1_player SET game_payoff = %s WHERE id = %s",
                    (p['game_payoff'], p['id'])
                )
            conn.commit()

    print("Payoffs updated successfully.")

if __name__ == "__main__":
    calculate_payoffs_postgres()

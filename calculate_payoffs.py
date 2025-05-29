import os
import psycopg2
import random
from urllib.parse import urlparse

DATABASE_URL = os.environ.get('DATABASE_URL')
if DATABASE_URL is None:
    raise ValueError("DATABASE_URL environment variable not set.")

def parse_database_url(db_url):
    result = urlparse(db_url)
    return {
        'dbname': result.path[1:],
        'user': result.username,
        'password': result.password,
        'host': result.hostname,
        'port': result.port
    }

def calculate_payoffs_postgres():
    conn_params = parse_database_url(DATABASE_URL)

    with psycopg2.connect(**conn_params) as conn:
        with conn.cursor() as cur:
            # Make sure you include treatment in SELECT
            cur.execute("""
                SELECT id, selected_bid1, constant, auction_value, follow_up_quiz_payment, comprehension_quiz_payment, treatment
                FROM stage_1_player
                ORDER BY id
            """)
            rows = cur.fetchall()
            
            # Group by treatment and prepare players dicts
            from collections import defaultdict
            players_by_treatment = defaultdict(list)
            for row in rows:
                player_dict = {
                    'id': row[0],
                    'selected_bid1': row[1],
                    'constant': row[2],
                    'auction_value': row[3],
                    'follow_up_quiz_payment': row[4],
                    'comprehension_quiz_payment': row[5],
                    'treatment': row[6],
                    'game_payoff': 0
                }
                players_by_treatment[player_dict['treatment']].append(player_dict)
            
            # Pair and calculate payoffs within each treatment group
            for treatment, group in players_by_treatment.items():
                random.seed(treatment) 
                random.shuffle(group)
                if len(group) % 2 != 0:
                    raise ValueError(f"Number of players in treatment '{treatment}' must be even to form pairs.")
                for i in range(0, len(group), 2):
                    p1 = group[i]
                    p2 = group[i+1]
                    # Calculate payoffs here (same as your logic)
                    if p1['selected_bid1'] > p2['selected_bid1']:
                        p1['game_payoff'] = 650 + (p1['auction_value'] - p2['selected_bid1']) + p1['follow_up_quiz_payment'] + p1['comprehension_quiz_payment']
                        p2['game_payoff'] = 650 + p2['follow_up_quiz_payment'] + p2['comprehension_quiz_payment']
                    elif p1['selected_bid1'] < p2['selected_bid1']:
                        p1['game_payoff'] = 650 + p1['follow_up_quiz_payment'] + p1['comprehension_quiz_payment']
                        p2['game_payoff'] = 650 + (p2['auction_value'] - p1['selected_bid1']) + p2['follow_up_quiz_payment'] + p2['comprehension_quiz_payment']
                    else:
                        p1['game_payoff'] = 650 + ((p1['auction_value'] - p2['selected_bid1']) // 2) + p1['follow_up_quiz_payment'] + p1['comprehension_quiz_payment']
                        p2['game_payoff'] = 650 + ((p2['auction_value'] - p1['selected_bid1']) // 2) + p2['follow_up_quiz_payment'] + p2['comprehension_quiz_payment']
            
                    print(f"Pairing Player {p1['id']} (bid: {p1['selected_bid1']}, value: {p1['auction_value']}) "
                        f"with Player {p2['id']} (bid: {p2['selected_bid1']}, value: {p2['auction_value']})")
                    print(f"  -> Player {p1['id']} payoff: {p1['game_payoff']}")
                    print(f"  -> Player {p2['id']} payoff: {p2['game_payoff']}")
                                
            # Flatten the grouped players back to a list for updating DB
            all_players = [p for group in players_by_treatment.values() for p in group]
            
            # Update payoffs in DB
            for p in all_players:
                cur.execute(
                    "UPDATE stage_1_player SET game_payoff = %s WHERE id = %s",
                    (p['game_payoff'], p['id'])
                )
            conn.commit()

if __name__ == "__main__":
    calculate_payoffs_postgres()

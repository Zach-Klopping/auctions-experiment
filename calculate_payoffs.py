import os
import psycopg2
import random
from urllib.parse import urlparse
from collections import defaultdict

# Get the DATABASE_URL environment variable, required for connecting to the database
DATABASE_URL = os.environ.get('DATABASE_URL')
if DATABASE_URL is None:
    raise ValueError("DATABASE_URL environment variable not set.")

def parse_database_url(db_url):
    """ Parse the database URL into components required by psycopg2.connect. Returns a dict with keys: dbname, user, password, host, port. """
    result = urlparse(db_url)
    return {
        'dbname': result.path[1:],   # Remove leading slash
        'user': result.username,
        'password': result.password,
        'host': result.hostname,
        'port': result.port
    }

def calculate_payoffs_postgres():
    # Parse connection parameters from DATABASE_URL
    conn_params = parse_database_url(DATABASE_URL)

    # Connect to PostgreSQL using a context manager to ensure proper cleanup
    with psycopg2.connect(**conn_params) as conn:
        with conn.cursor() as cur:
            # Query all relevant player data, including treatment for grouping
            cur.execute(""" SELECT id, id_in_group, selected_bid, auction_value, follow_up_quiz_payment, comprehension_quiz_payment, treatment FROM stage_1_player ORDER BY id """)
            rows = cur.fetchall()
            
            # Group players by their treatment assignment for paired payoff calculation
            players_by_treatment = defaultdict(list)
            all_players = []
            for row in rows:
                if row[2] is None:
                    continue

                player_dict = {
                    'id': row[0],
                    'id_in_group': row[1],
                    'selected_bid': row[2],
                    'auction_value': row[3],
                    'follow_up_quiz_payment': row[4],
                    'comprehension_quiz_payment': row[5],
                    'treatment': row[6],
                    'payoff_from_auction' : 0, # Initialize payoff
                    'game_payoff': 0  # Initialize payoff
                }
                players_by_treatment[player_dict['treatment']].append(player_dict)
                all_players.append(player_dict)

            # For each treatment, calculate payoffs for all players
            for treatment, group in players_by_treatment.items():
                random.seed(treatment)  # Seed for reproducibility per treatment

                # Build auction_value index for players in this treatment only
                players_by_auction_value = defaultdict(list)
                for p in group:
                    players_by_auction_value[p['auction_value']].append(p)

                fixed_auction_values = list(players_by_auction_value.keys())

                for p1 in group:
                    valid_values = [val for val in fixed_auction_values if any(p['id'] != p1['id'] for p in players_by_auction_value[val])]
                    matched_value = random.choice(valid_values)
                    partner_candidates = [p for p in players_by_auction_value[matched_value] if p['id'] != p1['id']]
                    p2 = random.choice(partner_candidates)

                    # Calculate payoff for p1 compared to p2
                    if p1['selected_bid'] > p2['selected_bid']:
                        auction_p1 = p1['auction_value'] - p2['selected_bid']
                    elif p1['selected_bid'] < p2['selected_bid']:
                        auction_p1 = 0
                    else:
                        auction_p1 = (p1['auction_value'] - p2['selected_bid']) // 2

                    p1['payoff_from_auction'] = auction_p1

                    full_p1 = 450 + auction_p1 + p1['follow_up_quiz_payment'] + p1['comprehension_quiz_payment']
                    p1['game_payoff'] = round(full_p1 / 100, 2)

                    print(f" -> Matched value: {matched_value}")
                    print(f"Player {p1['id_in_group']} (bid: {p1['selected_bid']}, auction_value: {p1['auction_value']}) "
                          f"matched with Player {p2['id_in_group']} (bid: {p2['selected_bid']}, auction_value: {p2['auction_value']})")
                    print(f" -> P1 payoff_from auction: {p1['payoff_from_auction']} | game_payoff: ${p1['game_payoff']:.2f}")
            
           # Update each player's payoff in the database
            for p in all_players:
                cur.execute(
                    """
                    UPDATE stage_1_player 
                    SET game_payoff = %s, payoff_from_auction = %s 
                    WHERE id = %s
                    """,
                    (p['game_payoff'], p['payoff_from_auction'], p['id'])
                )
            # Commit all updates
            conn.commit()

if __name__ == "__main__":
    calculate_payoffs_postgres()

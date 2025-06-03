import os
import psycopg2
import random
from urllib.parse import urlparse

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
            cur.execute(""" SELECT id, selected_bid, auction_value, follow_up_quiz_payment, comprehension_quiz_payment, treatment FROM stage_1_player ORDER BY id """)
            rows = cur.fetchall()
            
            from collections import defaultdict
            # Group players by their treatment assignment for paired payoff calculation
            players_by_treatment = defaultdict(list)
            for row in rows:
                player_dict = {
                    'id': row[0],
                    'selected_bid': row[1],
                    'auction_value': row[2],
                    'follow_up_quiz_payment': row[3],
                    'comprehension_quiz_payment': row[4],
                    'treatment': row[5],
                    'game_payoff': 0  # Initialize payoff
                }
                players_by_treatment[player_dict['treatment']].append(player_dict)
            
            # For each treatment group, shuffle players deterministically, then pair and calculate payoffs
            for treatment, group in players_by_treatment.items():
                group = [p for p in group if p['selected_bid'] is not None]
                random.seed(treatment)  # Seed by treatment for reproducible shuffling
                random.shuffle(group)
                
                n = len(group)
                last_player = None
                if n % 2 != 0:
                    last_player = group.pop()  
                
                # Process players in pairs (2 at a time)
                for i in range(0, len(group), 2):
                    p1 = group[i]
                    p2 = group[i+1]
                    
                    # Calculate payoffs based on bid comparisons and quiz payments
                    if p1['selected_bid'] > p2['selected_bid']:
                        raw_payoff_p1 = 650 + (p1['auction_value'] - p2['selected_bid']) + p1['follow_up_quiz_payment'] + p1['comprehension_quiz_payment']
                        raw_payoff_p2 = 650 + p2['follow_up_quiz_payment'] + p2['comprehension_quiz_payment']
                    elif p1['selected_bid'] < p2['selected_bid']:
                        raw_payoff_p1 = 650 + p1['follow_up_quiz_payment'] + p1['comprehension_quiz_payment']
                        raw_payoff_p2 = 650 + (p2['auction_value'] - p1['selected_bid']) + p2['follow_up_quiz_payment'] + p2['comprehension_quiz_payment']
                    else:  # bids equal, split difference
                        raw_payoff_p1 = 650 + ((p1['auction_value'] - p2['selected_bid']) // 2) + p1['follow_up_quiz_payment'] + p1['comprehension_quiz_payment']
                        raw_payoff_p2 = 650 + ((p2['auction_value'] - p1['selected_bid']) // 2) + p2['follow_up_quiz_payment'] + p2['comprehension_quiz_payment']
            
                    # Convert from cents to dollars and subtract fixed cost of 2.00 dollars
                    p1['game_payoff'] = (raw_payoff_p1 / 100) - 2.00
                    p2['game_payoff'] = (raw_payoff_p2 / 100) - 2.00

                    # Print result info for each pair
                    print(f"Pairing Player {p1['id']} (bid: {p1['selected_bid']}, value: {p1['auction_value']}) with Player {p2['id']} (bid: {p2['selected_bid']}, value: {p2['auction_value']})")
                    print(f" -> Player {p1['id']} payoff: ${p1['game_payoff']:.2f}")
                    print(f" -> Player {p2['id']} payoff: ${p2['game_payoff']:.2f}")

                # Code if there is an odd number
                if last_player:
                    partner = random.choice(group)
                    
                    p1 = last_player
                    p2 = partner
                    
                    if p1['selected_bid'] > p2['selected_bid']:
                        raw_payoff_p1 = 650 + (p1['auction_value'] - p2['selected_bid']) + p1['follow_up_quiz_payment'] + p1['comprehension_quiz_payment']
                    elif p1['selected_bid'] < p2['selected_bid']:
                        raw_payoff_p1 = 650 + p1['follow_up_quiz_payment'] + p1['comprehension_quiz_payment']
                    else:  # bids equal, split difference
                        raw_payoff_p1 = 650 + ((p1['auction_value'] - p2['selected_bid']) // 2) + p1['follow_up_quiz_payment'] + p1['comprehension_quiz_payment']

                    p1['game_payoff'] = (raw_payoff_p1 / 100) - 2.00

                    print(f"Leftover Player {p1['id']} paired randomly with Player {p2['id']} (bid: {p2['selected_bid']}, value: {p2['auction_value']})")
                    print(f" -> Player {p1['id']} payoff: ${p1['game_payoff']:.2f}")
                                
            # Flatten all players back into a single list for database update
            all_players = [p for group in players_by_treatment.values() for p in group]
            if last_player:
                all_players.append(last_player)
            
            # Update each player's payoff in the database
            for p in all_players:
                cur.execute(
                    "UPDATE stage_1_player SET game_payoff = %s WHERE id = %s",
                    (p['game_payoff'], p['id'])
                )
            # Commit all updates
            conn.commit()

if __name__ == "__main__":
    calculate_payoffs_postgres()

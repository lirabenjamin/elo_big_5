from flask import Flask, render_template, request, jsonify
import random
import numpy as np

app = Flask(__name__)

# Define the Big Five dimensions and their items
big_five_items = {
    "Extraversion": [1, 11, 16, 26, 36],
    "Agreeableness": [2, 7, 17, 22, 32, 42],
    "Conscientiousness": [3, 13, 28, 33, 38],
    "Neuroticism": [4, 14, 19, 29, 39],
    "Openness": [5, 10, 15, 20, 25, 30, 40, 44]
}

# Define item descriptions
item_descriptions = {
    1: "Is talkative",
    2: "Tends to find fault with others",
    3: "Does a thorough job",
    4: "Is depressed, blue",
    5: "Is original, comes up with new ideas",
    7: "Is helpful and unselfish with others",
    10: "Is curious about many different things",
    11: "Is full of energy",
    13: "Is a reliable worker",
    14: "Can be tense",
    15: "Is ingenious, a deep thinker",
    16: "Generates a lot of enthusiasm",
    17: "Has a forgiving nature",
    19: "Worries a lot",
    20: "Has an active imagination",
    22: "Is generally trusting",
    25: "Is inventive",
    26: "Has an assertive personality",
    28: "Perseveres until the task is finished",
    29: "Can be moody",
    30: "Values artistic, aesthetic experiences",
    32: "Is considerate and kind to almost everyone",
    33: "Does things efficiently",
    36: "Is outgoing, sociable",
    38: "Makes plans and follows through with them",
    39: "Gets nervous easily",
    40: "Likes to reflect, play with ideas",
    42: "Likes to cooperate with others",
    44: "Is sophisticated in art, music, or literature"
}

# Initialize Elo ratings
elo_ratings = {item: 1000 for item in item_descriptions.keys()}
big_five_elo = {dimension: 1000 for dimension in big_five_items}

def expected_score(rating_a, rating_b):
    return 1 / (1 + 10 ** ((rating_b - rating_a) / 400))

def update_elo(winner, loser, k=32):
    expected_win = expected_score(elo_ratings[winner], elo_ratings[loser])
    expected_lose = expected_score(elo_ratings[loser], elo_ratings[winner])
    
    print(f"Before update: {winner}={elo_ratings[winner]}, {loser}={elo_ratings[loser]}")
    
    elo_ratings[winner] += k * (1 - expected_win)
    elo_ratings[loser] -= k * (0 - expected_lose)
    
    print(f"After update: {winner}={elo_ratings[winner]}, {loser}={elo_ratings[loser]}")

def get_dimension(item):
    for dimension, items in big_five_items.items():
        if item in items:
            return dimension
    return None

def update_big_five_elo():
    for dimension, items in big_five_items.items():
        ratings = [elo_ratings[item] for item in items]
        big_five_elo[dimension] = np.mean(ratings)

@app.route('/')
def index():
    return render_template('index.html', items=item_descriptions)

@app.route('/compare', methods=['POST'])
def compare():
    data = request.json
    item_a = int(data['item_a'])
    item_b = int(data['item_b'])
    choice = data['choice']
    
    print(f"Received comparison: item_a={item_a}, item_b={item_b}, choice={choice}")
    
    if choice == '1':
        update_elo(item_a, item_b)
    elif choice == '2':
        update_elo(item_b, item_a)
    
    update_big_five_elo()
    
    print("Updated Elo Ratings:", elo_ratings)
    print("Updated Big Five Elo:", big_five_elo)
    
    return jsonify({
        'elo_ratings': elo_ratings,
        'big_five_elo': big_five_elo
    })

if __name__ == '__main__':
    app.run(debug=True)

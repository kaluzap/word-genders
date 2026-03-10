import os
import json
import base64
from io import BytesIO
from pathlib import Path

import matplotlib
matplotlib.use('Agg') # MUST be before import pyplot in util/util

from flask import Flask, request, jsonify, send_file, render_template
from flask_cors import CORS
import pandas as pd
from numpy import random
from gtts import gTTS

# Import existing classes
from util.dictionary import Dictionary
from configuration.configuration import Configuration, DATA_PATH
from util.util import SuccessStreak, play_string

app = Flask(__name__)
CORS(app)

# Global state for the single-user web version
class AppState:
    def __init__(self):
        self.dictionary = Dictionary()
        self.configuration = Configuration()
        self.success_streak = SuccessStreak()
        self.current_word = None
        self.current_case = None
        self.current_options = [] # For meanings mode
        self.already_tested = False
        self.count_good = 0
        self.count_total_clicks = 0
        self.count_total_words = 0
        self.allow_repetitions = True

state = AppState()

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/api/config')
def get_config():
    lang = request.args.get('lang', state.configuration.language)
    state.configuration.load_configuration(lang)
    return jsonify({
        'language': state.configuration.language,
        'sys_dict': state.configuration.sys_dict,
        'kind': state.dictionary.kind
    })

@app.route('/api/dictionaries')
def get_dictionaries():
    files = list(DATA_PATH.glob('*.csv'))
    return jsonify([f.name for f in files])

@app.route('/api/load_dictionary', methods=['POST'])
def load_dictionary():
    data = request.json
    dict_name = data.get('name')
    if not dict_name:
        return jsonify({'error': 'No dictionary name provided'}), 400
    
    dict_path = DATA_PATH / dict_name
    state.dictionary.load_dictionary(str(dict_path))
    return jsonify({
        'name': state.dictionary.name,
        'kind': state.dictionary.kind,
        'language': state.dictionary.language,
        'translation': state.dictionary.translation,
        'count': len(state.dictionary.data)
    })

def random_case():
    return "s" if random.rand() < 0.75 else "p"

@app.route('/api/next_word', methods=['GET'])
def next_word():
    if state.dictionary.data.empty:
        return jsonify({'error': 'No dictionary loaded'}), 400

    try:
        if state.allow_repetitions:
            indexes = [x for x in range(0, state.dictionary.data.shape[0])]
            total = state.dictionary.data["mistakes"].sum()
            if total == 0:
                state.dictionary.data["p"] = 1 / len(indexes)
            else:
                state.dictionary.data["p"] = state.dictionary.data["mistakes"] / total
            
            the_index = random.choice(indexes, 1, p=state.dictionary.data["p"].to_list())[0]
            df_sample = state.dictionary.data.iloc[[the_index]]
        else:
            active_df = state.dictionary.data[state.dictionary.data["active"]]
            if active_df.empty:
                return jsonify({'error': 'No more active words'}), 404
            df_sample = active_df.sample()

        state.current_word = df_sample.iloc[0].to_dict()
        state.current_word["index"] = int(df_sample.index[0])
        state.dictionary.data.at[state.current_word["index"], "active"] = False
        state.already_tested = False

        # Determine case
        state.current_case = random_case()
        if (state.current_word.get("plural") == "-") and (state.current_case == "p"):
            state.current_case = "s"
        if state.current_word.get("singular") == state.current_word.get("plural"):
            state.current_case = "sp"
        if state.current_word.get("singular") == "-":
            state.current_case = "p"

        # Text to show
        word_text = state.current_word["singular"] if state.current_case in ["s", "sp"] else state.current_word["plural"]

        return jsonify({
            'word': word_text,
            'translation': state.current_word['translation'],
            'case': state.current_case,
            'statistics': get_stats_dict()
        })

    except Exception as e:
        return jsonify({'error': str(e)}), 500

@app.route('/api/next_meaning', methods=['GET'])
def next_meaning():
    if state.dictionary.data.empty:
        return jsonify({'error': 'No dictionary loaded'}), 400

    try:
        # Pick target word
        if state.allow_repetitions:
            indexes = [x for x in range(0, state.dictionary.data.shape[0])]
            total = state.dictionary.data["mistakes"].sum()
            if total == 0:
                state.dictionary.data["p"] = 1 / len(indexes)
            else:
                state.dictionary.data["p"] = state.dictionary.data["mistakes"] / total
            
            the_index = random.choice(indexes, 1, p=state.dictionary.data["p"].to_list())[0]
            df_target = state.dictionary.data.iloc[[the_index]].copy()
        else:
            active_df = state.dictionary.data[state.dictionary.data["active"]]
            if active_df.empty:
                return jsonify({'error': 'No more active words'}), 404
            df_target = active_df.sample().copy()

        # Distractors
        df_distractors = state.dictionary.data[state.dictionary.data.index != df_target.index[0]].sample(3).copy()
        
        # Combine and shuffle
        df_options = pd.concat([df_target, df_distractors]).sample(frac=1)
        state.current_options = df_options['translation'].to_list()
        
        state.current_word = df_target.iloc[0].to_dict()
        state.current_word["index"] = int(df_target.index[0])
        state.dictionary.data.at[state.current_word["index"], "active"] = False
        state.already_tested = False

        # Determine display word
        kind = state.dictionary.kind
        display_word = ""
        if kind == "nouns":
            display_word = state.current_word["singular"] if state.current_word["singular"] != "-" else state.current_word["plural"]
        elif kind == "verbs":
            display_word = state.current_word["infinitive"]
        elif kind == "adjectives":
            display_word = state.current_word["adjective"]
        elif kind == "adverbs":
            display_word = state.current_word["adverb"]
        else:
            display_word = state.current_word.get("word", "???")

        return jsonify({
            'word': display_word,
            'options': state.current_options,
            'statistics': get_stats_dict()
        })

    except Exception as e:
        return jsonify({'error': str(e)}), 500

def generate_full_text(word_data, sys_dict, kind):
    text = ""
    if kind == "nouns":
        singular = word_data.get("singular", "-")
        if singular == "-":
            text += f"{sys_dict['missing_gender']['without_singular']}, "
        else:
            gender = word_data.get("gender", "")
            if "m" in gender: text += sys_dict["article_texts"]["m"] + " "
            if "f" in gender: text += sys_dict["article_texts"]["f"] + " "
            if "n" in gender: text += sys_dict["article_texts"]["n"] + " "
            text += singular + ", "

        plural = word_data.get("plural", "-")
        if plural == "-":
            text += f"{sys_dict['missing_gender']['without_plural']}"
        else:
            text += f"{sys_dict['article_texts']['p']} {plural}"
    elif kind == "verbs":
        parts = [word_data.get(x) for x in ["infinitive", "participle_II"] if word_data.get(x) and word_data.get(x) != "-"]
        text = ", ".join(parts)
    elif kind == "adjectives":
        parts = [word_data.get(x) for x in ["adjective", "comparative", "superlative"] if word_data.get(x) and word_data.get(x) != "-"]
        text = ", ".join(parts)
    elif kind == "adverbs":
        text = word_data.get("adverb", "")
    else:
        text = word_data.get("word", word_data.get("singular", ""))
    return text

@app.route('/api/test_meaning', methods=['POST'])
def test_meaning():
    data = request.json
    guess = data.get('guess') # The translation string
    
    if not state.current_word:
        return jsonify({'error': 'No active word'}), 400

    state.count_total_clicks += 1
    correct = (guess == state.current_word['translation'])
    
    if correct:
        state.success_streak.add_new_sucess()
        if not state.already_tested:
            state.count_good += 1
            idx = state.current_word["index"]
            state.dictionary.data.at[idx, "mistakes"] = max(1, state.dictionary.data.at[idx, "mistakes"] - 1)
            state.count_total_words += 1
    else:
        state.success_streak.stop_success_streak()
        if not state.already_tested:
            idx = state.current_word["index"]
            state.dictionary.data.at[idx, "mistakes"] += 1
            state.count_total_words += 1

    state.already_tested = True
    
    result = {
        'correct': correct,
        'translation': state.current_word['translation'],
        'gender': state.current_word.get('gender', ''),
        'singular': state.current_word.get('singular', '-'),
        'plural': state.current_word.get('plural', '-'),
        'full_text': generate_full_text(state.current_word, state.configuration.sys_dict, state.dictionary.kind),
        'statistics': get_stats_dict(),
        'is_record': state.success_streak.is_record
    }
    return jsonify(result)

@app.route('/api/test_word', methods=['POST'])
def test_word():
    data = request.json
    guess = data.get('guess')
    
    if not state.current_word:
        return jsonify({'error': 'No active word'}), 400

    state.count_total_clicks += 1
    correct = False
    
    # Logic from NounsFrame.test_word
    if ("s" in state.current_case) and (guess in state.current_word.get("gender", "")):
        correct = True
    elif guess in state.current_case:
        correct = True

    if correct:
        state.success_streak.add_new_sucess()
        if not state.already_tested:
            state.count_good += 1
            idx = state.current_word["index"]
            state.dictionary.data.at[idx, "mistakes"] = max(1, state.dictionary.data.at[idx, "mistakes"] - 1)
            state.count_total_words += 1
    else:
        state.success_streak.stop_success_streak()
        if not state.already_tested:
            idx = state.current_word["index"]
            state.dictionary.data.at[idx, "mistakes"] += 1
            state.count_total_words += 1

    state.already_tested = True
    
    # Prepare result data
    result = {
        'correct': correct,
        'gender': state.current_word.get('gender', ''),
        'singular': state.current_word.get('singular', '-'),
        'plural': state.current_word.get('plural', '-'),
        'full_text': generate_full_text(state.current_word, state.configuration.sys_dict, state.dictionary.kind),
        'statistics': get_stats_dict(),
        'is_record': state.success_streak.is_record
    }
    
    return jsonify(result)

@app.route('/api/streak_image')
def streak_image():
    # Load labels from config
    xlabel = state.configuration.sys_dict.get('figure', {}).get('xlabel', 'Streak')
    ylabel = state.configuration.sys_dict.get('figure', {}).get('ylabel', 'Frequency')
    state.success_streak.make_success_streak_figure(xlabel, ylabel)
    
    img_io = BytesIO()
    state.success_streak.last_success_streak_img.save(img_io, 'PNG')
    img_io.seek(0)
    return send_file(img_io, mimetype='image/png')

def get_stats_dict():
    ratio_success = state.count_good / state.count_total_words if state.count_total_words else 0
    ratio_attempts = state.count_good / state.count_total_clicks if state.count_total_clicks else 0
    return {
        'count_good': state.count_good,
        'count_total_words': state.count_total_words,
        'count_total_clicks': state.count_total_clicks,
        'ratio_success': ratio_success,
        'ratio_attempts': ratio_attempts,
        'success_streak': state.success_streak.success_streak,
        'success_streak_record': state.success_streak.success_streak_record,
        'streak_history': state.success_streak.success_streak_history + ([state.success_streak.success_streak] if state.success_streak.success_streak > 0 else [])
    }

@app.route('/api/speak')
def speak():
    text = request.args.get('text', '')
    lang = request.args.get('lang', state.configuration.language)
    if not text:
        return "No text", 400

    # Filter out "missing gender" strings (e.g., "ohne Plural")
    sys_dict = state.configuration.sys_dict
    if sys_dict and 'missing_gender' in sys_dict:
        for val in sys_dict['missing_gender'].values():
            text = text.replace(val, "")
    
    # Clean up leftover characters like brackets, extra commas, and spaces
    text = text.replace("[]", "").replace(", ,", ",").strip(", ")

    try:
        speech = gTTS(text, lang=lang)
        mp3_fp = BytesIO()
        speech.write_to_fp(mp3_fp)
        mp3_fp.seek(0)
        return send_file(mp3_fp, mimetype='audio/mpeg')
    except Exception as e:
        return str(e), 500

@app.route('/api/save', methods=['POST'])
def save():
    state.dictionary.save_dictionary()
    return jsonify({'status': 'saved'})

@app.route('/api/reset_active', methods=['POST'])
def reset_active():
    state.dictionary.make_all_active()
    return jsonify({'status': 'reset'})

@app.route('/api/reset_stats', methods=['POST'])
def reset_stats():
    state.success_streak = SuccessStreak()
    state.count_good = 0
    state.count_total_clicks = 0
    state.count_total_words = 0
    state.already_tested = False
    state.current_word = None
    return jsonify({'status': 'stats reset'})

@app.route('/api/set_repetitions', methods=['POST'])
def set_repetitions():
    state.allow_repetitions = request.json.get('allow', True)
    return jsonify({'allow_repetitions': state.allow_repetitions})

if __name__ == '__main__':
    # Ensure templates directory exists
    Path("templates").mkdir(exist_ok=True)
    app.run(debug=True, port=5000)

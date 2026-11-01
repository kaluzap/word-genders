# Word Genders

A tool for practicing noun genders and meanings in different languages (currently German and Russian).

## Installation

Clone repository:

```bash
git clone https://github.com/kaluzap/word-genders.git
cd word-genders
```

Create and activate a virtual environment:

```bash
python -m venv venv
source venv/bin/activate  # On Linux/macOS
# or
venv\Scripts\activate     # On Windows
```

Install the requirements:

```bash
pip install -r requirements.txt
```

## Usage

Start the app (Flask):

```bash
python app_web.py
```

Then open your browser at `http://127.0.0.1:5000`. On the **Configuration** screen:
1.  **Training language**: German or Russian.
2.  **Dictionary**: any `data_*.csv` file in the `data/` directory.
3.  **Mode**:
    *   **Genders**: practice the genders of nouns (needs a nouns dictionary).
    *   **Meanings**: pick the right translation out of four.

Your training progress (how often each word was missed) is stored in `data/scores.csv`, which is not tracked by git. Deleting it resets all scores.

Each word appears only once per dictionary, with all its translations in the same row (e.g. `"Gewicht","Gewichte","n","peso, importancia, pesa"`). The same spelling can appear again only with a different plural or gender, such as `der See` (lago) and `die See` (mar). If a dictionary repeats a word, its rows are merged when it is loaded.

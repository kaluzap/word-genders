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

## Desktop Application

Run the desktop application (Tkinter):

```bash
python words.py
```

From the **Configuration** screen, you can:
1.  **Choose training language**: German or Russian.
2.  **Load dictionary**: Choose a `.csv` file from the `data/` directory.
3.  **Tools**:
    *   **Nouns genders**: Practice the genders of nouns.
    *   **Meanings**: Practice word translations.
    *   **Manage words**: Add or remove words from the current dictionary.

### Noun genders in German
![Screenshot](/img/nouns_german.png)

### Noun genders in Russian
![Screenshot](/img/nouns_russian.png)

## Web Application

Run the web version (Flask):

```bash
python app_web.py
```

Then open your browser at `http://127.0.0.1:5000`.



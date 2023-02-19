# Word Genders

## Installation

Clone repository

```
git clone https://github.com/kaluzap/word-genders.git
```

Create virtual enviroment inside the new directory.

```
cd words
```

```
virtualenv venv
```

Activate virtual enviroment:

```
source venv/bin/activate
```

Install the requirements:

```
pip install -r requirements.txt
```

## Noun genders in German
```
python nouns-genders.py
```
![Screenshot](/img/nouns_german.png)

## Noun genders in Russian
```
python nouns-genders.py -l ru -s configuration/sys_dict_ru.cfg -d data/data_nouns_ru_sp.csv
```
![Screenshot](/img/nouns_russian.png)



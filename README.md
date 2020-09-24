# README

All in one solution to help kids learn with advanced drilling solutions for times table, vocab cards, ...

* HTML5 client (jQuery+PWA) /Server (Flask) solution for flashcards 
* Flashcards written in markdown and import/export in json file for easier manual or programmatic edits
* Frequency of question optimised as function of how well answer is remembered (see SRS below). Today SM2+ like, next A/B split testing SM2 vs SM19

## Usage

after going through installation on your_server (either a VPS IP or a C_NAME)

open in a web-browser http://your_server/drillmaster/

start practicing :)

## Installation

```bash
cd /var/www/
mkdir -p DrillMaster
git clone git@github.com:matt-chv/DrillMaster.git
cd DrillMaster
pip install -r requirements.txt
flask db init
flask db migrate -m "users table"
flask db migrate -m "cards table"
flask db upgrade
flask run
mv drillmaster.wsgi ..
```

### Apache settings

```wsgi
WSGIScriptAlias /drillmaster /var/www/DrillMaster/drillmaster.wsgi

<Directory /var/www/DrillMaster/DrillMaster/>
   Order allow,deny
   Allow from all
</Directory>

Alias "/DrillMaster/static/" "/var/www/DrillMaster/DrillMaster/static/"
<Directory /var/www/DrillMaster/DrillMaster/static/>
   Order allow,deny
   Allow from all
</Directory>
```


## Coming (soon?)
* adding support for WebSockets for student / assessor flash card synch
* Algorithm update to SM2
* Flashcards in markdown
* Flashcards rendering with css formatting for code / math / ... ala jupyter notebook
* import/export Anki and Mnemosyne file format for flashcards
* import/export Anki / Mnemosyne learning history

## CREDITS

> Add here open source licenses

### SRS

At a very high level SRS is a computer version of Leitner system which is the theoretical underpinning for paper flash cards and multiple decks.

More specifically memorisation is a function of how often a memory has been recalled (see Hermann Ebbinghaus [here](http://www.deutschestextarchiv.de/book/view/ebbinghaus_gedaechtnis_1885?p=67) or wikipedia's summary [here](https://en.wikipedia.org/wiki/Hermann_Ebbinghaus) )


Thus optimising how often a memory is recalled helps improve how fast new data can be memorised without overloading brain nor agendas.

For algorithmic details, see [Here](http://www.blueraja.com/blog/477/a-better-spaced-repetition-learning-algorithm-sm2) next


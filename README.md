# README

WHY?

Adressing home schooling challenges, leveraging state of the art learning techniques 
(see [wiki article on SRS](https://en.wikipedia.org/wiki/Spaced_repetition)) to increase learning efficiency and reduce mental fatigue.

WHAT ?

1. Paper-less solution (web centric) for skills and knowledge acquisition through drilling 
2. Questions frequency inversely proportional to how well the answer is known
3. Parent/ Tutor screens different from kids/students
4. Taking paper based flash cards concepts to the age of portable screens (smarphone, laptops, ...)
5. Fully under parental control (gettingn read of paywall, ...)

HOW?

A self hosted web solution open source

## Technologies

* Self-hosted solution (public hosting considered but not available)
* HTML5 client (jQuery+[PWA](https://en.wikipedia.org/wiki/Progressive_web_application)) / Server (Apache2+Flask) solution for flashcards 
* Flashcards written in json/markdown and import/export in json file for easier manual or programmatic edits
* Frequency of question optimised as function of how well answer is remembered (see SRS below). Today SM2+ like, next A/B split testing SM2 vs SM19

## Usage

### VPS/C_NAME
after going through installation on your_server (either a VPS IP or a C_NAME)

open in a web-browser http://your_server/drillmaster/

start practicing :)

### Local machine

```
(venv) >set FLASK_ENV=development
(venv) >python my_app.py
 * Serving Flask app "app" (lazy loading)
 * Environment: production
   WARNING: This is a development server. Do not use it in a production deployment.
   Use a production WSGI server instead.
 * Debug mode: on
INFO: * Restarting with stat
WARNING: * Debugger is active!
```

### Installation

#### Install mod_wsgi
see online tutorials

#### Clone flask app 

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

#### Apache settings

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

## Next

Coming (soon?):
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


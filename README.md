# README
* Client (jQuery) /Server (Flask) solution for flashcards 
* Flashcards stored as json file for easier manual or programmatic edits
* algorithm: custom now - [SM2+](http://www.blueraja.com/blog/477/a-better-spaced-repetition-learning-algorithm-sm2) next

## Usage
git clone https://github.com/matt-chv/flashcards.git
cd flashcards
pip install -r requirements.txt
flask db init
flask db migrate -m "users table"
flask db migrate -m "cards table"
flask db upgrade
flask run

## Coming (soon?)
* adding support for WebSockets for student / assessor flash card synch
* Algorithm update to SM2
* Flashcards in markdown
* Flashcards rendering with css formatting for code / math / ... ala jupyter notebook
* import/export Anki and Mnemosyne file format for flashcards
* import/export Anki / Mnemosyne learning history

## CREDITS
The hmtl and js was initially forked from Johennes' flashcards
>git clone https://github.com/Johennes/jquery.flashcards.git

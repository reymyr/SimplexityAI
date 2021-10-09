DIR=venv

if ! -d "$DIR"; then
    pip install virtualenv
    virtualenv -p python venv
    source venv/bin/activate
    pip install -r requirements.txt
    clear
    python main.py --row 6 --col 7 --type bvb --player_choice 0 --thinking_time 2 --bot1 group1-minimax-1.pkl --bot2 group1-minimax-2.pkl
else
    source venv/bin/activate
    cd src
    pip install -r requirements.txt
    clear
    python main.py --row 6 --col 7 --type bvb --player_choice 0 --thinking_time 2 --bot1 group1-minimax-1.pkl --bot2 group1-minimax-2.pkl
fi
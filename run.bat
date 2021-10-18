@REM Old Command
@REM python main.py --row 6 --col 7 --type bvb --player_choice 0 --thinking_time 3 --bot1 group1-minimax-1.pkl --bot2 group1-minimax-2.pkl

@REM With dump
@REM python main.py --is_dump --row 6 --col 7 --type bvb --player_choice 0 --thinking_time 2 --bot1 minimax-1.pkl --bot2 random-1.pkl

@REM No dump
python main.py --row 6 --col 7 --type bvb --player_choice 0 --thinking_time 6 --bot1 minimax-1.pkl --bot2 random-1.pkl

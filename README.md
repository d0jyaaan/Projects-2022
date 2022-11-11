# Chess Engine

## Table of Contents
+ [About](#about)
+ [Usage](#usage)
+ [Disclaimer](#disclaimer)

## About <a name = "about"></a>
<p>
 Chess engine with basic chess AI.<br><br>
 Features: 
 <ul>
    <li>Scoreboard</li>
    <li>Reset board feature</li>
    <li>Real Time PGN</li>
    <li>Import PGN and FEN</li>
    <li>Export PGN and FEN</li>
    <li>Chess AI</li>
 </ul>
 <br>
 Used Alpha beta pruning and Negamax search for the chess AI.
 <br><br>
 
### Future Implementations
 
```
1. Optimized Move Ordering Function 
2. Evaluation function using Neural Networks / Better evaluation function 
3. Player Clock (Rapid, Blitz, Classical) 
```

## Usage <a name = "usage"></a>
Execute the following in terminal.
```
python ChessMain.py
```
Controls for the chess engine.
```
  ___         _           _
 / __|___ _ _| |_ _ _ ___| |___
| (__/ _ \ ' \  _| '_/ _ \ (_-<
 \___\___/_||_\__|_| \___/_/__/

Select Screen
SELECT GAMEMODE : AI and Multiplayer
Q : Load PGN
W : Load FEN

Board
D : Get FEN of current position
E : Get PGN of current position
R : Reset the board
```
## Disclaimers <a name = "disclaimer"></a>
A few things to take note of:
<ol> 
<li>The Chess Ai has a long search time and the moves are sometimes inaccurate due to bad move ordering.</li>
<li>Click and drop is sometimes clunky and does not work. In this case, reselect the piece again.</li>
</ol>


**All rights reserved.** <br>
**Copyright © 2022 D0jyaaan.**

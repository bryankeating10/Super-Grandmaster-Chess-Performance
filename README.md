# **Chess Performance Analytics**
## :warning::construction: Under construction! :warning::construction:
## Project Overview

The goal of this project is to analyze chess players’ performance across large databases of games stored in PGN format.
By structuring, processing, and visualizing this data, the project aims to uncover insights such as move efficiency, time usage, opening success rates, and player improvement over time.

This project leverages Python, Pandas, and custom-built classes (MetaData, MoveData, and future analytics modules) to organize chess data and extract meaningful metrics.

## Introduction
PGN is an acronym for Portable Game Notation and stores chess game data in a standardized format. The metadata is formated as key-value pairs:
```
[Event "Live Chess"]
[Site "Chess.com"]
[Date "2014.01.06"]
[White "Hikaru"]
[Black "Godswill"]
[Result "1-0"]
```
and the move data is stored as either a semi-structured list of moves:
```
1.e4 e5 2.Nf3 f5 3.Nxe5 Qf6 4.d4 d6
5.Nc4 fxe4 6.Nc3 Ne7 7.d5 Qg6 8.h3 h5  1-0
```
or a semi-structured list of key-value pairs:
```
1. e4 { [%eval 0.17] [%clk 0:00:30] } 1... c5 { [%eval 0.19] [%clk 0:00:30] }
2. Nf3 { [%eval 0.25] [%clk 0:00:29] } 2... Nc6 { [%eval 0.33] [%clk 0:00:30] }
3. Bc4 { [%eval -0.13] [%clk 0:00:28] } 3... e6 { [%eval -0.04] [%clk 0:00:30] } 0-1
```

## Directory Structure

### `Data/`
Stores all raw and intermediate data files.
Example contents:
* PGN game files (raw data)
* CSV exports of game metadata and move data

### `Analysis/`
Contains Jupyter notebooks and scripts used to process and analyze data.
Example contents:
* `analyze_player.ipynb` — analyzes a specific player’s performance
* `opening_statistics.ipynb` — summarizes outcomes by opening

### `Tests/`
Houses test scripts to ensure data extraction and analytics run correctly.
Example contents:
* `test_metadata_extraction.py`
* `test_move_parsing.py`

### `Visuals/`
Stores all generated plots, charts, and other visual artifacts from the analysis notebooks.
Example contents:
* `elo_trend.png` — ELO trend over time for a player
* `move_time_distribution.png` — histogram of time spent per move

### `Reports/`
Contains final HTML reports or dashboards summarizing analytical findings and visuals.
Example contents:
* `player_summary.html` — per-player summary dashboards
* `opening_report.html` — aggregated opening analysis report

### `Core/`
Defines the core data models and logic.
Example contents:
* `metadata.py` — handles game-level metadata
* `movedata.py` — manages move parsing and timing
* `player_analytics.py` — high-level analysis across games

### `Utils/`
Contains reusable helper functions and shared utilities.
Example contents:
* `file_io.py` — file loading/saving utilities
* `data_cleaning.py` — functions for normalizing and validating data
* `visual_helpers.py` — setup and export of visualizations

## Future Goals
* Expand the analytics to include opponent-based performance metrics.
* Develop an interactive dashboard for browsing player statistics.
* Incorporate machine learning to predict outcomes or detect playstyle trends.

## Resources
* `Hikaru.pgn`
    * Platform: kaggle.com
    * Creator: Michal Wierzbicki
    * Dataset: [Hikaru Nakamura Chess.com Data](https://www.kaggle.com/datasets/michalwierzbicki/hikaru-nakamura-chesscom-online-chess-games/data?select=Hikaru.pgn)
* `lichess_sample.pgn`
    * Platform: liches.org
    * Creator: Lichess Community
    * Dataset: [Standard game sample](https://database.lichess.org/#standard_games)
* `chess.com_sample.pgn`
    * Platform: kaggle.com
    * Creator: Michal Wierzbicki
    * Dataset: [Hikaru Nakamura Chess.com Data](https://www.kaggle.com/datasets/michalwierzbicki/hikaru-nakamura-chesscom-online-chess-games/data?select=Hikaru.pgn)
* `pgn_mentor_sample.pgn`
    * Platform: pgnmentor.com
    * Creator: 64 Squares
    * Dataset: [Latvian-Elephant Opening](https://www.pgnmentor.com/files.html)
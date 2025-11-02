# **Chess Performance Analytics**
## :warning::construction: Under construction! :warning::construction:
## Project Overview

The goal of this project is to analyze chess players’ performance across large databases of games stored in PGN format.
By structuring, processing, and visualizing this data, the project aims to uncover insights such as move efficiency, time usage, opening success rates, and player improvement over time.

This project leverages Python, Pandas, and custom-built classes (MetaData, MoveData, and future analytics modules) to organize chess data and extract meaningful metrics.

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
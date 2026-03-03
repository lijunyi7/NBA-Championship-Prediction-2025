# NBA-Championship-Prediction-2025

A machine learning project that predicts NBA championship probability for playoff teams using historical team statistics (2005–2024) and a Random Forest classifier.

## Overview

This project:

1. **Fetches** playoff team and player data from the [NBA API](https://github.com/swar/nba_api)
2. **Builds** training datasets with team stats and champion labels (who won each year)
3. **Trains** a Random Forest model on features like win rate, shooting percentages, rebounds, assists, and playoff rank
4. **Evaluates** with leave-one-out cross-validation and can output championship probabilities for current or past playoff fields

## Project Structure

```
NBA-Championship-Prediction-2025/
├── getting_data.py          # Fetch playoff teams & players from NBA API
├── prep_tranning_data.py    # Build training data with champion labels, save by year
├── model_train.ipynb        # Model training, validation, and final model
├── playground.ipynb         # Exploration and ad-hoc analysis
├── requirements.txt         # Python dependencies
├── training_data/           # Generated training data
│   └── past_playoff_team_data/   # One CSV per season (e.g. 2005_playoff_teams.csv)
└── hansen_yang_website/     # Separate NBA analytics web app (see its README)
```

## Setup

### 1. Create a virtual environment (recommended)

```bash
python -m venv venv
source venv/bin/activate   # On Windows: venv\Scripts\activate
```

### 2. Install dependencies

```bash
pip install -r requirements.txt
```

Main dependencies:

- **nba-api** – NBA stats API client
- **pandas** – Data handling
- **scikit-learn** – Random Forest and metrics
- **numpy** – Numerical operations

## Usage

### Fetch and prepare data

From the project root:

```python
import getting_data
import prep_tranning_data

# Get playoff teams for a season (e.g. 2025)
teams_df = getting_data.get_playoff_teams_data(year=2025)

# Build training data for 2005–2024 and save by year
years = list(prep_tranning_data.champions.keys())
full_df = prep_tranning_data.build_championship_training_data(years, prep_tranning_data.champions)
prep_tranning_data.save_past_playoff_teams_by_year(
    full_df,
    output_root="training_data/past_playoff_team_data"
)
```

Optional: save per-team player stats:

```python
players_df = getting_data.get_playoff_players_data(year=2025, playoff_teams_df=teams_df)
getting_data.save_player_stats_per_team(players_df, output_dir="playoff_player_stats_2025")
```

### Train and evaluate the model

Open **`model_train.ipynb`** and run the cells. The notebook:

- Loads training data from `training_data/past_playoff_team_data/`
- Uses features: `WinPCT`, `FG_PCT`, `FG3_PCT`, `FT_PCT`, `REB`, `AST`, `TOV`, `STL`, `BLK`, `BLKA`, `PTS`, `PLUS_MINUS`, `PlayoffRank`
- Trains a **Random Forest** classifier (e.g. 300 trees, max depth 6, class_weight='balanced')
- Runs leave-one-out cross-validation by year/team
- Trains a final model on 2005–2024 and can predict championship probability for a given season’s playoff teams

### Explore data

Use **`playground.ipynb`** to inspect standings, merge results, and try different ideas without changing the main pipeline.

## Data and Model Details

- **Champion labels**: Stored in `prep_tranning_data.champions` (2005–2024). Each playoff team row gets `CHAMPION=1` for that year’s winner and `0` otherwise.
- **Features**: Regular-season team stats from the NBA API (win %, shooting %, counting stats, plus-minus, playoff rank).
- **Training data path**: By default the notebook expects CSVs in `training_data/past_playoff_team_data/` named `{year}_playoff_teams.csv`. Generate them with `prep_tranning_data` as above.

## Subproject: Hansen Yang Website

The **`hansen_yang_website/`** folder contains a separate React + Vite app for Hansen Yang’s NBA analytics (bilingual, real-time data). See **`hansen_yang_website/README.md`** for setup and run instructions.

## License

Use and modify as needed for your own analysis. NBA data is subject to the NBA’s terms of use.

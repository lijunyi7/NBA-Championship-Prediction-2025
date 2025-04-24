from getting_data import get_playoff_teams_data, get_playoff_players_data 
import pandas as pd
import os
import time

champions = {
    2005: "San Antonio Spurs",
    2006: "Miami Heat",
    2007: "San Antonio Spurs",
    2008: "Boston Celtics",
    2009: "Los Angeles Lakers",
    2010: "Los Angeles Lakers",
    2011: "Dallas Mavericks",
    2012: "Miami Heat",
    2013: "Miami Heat",
    2014: "San Antonio Spurs",
    2015: "Golden State Warriors",
    2016: "Cleveland Cavaliers",
    2017: "Golden State Warriors",
    2018: "Golden State Warriors",
    2019: "Toronto Raptors",
    2020: "Los Angeles Lakers",
    2021: "Milwaukee Bucks",
    2022: "Golden State Warriors",
    2023: "Denver Nuggets",
    2024: "Golden State Warriors"
}

def build_championship_training_data(years, champions_dict):
    """
    Builds a training dataset from multiple years of playoff team stats.
    """
    training_data = []
    for year in years:
        try:
            # print(f"Fetching data for {year}...")
            df = get_playoff_teams_data(year)
            df['SEASON'] = year

            # Add champion label
            df['CHAMPION'] = df['TEAM_NAME'].apply(
                lambda x: 1 if x.lower() == champions_dict[year].lower() else 0
            )

            training_data.append(df)
        except Exception as e:
            print(f"Error in year {year}: {e}")

    full_df = pd.concat(training_data, ignore_index=True)
    return full_df




def save_past_playoff_teams_by_year(df, output_root="training_data/teams/past_playoff_data"):
    """
    Saves each season's playoff team data as a separate CSV inside a structured directory.
    """
    os.makedirs(output_root, exist_ok=True)

    # Group the training data by year
    for year, group in df.groupby('SEASON'):
        filename = f"{int(year)}_playoff_teams.csv"
        filepath = os.path.join(output_root, filename)
        group.to_csv(filepath, index=False)




# def build_championship_training_data(years, champions_dict,
#                                      team_output_root="training_data/past_playoff_data",
#                                      player_output_root="training_data/past_playoff_players"):
#     """
#     Builds a training dataset from multiple years of playoff team stats
#     and saves both team and player stats per year.
#     """
#     os.makedirs(team_output_root, exist_ok=True)
#     os.makedirs(player_output_root, exist_ok=True)

#     training_data = []

#     for year in years:
#         try:
#             print(f"📥 Fetching playoff teams for {year}...")
#             df = get_playoff_teams_data(year)
#             df['SEASON'] = year

#             # Add CHAMPION column
#             df['CHAMPION'] = df['TEAM_NAME'].apply(
#                 lambda x: 1 if x.lower() == champions_dict[year].lower() else 0
#             )

#             # Save this year's team stats
#             team_path = os.path.join(team_output_root, f"{year}_playoff_teams.csv")
#             df.to_csv(team_path, index=False)
#             print(f"✅ Saved team stats: {team_path}")

#             # Save this year's player stats
#             print(f"📥 Fetching playoff players for {year}...")
#             player_df = get_playoff_players_data(year, playoff_teams_df=df)
#             player_path = os.path.join(player_output_root, f"{year}_playoff_players.csv")
#             player_df.to_csv(player_path, index=False)
#             print(f"✅ Saved player stats: {player_path}")

#             # Add to master training set
#             training_data.append(df)

#             # Respect rate limits
#             time.sleep(1)

#         except Exception as e:
#             print(f"⚠️ Error in year {year}: {e}")

#     full_df = pd.concat(training_data, ignore_index=True)
#     return full_df
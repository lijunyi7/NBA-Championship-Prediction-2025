from nba_api.stats.endpoints import leaguedashteamstats, leaguestandings, leaguedashplayerstats
import pandas as pd
import time
import os



def get_playoff_teams_data(year=2025):
    """
    Get the playoff teams data for a given year and season type.
    """
    time.sleep(1)

    # Get all basic team stats includes playoff ranks
    standings = leaguestandings.LeagueStandings(season=f"{year-1}-{str(year)[-2:]}")
    standings_df = standings.get_data_frames()[0]

    standings_df = standings_df[[
        'TeamID', 'TeamCity', 'TeamName', 'Conference', 'PlayoffRank', 'WINS', 'LOSSES', 'WinPCT'
    ]]
    standings_df['TEAM'] = standings_df['TeamCity'] + ' ' + standings_df['TeamName']

    # Filter for playoff teams
    time.sleep(1)
    team_stats = leaguedashteamstats.LeagueDashTeamStats(season=f"{year-1}-{str(year)[-2:]}")
    stats_df = team_stats.get_data_frames()[0]

    # Merge the two dataframes
    merged = pd.merge(
    stats_df,
    standings_df,
    left_on='TEAM_ID',
    right_on='TeamID',
    how='inner'
    )

    # Filter the merged dataframe to keep only the relevant columns
    columns_to_keep = [
        'TEAM_ID', 'TEAM_NAME', 'Conference', 'PlayoffRank',
        'WinPCT', 'FG_PCT', 'FG3_PCT', 'FT_PCT',
        'REB', 'AST', 'TOV', 'STL', 'BLK', 'BLKA',
        'PTS', 'PLUS_MINUS'
    ]
    merged_filtered = merged[[col for col in columns_to_keep if col in merged.columns]]
    # merged_filtered.sort_values(by=['Conference', 'PlayoffRank'])
    east = merged_filtered[merged_filtered['Conference'] == 'East'].sort_values(by='PlayoffRank').head(8)
    west = merged_filtered[merged_filtered['Conference'] == 'West'].sort_values(by='PlayoffRank').head(8)
    play_off_df = pd.concat([east, west]).sort_values(by=['Conference', 'PlayoffRank'])
    return play_off_df



def get_playoff_players_data(year=2025, playoff_teams_df=None):
    """
    Get the playoff players data for a given year and season type.
    """
    if playoff_teams_df is None:
        playoff_teams_df = get_playoff_teams_data(year)

    time.sleep(1)

    # Get all player stats from the season
    player_stats = leaguedashplayerstats.LeagueDashPlayerStats(
        season=f"{year-1}-{str(year)[-2:]}"
    )
    player_df = player_stats.get_data_frames()[0]

    # Filter only players from playoff teams
    playoff_team_ids = playoff_teams_df['TEAM_ID'].unique()
    playoff_players_df = player_df[player_df['TEAM_ID'].isin(playoff_team_ids)]
    return playoff_players_df


def save_player_stats_per_team(playoff_players_df, output_dir="playoff_player_stats_2025"):
    """
    Save each playoff team's player stats into a separate CSV file.
    """
    # Create output directory if it doesn't exist
    os.makedirs(output_dir, exist_ok=True)

    # Group players by team ID or team abbreviation
    grouped = playoff_players_df.groupby('TEAM_ABBREVIATION')

    for team_abbr, group in grouped:
        # Create a clean filename
        filename = f"{team_abbr}_players.csv"
        filepath = os.path.join(output_dir, filename)

        # Save to CSV
        group.to_csv(filepath, index=False)



    







    




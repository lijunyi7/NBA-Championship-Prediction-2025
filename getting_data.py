from nba_api.stats.endpoints import leaguedashteamstats, leaguestandings
import pandas as pd
import time


def get_playoff_teams(year=2025, season_type="Regular Season"):
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






    




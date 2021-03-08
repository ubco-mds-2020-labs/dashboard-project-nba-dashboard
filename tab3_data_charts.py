import pandas as pd
import altair as alt
alt.data_transformers.disable_max_rows()

# read in data
full_data = pd.read_csv("players_stats_by_season_full_details.csv")
# filter data to only include NBA
NBA_data = full_data[full_data["League"] == "NBA"]
# Regular season data
NBA_reg = NBA_data[NBA_data['Stage'] == "Regular_Season"]
# Playoff data
NBA_playoff = NBA_data[NBA_data['Stage'] == 'Playoffs']
# group by the seasons and sum up numerical columns. This shows stats by season (this includes regular season and playoff games together)
NBA_seasons_full = NBA_data.groupby('Season').sum().reset_index()

# list for the drop down menu
longform_stat_list = ['Average Player Minutes Played per Game', 'Field Goals Made per Game', 'Field Goals Attempted per Game',
'3-Pointers Made per Game', '3-Pointers Attempted per Game', 'Free-throws Made per Game',
'Free-throws Attempted per Game', 'Turnovers per Game', 'Personal Fouls per Game', 'Offensive Rebounds per Game',
'Defensive Rebounds per Game', 'Total Rebounds per Game', 'Assists per Game', 'Steals per Game', 
'Blocks per Game', 'Points per Game', 'Average Player Weight', 'Average Player Height', 'Average Player Body Mass Index', 'Percentage of Field Goals That Are 3-pointers']

# dictionary linking dropdown list key to stat value column labels
stat_dict = {'Average Player Minutes Played per Game':'MIN/Game', 'Field Goals Made per Game':'FGM/Game', 
'Field Goals Attempted per Game':'FGA/Game', '3-Pointers Made per Game':'3PM/Game',
'3-Pointers Attempted per Game':'3PA/Game', 'Free-throws Made per Game':'FTM/Game',
'Free-throws Attempted per Game':'FTA/Game', 'Turnovers per Game':'TOV/Game', 'Personal Fouls per Game':'PF/Game', 'Offensive Rebounds per Game':'ORB/Game', 'Defensive Rebounds per Game':'DRB/Game', 'Total Rebounds per Game':'REB/Game', 'Assists per Game':'Ast/Game', 'Steals per Game':'STL/Game', 
'Blocks per Game':'BLK/Game', 'Points per Game':'Pts/Game', 'Average Player Weight (lbs)':'avg_weight', 'Average Player Height (cm)':'avg_height_cm', 'Average Player Body Mass Index':'avg_BMI', 'Ratio of Field Goals That Are 3-pointers':'3PM_ratio'}




## Data wrangling for stats over time for players/teams:

# Create column for ratio of shots made that are 3-pointers
NBA_seasons_full['3PM_ratio'] = (NBA_seasons_full['3PM']/NBA_seasons_full['FGM'])
# Create a column for average player height (need to create a season average dataframe first)
NBA_seasons_full_avg = NBA_data.groupby('Season').mean().reset_index()
NBA_seasons_full['avg_height_cm'] = NBA_seasons_full_avg['height_cm']
# Create a column for average player weight (lbs)
NBA_seasons_full['avg_weight'] = NBA_seasons_full_avg['weight']
# Create a column for average player BMI
NBA_seasons_full['avg_BMI'] = NBA_seasons_full_avg['weight_kg']/((NBA_seasons_full_avg['height_cm']/100)**2)
## All of the following numerical stats per game (eg. points, assists, etc.) are found by 
## getting the stat/minute/player, then multiplying that by 5 for 5 players on the court at 
## a time for each team and then multiplying by 48 for 48 minutes in a game. 
# Create a points per game column
NBA_seasons_full['Pts/Game'] = (NBA_seasons_full['PTS']/NBA_seasons_full['MIN'])*(5*48)
# Create an assists per game column
NBA_seasons_full['Ast/Game'] = (NBA_seasons_full['AST']/NBA_seasons_full['MIN'])*(5*48)
# Create a field goals attempted per game column
NBA_seasons_full['FGA/Game'] = (NBA_seasons_full['FGA']/NBA_seasons_full['MIN'])*(5*48)
# Create a field goals made per game column
NBA_seasons_full['FGM/Game'] = (NBA_seasons_full['FGM']/NBA_seasons_full['MIN'])*(5*48)
# Create a total rebounds per game column
NBA_seasons_full['ORB/Game'] = (NBA_seasons_full['ORB']/NBA_seasons_full['MIN'])*(5*48)
# Create a defensive rebounds per game column
NBA_seasons_full['DRB/Game'] = (NBA_seasons_full['DRB']/NBA_seasons_full['MIN'])*(5*48)
# Create a total rebounds per game column
NBA_seasons_full['REB/Game'] = (NBA_seasons_full['REB']/NBA_seasons_full['MIN'])*(5*48)
# Create a minutes per game column
NBA_seasons_full['MIN/Game'] = NBA_seasons_full['MIN']/NBA_seasons_full['GP']
# Create a 3 pointers made per game column
NBA_seasons_full['3PM/Game'] = (NBA_seasons_full['3PM']/NBA_seasons_full['MIN'])*(5*48)
# Create a 3-pointers attempted per game column
NBA_seasons_full['3PA/Game'] = (NBA_seasons_full['3PA']/NBA_seasons_full['MIN'])*(5*48)
# Create a free-throws attempted per game column
NBA_seasons_full['FTA/Game'] = (NBA_seasons_full['FTA']/NBA_seasons_full['MIN'])*(5*48)
# Create a free-throws attempted per game column
NBA_seasons_full['FTM/Game'] = (NBA_seasons_full['FTM']/NBA_seasons_full['MIN'])*(5*48)
# Create a turnovers per game column
NBA_seasons_full['TOV/Game'] = (NBA_seasons_full['TOV']/NBA_seasons_full['MIN'])*(5*48)
# Create a personal fouls per game column
NBA_seasons_full['PF/Game'] = (NBA_seasons_full['PF']/NBA_seasons_full['MIN'])*(5*48)
# Create a steals per game column
NBA_seasons_full['STL/Game'] = (NBA_seasons_full['STL']/NBA_seasons_full['MIN'])*(5*48)
# Create a blocks per game column
NBA_seasons_full['BLK/Game'] = (NBA_seasons_full['BLK']/NBA_seasons_full['MIN'])*(5*48)




## Data Wrangling for stats over time for age.

NBA_data_age = NBA_data.copy()
# Convert birth year to integer
NBA_data_age['birth_year'] = NBA_data_age['birth_year'].map(lambda x: int(x))
NBA_data_age.reset_index(drop=True, inplace=True)
# Convert Season to the year the season ended (instead of the two years the season spans)
# and convert it to an integer. 
NBA_data_age['Season'] = NBA_data_age['Season'].map(lambda x: int(x[-4:len(x)]))
# Create a column for age by subtracting birth year from the season year 
#(use year of playoffs)
NBA_data_age['Age'] = NBA_data_age['Season'] - NBA_data_age['birth_year']
# Drop ages > 39 years old because there are less than 30 players in these
# age groups so the average estimates are likely to be innacurate. 
NBA_data_age = NBA_data_age[NBA_data_age['Age'] < 40]
# Group the NBA data by age and sum up the numerical categories
NBA_age_avg = NBA_data_age.groupby('Age').mean().reset_index()
NBA_age_sum = NBA_data_age.groupby('Age').sum().reset_index()
# Create column for ratio of shots made that are 3-pointers
NBA_age_sum['3PM_ratio'] = (NBA_age_sum['3PM']/NBA_age_sum['FGM'])
# Create a column for average player height (need to create a season average dataframe first)
NBA_age_sum['avg_height_cm'] = NBA_age_avg['height_cm']
# Create a column for average player weight (lbs)
NBA_age_sum['avg_weight'] = NBA_age_avg['weight']
# Create a column for average player BMI
NBA_age_sum['avg_BMI'] = NBA_age_avg['weight_kg']/((NBA_age_avg['height_cm']/100)**2)
## All of the following numerical stats per game by age (eg. points, assists, etc.) are 
##found by getting the stat/game played. 
# Create a points per game column
NBA_age_sum['Pts/Game'] = NBA_age_sum['PTS']/NBA_age_sum['GP']
# Create an assists per game column
NBA_age_sum['Ast/Game'] = NBA_age_sum['AST']/NBA_age_sum['GP']
# Create a field goals attempted per game column
NBA_age_sum['FGA/Game'] = NBA_age_sum['FGA']/NBA_age_sum['GP']
# Create a field goals made per game column
NBA_age_sum['FGM/Game'] = NBA_age_sum['FGM']/NBA_age_sum['GP']
# Create a total rebounds per game column
NBA_age_sum['ORB/Game'] = NBA_age_sum['ORB']/NBA_age_sum['GP']
# Create a defensive rebounds per game column
NBA_age_sum['DRB/Game'] = NBA_age_sum['DRB']/NBA_age_sum['GP']
# Create a total rebounds per game column
NBA_age_sum['REB/Game'] = NBA_age_sum['REB']/NBA_age_sum['GP']
# Create a minutes per game column
NBA_age_sum['MIN/Game'] = NBA_age_sum['MIN']/NBA_age_sum['GP']
# Create a 3 pointers made per game column
NBA_age_sum['3PM/Game'] = NBA_age_sum['3PM']/NBA_age_sum['GP']
# Create a 3-pointers attempted per game column
NBA_age_sum['3PA/Game'] = NBA_age_sum['3PA']/NBA_age_sum['GP']
# Create a free-throws attempted per game column
NBA_age_sum['FTA/Game'] = NBA_age_sum['FTA']/NBA_age_sum['GP']
# Create a free-throws attempted per game column
NBA_age_sum['FTM/Game'] = NBA_age_sum['FTM']/NBA_age_sum['GP']
# Create a turnovers per game column
NBA_age_sum['TOV/Game'] = NBA_age_sum['TOV']/NBA_age_sum['GP']
# Create a personal fouls per game column
NBA_age_sum['PF/Game'] = NBA_age_sum['PF']/NBA_age_sum['GP']
# Create a steals per game column
NBA_age_sum['STL/Game'] = NBA_age_sum['STL']/NBA_age_sum['GP']
# Create a blocks per game column
NBA_age_sum['BLK/Game'] = NBA_age_sum['BLK']/NBA_age_sum['GP']




## Data Wrangling for playoff vs reg season stats chart

NBA_reg_seasons = NBA_reg.groupby('Season').sum().reset_index()
NBA_playoff_seasons = NBA_playoff.groupby('Season').sum().reset_index()




# Make regular season stats

# Create column for ratio of shots made that are 3-pointers
NBA_reg_seasons['3PM_ratio'] = (NBA_reg_seasons['3PM']/NBA_reg_seasons['FGM'])
# Create a column for average player height (need to create a season average dataframe first)
NBA_reg_seasons_avg = NBA_reg.groupby('Season').mean().reset_index()
NBA_reg_seasons['avg_height_cm'] = NBA_reg_seasons_avg['height_cm']
# Create a column for average player weight (lbs)
NBA_reg_seasons['avg_weight'] = NBA_reg_seasons_avg['weight']
# Create a column for average player BMI
NBA_reg_seasons['avg_BMI'] = NBA_reg_seasons_avg['weight_kg']/((NBA_reg_seasons_avg['height_cm']/100)**2)
## All of the following numerical stats per game (eg. points, assists, etc.) are found
## by getting the stat/minute/player, then multiplying that by 5 for 5 players on the 
## court at a time for each team and then multiplying by 48 for 48 minutes in a game. 
# Create a points per game column
NBA_reg_seasons['Pts/Game'] = (NBA_reg_seasons['PTS']/NBA_reg_seasons['MIN'])*(5*48)
# Create an assists per game column
NBA_reg_seasons['Ast/Game'] = (NBA_reg_seasons['AST']/NBA_reg_seasons['MIN'])*(5*48)
# Create a field goals attempted per game column
NBA_reg_seasons['FGA/Game'] = (NBA_reg_seasons['FGA']/NBA_reg_seasons['MIN'])*(5*48)
# Create a field goals made per game column
NBA_reg_seasons['FGM/Game'] = (NBA_reg_seasons['FGM']/NBA_reg_seasons['MIN'])*(5*48)
# Create a total rebounds per game column
NBA_reg_seasons['ORB/Game'] = (NBA_reg_seasons['ORB']/NBA_reg_seasons['MIN'])*(5*48)
# Create a defensive rebounds per game column
NBA_reg_seasons['DRB/Game'] = (NBA_reg_seasons['DRB']/NBA_reg_seasons['MIN'])*(5*48)
# Create a total rebounds per game column
NBA_reg_seasons['REB/Game'] = (NBA_reg_seasons['REB']/NBA_reg_seasons['MIN'])*(5*48)
# Create a minutes per game column
NBA_reg_seasons['MIN/Game'] = NBA_reg_seasons['MIN']/NBA_reg_seasons['GP']
# Create a 3 pointers made per game column
NBA_reg_seasons['3PM/Game'] = (NBA_reg_seasons['3PM']/NBA_reg_seasons['MIN'])*(5*48)
# Create a 3-pointers attempted per game column
NBA_reg_seasons['3PA/Game'] = (NBA_reg_seasons['3PA']/NBA_reg_seasons['MIN'])*(5*48)
# Create a free-throws attempted per game column
NBA_reg_seasons['FTA/Game'] = (NBA_reg_seasons['FTA']/NBA_reg_seasons['MIN'])*(5*48)
# Create a free-throws attempted per game column
NBA_reg_seasons['FTM/Game'] = (NBA_reg_seasons['FTM']/NBA_reg_seasons['MIN'])*(5*48)
# Create a turnovers per game column
NBA_reg_seasons['TOV/Game'] = (NBA_reg_seasons['TOV']/NBA_reg_seasons['MIN'])*(5*48)
# Create a personal fouls per game column
NBA_reg_seasons['PF/Game'] = (NBA_reg_seasons['PF']/NBA_reg_seasons['MIN'])*(5*48)
# Create a steals per game column
NBA_reg_seasons['STL/Game'] = (NBA_reg_seasons['STL']/NBA_reg_seasons['MIN'])*(5*48)
# Create a blocks per game column
NBA_reg_seasons['BLK/Game'] = (NBA_reg_seasons['BLK']/NBA_reg_seasons['MIN'])*(5*48)




## Make playoff stats

# Create column for ratio of shots made that are 3-pointers
NBA_playoff_seasons['3PM_ratio'] = (NBA_playoff_seasons['3PM']/NBA_playoff_seasons['FGM'])
# Create a column for average player height (need to create a season average dataframe first)
NBA_playoff_seasons_avg = NBA_playoff.groupby('Season').mean().reset_index()
NBA_playoff_seasons['avg_height_cm'] = NBA_playoff_seasons_avg['height_cm']
# Create a column for average player weight (lbs)
NBA_playoff_seasons['avg_weight'] = NBA_playoff_seasons_avg['weight']
# Create a column for average player BMI
NBA_playoff_seasons['avg_BMI'] = NBA_playoff_seasons_avg['weight_kg']/((NBA_playoff_seasons_avg['height_cm']/100)**2)
## All of the following numerical stats per game (eg. points, assists, etc.) are found
## by getting the stat/minute/player, then multiplying that by 5 for 5 players on the 
## court at a time for each team and then multiplying by 48 for 48 minutes in a game. 
# Create a points per game column
NBA_playoff_seasons['Pts/Game'] = (NBA_playoff_seasons['PTS']/NBA_playoff_seasons['MIN'])*(5*48)
# Create an assists per game column
NBA_playoff_seasons['Ast/Game'] = (NBA_playoff_seasons['AST']/NBA_playoff_seasons['MIN'])*(5*48)
# Create a field goals attempted per game column
NBA_playoff_seasons['FGA/Game'] = (NBA_playoff_seasons['FGA']/NBA_playoff_seasons['MIN'])*(5*48)
# Create a field goals made per game column
NBA_playoff_seasons['FGM/Game'] = (NBA_playoff_seasons['FGM']/NBA_playoff_seasons['MIN'])*(5*48)
# Create a total rebounds per game column
NBA_playoff_seasons['ORB/Game'] = (NBA_playoff_seasons['ORB']/NBA_playoff_seasons['MIN'])*(5*48)
# Create a defensive rebounds per game column
NBA_playoff_seasons['DRB/Game'] = (NBA_playoff_seasons['DRB']/NBA_playoff_seasons['MIN'])*(5*48)
# Create a total rebounds per game column
NBA_playoff_seasons['REB/Game'] = (NBA_playoff_seasons['REB']/NBA_playoff_seasons['MIN'])*(5*48)
# Create a minutes per game column
NBA_playoff_seasons['MIN/Game'] = NBA_playoff_seasons['MIN']/NBA_playoff_seasons['GP']
# Create a 3 pointers made per game column
NBA_playoff_seasons['3PM/Game'] = (NBA_playoff_seasons['3PM']/NBA_playoff_seasons['MIN'])*(5*48)
# Create a 3-pointers attempted per game column
NBA_playoff_seasons['3PA/Game'] = (NBA_playoff_seasons['3PA']/NBA_playoff_seasons['MIN'])*(5*48)
# Create a free-throws attempted per game column
NBA_playoff_seasons['FTA/Game'] = (NBA_playoff_seasons['FTA']/NBA_playoff_seasons['MIN'])*(5*48)
# Create a free-throws attempted per game column
NBA_playoff_seasons['FTM/Game'] = (NBA_playoff_seasons['FTM']/NBA_playoff_seasons['MIN'])*(5*48)
# Create a turnovers per game column
NBA_playoff_seasons['TOV/Game'] = (NBA_playoff_seasons['TOV']/NBA_playoff_seasons['MIN'])*(5*48)
# Create a personal fouls per game column
NBA_playoff_seasons['PF/Game'] = (NBA_playoff_seasons['PF']/NBA_playoff_seasons['MIN'])*(5*48)
# Create a steals per game column
NBA_playoff_seasons['STL/Game'] = (NBA_playoff_seasons['STL']/NBA_playoff_seasons['MIN'])*(5*48)
# Create a blocks per game column
NBA_playoff_seasons['BLK/Game'] = (NBA_playoff_seasons['BLK']/NBA_playoff_seasons['MIN'])*(5*48)

##Add a column of type of season to grouped dataframes
list = ['Regular Season'] * len(NBA_reg_seasons)
col = pd.Series(list)
NBA_reg_seasons['Type'] = col

plist = ['Playoffs'] * len(NBA_playoff_seasons)
pcol = pd.Series(plist)
NBA_playoff_seasons['Type'] = pcol

# Combine playoffs and regular season dataframes into one
type_seasons = NBA_reg_seasons.append(NBA_playoff_seasons)





## Function for chart 1 (stats of teams/players over time)

def simple_stat(stat):
    # Use dictionary key to get the proper column
    leave_list = ['Average Player Minutes Played per Game', 'Average Player Weight', 'Average Player Height', 'Average Player Body Mass Index', 'Percentage of Field Goals That Are 3-pointers']
    stat_label = stat_dict[stat]
    if stat not in leave_list:
        stat = stat + ' per Team'
    line_chart = alt.Chart(NBA_seasons_full, title=alt.TitleParams(text=stat)).mark_line(color='#f6573f', size=3).encode(alt.Y(stat_label, scale= alt.Scale(zero=False),
    axis=alt.Axis(grid=False), title=None), alt.X('Season')).configure_view(strokeWidth=0)
    return line_chart



## Function for chart 2 (stats of players by age)

def simple_stat_age(stat):
    # Use dictionary key to get the proper column
    stat_label = stat_dict[stat]
    line_chart = alt.Chart(NBA_age_sum, title=alt.TitleParams(text=stat)).mark_line(color="#969696", size=3).encode(alt.Y(stat_label, scale= alt.Scale(zero=False),
    axis=alt.Axis(grid=False), title=None), alt.X('Age', axis=alt.Axis(grid=False))).configure_view(strokeWidth=0)
    return line_chart



## Function for chart 3 (stats in playoffs vs. regular season)

def type_stat(stat):
    # Use dictionary key to get the proper column
    leave_list = ['Average Player Minutes Played per Game', 'Average Player Weight', 'Average Player Height', 'Average Player Body Mass Index', 'Percentage of Field Goals That Are 3-pointers']
    stat_label = stat_dict[stat]
    if stat not in leave_list:
        stat = stat + ' per Team'
    stat = stat + ' by Season'
    bar_chart = alt.Chart(type_seasons).mark_bar().encode(alt.Y(stat_label, scale= alt.Scale(zero=False),
    axis=alt.Axis(grid=False), title=None, stack=None), alt.X('Type', axis=None), alt.Column('Season', title = stat,
    header= alt.Header(labelOrient='bottom', labelAngle=90, labelPadding=60)), alt.Color('Type', legend = alt.Legend(orient = 'bottom', title=None))).properties(width=15).configure_facet(spacing=5).configure_axis(grid=False).configure_view(strokeWidth=0)
    return bar_chart
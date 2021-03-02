

# Motivation & Purpose

__Our Role:__ Sports Analytics Consulting Firm

__Target Audience:__ NBA General Managers, Scouts, Coaching Staff, Training Staff, and Fans

__Purpose:__

With the enormous growth of media technology, sports teams are now relying on high-tech analytics to gain an edge against opposing teams. The increased focus towards tracking individual player and team statistics has allowed for a deeper understanding of how gameplay in the NBA has evolved, team performance, player performance, and player health. Thus, we propose building a data visualization app that allows NBA General Managers, Scouts, and Coaches to visually explore player and team performance to identify factors that can attribute to team success. Our app will show individual player statistics throughouts their careers such as points (ppg), assists (ast), rebounds (reb), blocks (blk), steals (stl), field goal percentages (fg%), 3-point percentages (3p%), and free-throw percentages (ft%). In addition, we will show advanced analytics such as player performance as they age to infer possible correlations between player performance and fatigue. Finally, we will explore trends in team statistics throughout the years such as 3-point attempts to understsand how gameplay and player skillset has evolved.

# Description of the Data

Our dashboard will be visualizing data from the `players_stats_by_season_full_details.csv` dataset found on [Kaggle](https://www.kaggle.com/jacobbaruch/basketball-players-stats-per-season-49-leagues). This dataset contains statistics for professional basketball players in multiple leagues. For our dashboard, we will be limiting the data to only include players in the National Basketball Association (NBA). Each row in the data set pertains to a single player in a single season or a single playoff season. Some of the statistics that will be visualized in our dashboard are `PTS` (points), `AST` (assists), `FGM` (field goals made), `FGA` (field goals attempted), `3PM` (3-pointers made), `3PA` (3-pointers attempted), `REB` (rebounds), `STL` (steals), and `BLK` (blocks). Additionally, we will be wrangling the data to derive metrics such as points per game, assists per game, and rebounds per game. The data will also be manipulated to view overall trends in performance statistics throughout the NBA as a whole (ie. the average percentage of shots that are three pointers in a season throughout the NBA). Complementary data and other variables may be added through data wrangling to aid in further analysis.

# Research Questions

1. How has the 3-point shot evolved over time in the NBA?

   - We would observe how the 3-point shot has evolved by position and height.

2. What are other performance trends observed in the NBA over time?

   - Are players becoming more skilled beyond what is expected of their position? For example, are today's forwards and centers averaging higher assists per game compared to their predecessors? Are point guards scoring more compared to points guards of the past?

3. How long do players typically maintain their peak performance (prime) before their performance starts declining?

   - How many minutes on average do players play before a noticeable decline in performance is observed?

4. What are a few performance metrics that differentiate playoff teams from non-playoff teams?

   - What is the distribution of performance statistics across a team?

   - Do playoff teams have stronger supporting players (bench) in addition to superstar players?

5. Does a player’s position in the draft correlate to their ranking in important statistical categories throughout their career?

   

# Usage Scenario 1
Naveen is an NBA analyst for the Brooklyn Nets. Currently they have a great team with a lot of star power, but their budget is tight and they are looking for ways to add value in the future without increasing their payroll. The Nets superstars seem to be in their prime, but the front office is wondering if they should continue to sign expensive long term deals with these players. Naveen is wondering if these star players are currently at their peak and if their performance is likely to suffer in the future based on their age. He uses his NBA analytics app to view the NBA averages of statistics by age. He is able to see at what age players (on average) peak in the different performance categories. He can then compare the star players individual career stats and see if they follow a similar trajectory to the average statistical trends and determine if those players have peaked yet (statistically speaking). Naveen is also able to see how the trends of certain statistics in the NBA are changing over time (for instance, there are much more three-pointers attempted in today’s NBA), so he can help shape the team by encouraging management to select players who will excel in the desired performance areas. 

# Usage Scenario 2

The NBA draft is coming up and the Nets are trying to find hidden value in the later rounds of the draft. In need of a 3-point shooter, the Nets front office asks their top scout Naveen to review the prospects from the draft. When comparing the Nets to successful playoff teams on the NBA Analytics app, Naveen realizes that the Nets are in dire need of a player to help contribute in assists and steals. Based on his findings, it is clear to Naveen that he must select a player who not only specializes in 3-pointers, but can also fill these gaps for the Brooklyn Nets.
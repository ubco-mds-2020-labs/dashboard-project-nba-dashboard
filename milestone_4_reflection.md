# Milestone # 4 Reflection

### March 25, 2021

### Group Participants:
- Connor Fairbanks
- Tony Zhou
- Graham Kerford
- Naveen Chalasani

During this week, we decided to implement some of the suggestions we received from Firas. We removed the borders of the iframes from our plots, and we changed the y-axis for our `true shooting %` graph to start at zero. Removing the borders also improved the aesthetics of the plots (which was one of the feedback suggestions we received from peers). We also improved the structure of our code by adding PEP8 style docstrings to the functions and adding other explanatory comments in the code. A glossary tab was added to define the statistics used in the dashboard. 

Throughout our testing of the dashboard, we realized that when certain players were selected, some plots had scroll bars around them. These scroll bars were removed. We felt that our python dashboard was quite fast, so we did not make any changes to improve the speed of performance. Automatic deployment from GitHub to Heroku was also implemented this week. 

One recurring theme of feedback we received was the suggestion to allow comparison between two players. The goal of our dashboard was to display as much information about a selected player as we could, while still maintaining a clean dashboard with plots that are easy to interpret. We decided to omit the ability to compare two players due to the spatial constraints. Having all of the included statistics for more than one player would result in very busy charts which would become difficult for users to understand.

We have yet to implement the incorporation of adding up-to-date data to the dashboard by using the NBA API. Limited working time was the reason we decided not to include this feature. All of our plots and code were based on pulling data from one specific dataframe that we chose as our source. The task of changing all of the code and plots to source from an API would have required more time than was available to us. Building (or learning to use a previously existing) API wrapper for the NBA data would have taken too long for us to complete at our experience level and with our existing course load. 

Another recurring theme that we noted was the positive feedback we received for our use of tiles. Our peers seemed to appreciate the summary statistics displayed in the tiles on the first two tabs. We will remember this feedback and consider including such tiles in the dashboards that we design in the future. 

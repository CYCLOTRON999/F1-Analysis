import streamlit as st
import pandas as pd
import plotly.express as px
import matplotlib.pyplot as plt

st.set_page_config(page_title="Formula 1 Analysis", page_icon="🏎️", layout="wide")

drivers = pd.read_csv('drivers_updated.csv')
ddrivers = ['Driver','Code','Nationality','year','Car','PTS','Pos']
drivers = drivers[ddrivers]
drivers.rename(columns={'year':'Year','PTS':'Points','Pos':'Position'}, inplace=True)
teams = pd.read_csv('teams_updated.csv')
teams.rename(columns={'Pos':'Position','PTS':'Points','year':'Year'}, inplace=True)
fastest_laps = pd.read_csv('fastest_laps_updated.csv')
fastest_laps.rename(columns={'year':'Year'}, inplace=True)
winners = pd.read_csv('winners.csv')
race_result = pd.read_csv('race_results_2020.csv')



st.title("""THE  FORMULA  1   🏎️...""")
st.header("Welcome to the world beyond the grid, where speed meets strategy, and every second counts. Dive into the thrilling universe of Formula 1, where precision engineering, daring drivers, and cutting-edge technology converge to create a spectacle like no other. Explore the history, analyze the data, and experience the adrenaline of the world's premier motorsport.")
st.subheader("Formula 1")
st.write(""""F1", "Formula 1", "FIA F1 World Championship", and "FIA Formula One World Championship" """)
st.write("""Formula One is the highest class of international racing for open-wheel, single-seater formula racing cars. Sanctioned by the Fédération Internationale de l'Automobile (FIA) and managed by the Formula One Group, the FIA Formula One World Championship has been one of the premier forms of motorsport worldwide since its inaugural season in 1950.
         The word "formula" in the name refers to a strict set of technical, sporting, and financial regulations to which all participants' cars must conform.""")
st.subheader("History of Formula 1")
st.write("""Formula One originated from the European Grand Prix championships of the 1920s and 1930s. The foundation for the modern format was drafted in 1946, with the first non-championship races held later that year. The inaugural World Championship race took place at Silverstone, United Kingdom, in 1950.""")
st.subheader("Championship Format")
st.write("""A season consists of a series of races, termed Grands Prix, contested on purpose-built circuits and closed public streets. Results are tallied via a standardized points system to award two annual titles: the World Drivers' Championship and the World Constructors' Championship (for manufacturers).
         
The Weekend: Comprises free practice, a three-part knockout qualifying session to determine the starting grid, and a Sunday race covering at least 305 kilometres (190 mi). Select events include a short "Sprint" race.

The Grid: Composed of 10 teams, each fielding two drivers. Operations are constrained by a mandatory financial cost cap to promote competitive parity.""")
st.sidebar.title("All About Formula 1")
st.sidebar.header("Analysis About Formula 1")
optn = st.sidebar.selectbox('Select one',['Select an option...','DRIVERS','TEAMS','CIRCUIT ANALYSIS'])


if optn == 'DRIVERS':
    st.title('DRIVER\'S ANALYSIS')
    selected_driver = st.sidebar.selectbox('Select a driver',drivers['Driver'].unique())
    btn1 = st.sidebar.button('Show Driver Analysis')
    if btn1:
        st.dataframe(drivers[drivers['Driver'] == selected_driver], hide_index=True)        
        s = selected_driver.title()
        st.write(px.bar(drivers[drivers['Driver'] == selected_driver], x='Year', y='Points', title=f'Points of  {s} over the years'))
        st.subheader('Fastest Laps')
        st.dataframe(fastest_laps[fastest_laps['Driver'] == selected_driver].iloc[:,[0,2, 3, 4]], hide_index=True)
        with st.expander("Click to view Fastest Laps Analysis"):
            st.write(px.scatter(fastest_laps[fastest_laps['Driver'] == selected_driver], x='Year', y='Time', color='Grand Prix'))
        df = winners.groupby('Winner').get_group(selected_driver)['Grand Prix'].value_counts().sort_values(ascending=False).reset_index()
        df.columns = ['Grand Prix', 'Wins']
        st.plotly_chart(px.pie(df, names='Grand Prix', values='Wins', title=f'Grand Prix won by {selected_driver}').update_traces(textposition='inside', textinfo='percent+label'))
        
        
elif optn == 'TEAMS':
    st.title('TEAM\'S ANALYSIS')       
    selected_team = st.sidebar.selectbox('Select a team',teams['Team'].unique())
    st.write("There was no official Formula One World Constructors' Championship between 1950 - 1957.")
    btn1 = st.sidebar.button('Show Team Analysis')
    if btn1:
        st.subheader(selected_team)
        st.dataframe(teams[teams['Team'] == selected_team], hide_index=True)
        with st.expander("Click to view Team Points Analysis"):
            # st.write(px.line(teams[teams['Team'] == selected_team], x='Year', y='Position',hover_name='Points'))
            df = teams[teams['Team'] == selected_team]
            fig = px.line(df, x='Year', y='Position', hover_name='Points')
            fig.update_layout(yaxis=dict(autorange='reversed'))
            st.plotly_chart(fig)
        col1, col2 = st.columns(2)
        with col1:
            st.subheader('Podium Standing Analysis')
            st.plotly_chart(px.pie(race_result[race_result['Team'] == selected_team], names='Position', title=f'Podium finish of {selected_team} (Based on every race from 1950-2020)'))
        with col2:
            st.subheader('Constructor\'s Championship Position Analysis')
            st.plotly_chart(px.pie(teams[teams['Team'] == selected_team], names='Position', title=f'Success Rate of {selected_team} (Overall)').update_traces(textposition='inside', textinfo='percent+label'))
        
        
elif optn == 'CIRCUIT ANALYSIS':
    st.title('CIRCUIT ANALYSIS')
    selected_track = st.sidebar.selectbox('Select a Circuit',winners['Grand Prix'].unique())
    btn1 = st.sidebar.button('Show Circuit Analysis')
    if btn1:
        st.subheader('Circuit Analysis')
        st.dataframe(winners[winners['Grand Prix'] == selected_track], hide_index=True)
        col1, col2 = st.columns(2)
        winners.groupby('Grand Prix')
        with col1:
            top_driver = winners.groupby('Grand Prix').get_group(selected_track)['Winner'].value_counts().sort_values(ascending=False).head(10).reset_index()
            top_driver.columns = ['Driver', 'Wins']
            fig = px.bar(
                top_driver,
                x='Driver', 
                y='Wins', 
                title=f'Total Wins of Drivers(Top 10) in {selected_track}',
                labels={'Driver': 'Driver Name', 'Wins': 'Total Wins'},
                text_auto=True # Adds the win count right on top of the bars
            )
            st.plotly_chart(fig)
        with col2:
            top_team = winners.groupby('Grand Prix').get_group(selected_track)['Car'].value_counts().sort_values(ascending=False).head(10).reset_index()
            top_team.columns = ['Team', 'Wins']
            fig = px.pie(
                top_team,
                names='Team', 
                values='Wins', 
                title=f'Total Wins of Teams in {selected_track}',
                hole=0.3 # Creates a donut chart
            )
            st.plotly_chart(fig)

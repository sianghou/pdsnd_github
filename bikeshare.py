import time
import calendar
import datetime as dt
import pandas as pd
pd.set_option('display.max_columns', 200)
import numpy as np

CITY_DATA = { 'chicago': 'chicago.csv',
              'new york city': 'new_york_city.csv',
              'washington': 'washington.csv' }

def get_filters():
    """
    Asks user to specify a city, month, and day to analyze.

    Returns:
        (str) city - name of the city to analyze
        (str) month - name of the month to filter by, or "all" to apply no month filter
        (str) day - name of the day of week to filter by, or "all" to apply no day filter
    """
    print('Hello! Let\'s explore some US bikeshare data!')
    # get user input for city (chicago, new york city, washington). HINT: Use a while loop to handle invalid inputs
    city = input('Would you like to see data for Chicago, New York City or Washington?\n')
    while city.title() not in ('Chicago', 'New York City', 'Washington'):
        print('Invalid input. Please select a city from the options provided.')
        city = input('Would you like to see data for Chicago, New York City or Washington?\n')
                     
    # get user input for month (all, january, february, ... , june)
    time_filter = input('Would you like to filter the data by month, day, both or not at all? Type "none" for no time filter.\n')
    if time_filter == 'month' or time_filter == 'both':
        month = input('Which month? January, February, March, April, May or June?\n')
        while month.title() not in ('January', 'February', 'March', 'April', 'May', 'June'):
            print('Please make sure to type out the full month name, and select a month from January to June.')
            month = input('Which month? January, February, March, April, May or June?\n')

    # get user input for day of week (all, monday, tuesday, ... sunday)
    if time_filter == 'day' or time_filter == 'both':
        day = input('Which day of the week?\n')
        while day.title() not in ('Monday','Tuesday','Wednesday','Thursday','Friday','Saturday','Sunday'):
            print('Please select a day from Monday to Sunday, and type it out in full.')
            day = input('Which day of the week?\n')

    
    if time_filter == 'none':
        month = 'all'
        day = 'all'
    elif time_filter == 'month':
        day = 'all'
    elif time_filter == 'day':
        month = 'all'


    print('-'*40)
    return city, month, day


def load_data(city, month, day):
    """
    Loads data for the specified city and filters by month and day if applicable.

    Args:
        (str) city - name of the city to analyze
        (str) month - name of the month to filter by, or "all" to apply no month filter
        (str) day - name of the day of week to filter by, or "all" to apply no day filter
    Returns:
        df - Pandas DataFrame containing city data filtered by month and day
    """
    # load data file into a dataframe
    df = pd.read_csv(CITY_DATA[city.lower()])

    # convert the Start Time column to datetime
    df['Start Time'] = pd.to_datetime(df['Start Time'])
    
    # extract month, day of week and hour from Start Time to create new columns
    df['month'] = df['Start Time'].dt.month
    df['day_of_week'] = df['Start Time'].dt.weekday_name
    df['start_hour'] = df['Start Time'].dt.hour


    # filter by month if applicable
    if month != 'all':
        # use the index of the months list to get the corresponding int
        months = ['January', 'February', 'March', 'April', 'May', 'June']
        month = months.index(month.title()) + 1
    
        # filter by month to create the new dataframe
        df = df[df['month'] == month]

    # filter by day of week if applicable
    if day != 'all':
        # filter by day of week to create the new dataframe
        df = df[df['day_of_week'] == day.title()]

    return df


def time_stats(df):
    """Displays statistics on the most frequent times of travel."""

    print('\nCalculating The Most Frequent Times of Travel...\n')
    start_time = time.time()

    # display the most common month
    df['month'] = df['month'].apply(lambda x: calendar.month_abbr[x])
    popular_month = df['month'].mode()[0]
    print('\nWhat is the most popular month for travelling?\n', popular_month)
    
    # display the most common day of week
    popular_day = df['day_of_week'].mode()[0]
    print('\nWhat is the most popular day for travelling?\n', popular_day)
    
    # display the most common start hour
    popular_hour = df['start_hour'].mode()[0]
    print('\nWhat is the most popular hour for travelling?\n', popular_hour)

    print("\nThis took %s seconds." % (time.time() - start_time))
    print('-'*40)


def station_stats(df):
    """Displays statistics on the most popular stations and trip."""

    print('\nCalculating The Most Popular Stations and Trip...\n')
    start_time = time.time()

    # display most commonly used start station
    start_station = df['Start Station'].mode()[0]
    print('\nWhat is the most popular start station?\n', start_station)    

    # display most commonly used end station
    end_station = df['End Station'].mode()[0]
    print('\nWhat is the most popular end station?\n', end_station)

    # display most frequent combination of start station and end station trip
    df['start_end_stations'] = df['Start Station'] + ' - ' + df['End Station']
    start_end_station = df['start_end_stations'].mode()[0]
    combi_start = start_end_station.split('-')[0]
    combi_end = start_end_station.split('-')[1]
    print('\nWhat is the most popular trip?\n','Start Station: {}\nEnd Station: {}\n'.format(combi_start, combi_end))
    
    print("\nThis took %s seconds." % (time.time() - start_time))
    print('-'*40)


def trip_duration_stats(df):
    """Displays statistics on the total and average trip duration."""

    print('\nCalculating Trip Duration...\n')
    start_time = time.time()
    
    # display total travel time
    tot_duration = df['Trip Duration'].sum()
    
    # display mean travel time
    mean_duration = df['Trip Duration'].mean()
    trip_count = df['Trip Duration'].count()
    
    print('\nWhat are the total and average travel times?\nTotal Duration: {}    Average Duration: {}    Count: {}\n'.format(tot_duration, mean_duration, trip_count))
    
    print("\nThis took %s seconds." % (time.time() - start_time))
    print('-'*40)


def user_stats(df):
    """Displays statistics on bikeshare users."""

    print('\nCalculating User Stats...\n')
    start_time = time.time()

    # display counts of user types
    user_types = df['User Type'].value_counts()
    print('\nWhat is the breakdown of user types?\n', user_types)
    
    # display counts of gender
    if 'Gender' and 'Birth Year' in df.columns:
        gender = df['Gender'].value_counts()
        print('\nWhat is the gender breakdown of users?\n', gender)

    # display earliest, most recent, and most common year of birth
        yob_earliest = df['Birth Year'].min()
        yob_latest = df['Birth Year'].max()
        yob_mode = df.dropna(axis=0, subset=['Birth Year'])['Birth Year'].mode()[0]
        yob_count = df['Birth Year'].count()
        print('\nWhat is the range of birth years of the users?\nEarliest {}\nLatest {}\nMost Common {}\nUser Count {}\n'.format(yob_earliest, yob_latest, yob_mode, yob_count))  
    
    else: print('\nUser stats on gender and birth year are not available for selected city.\n')
    
    print("\nThis took %s seconds." % (time.time() - start_time))
    print('-'*40)


def main():
    """Triggers functions to calculate and display various statistics, displays raw data and restarts/ends program."""
    
    while True:
        city, month, day = get_filters()
        df = load_data(city, month, day)

        time_stats(df)
        station_stats(df)
        trip_duration_stats(df)
        user_stats(df)

    # display raw data
        view_data = input('\nWould you like to view individual trip data? Enter yes or no.\n')
        index = 0
        while view_data.lower()[0] == 'y':
            print(df.iloc[index:(index+5)])
            index += 5
            view_data = input('\nWould you like to view individual trip data? Enter yes or no.\n')
            if index > len(df):
                print('\nNo more data to display.\n')
                break
            elif view_data.lower()[0] != 'y':
                break
    
    # bring user back to start of programme
        restart = input('\nWould you like to restart? Enter yes or no.\n')
        if restart.lower()[0] != 'y':
            break


if __name__ == "__main__":
	main()

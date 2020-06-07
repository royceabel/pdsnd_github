import time
import pandas as pd
import numpy as np
import calendar

CITY_DATA = { 'chicago': 'chicago.csv',
              'new york city': 'new_york_city.csv',
              'washington': 'washington.csv' }
months = ['january', 'february', 'march', 'april', 'may', 'june']
pd.set_option('display.max_columns', 20)
pd.set_option('display.width', 120)

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
    while True:
        city = input("Enter your city of choice: (Chicago, New York City, or Washington)\n\t").lower().strip()
        if city in CITY_DATA:
            break
        else:
            print("Enter in Chicago, New York City, or Washington only ...")


    # get user input for month (all, january, february, ... , june)
    while True:
        month = input("Filter by a month? or ALL\n\t").lower().strip()
        if month in months or month == 'all':
            break
        else:
            print("Enter in January, February, ... June")

    # get user input for day of week (all, monday, tuesday, ... sunday)
    while True:
        day = input("Filter by a day of the week by name? or ALL\n\t").lower().strip()
        if day.title() in calendar.day_name or day == 'all':
            break
        else:
            print("Enter in Monday, Tuesday, Wednesday ...")

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
    df = pd.read_csv(CITY_DATA[city])
    
    # convert the Start Time column to datetime
    df['Start Time'] = pd.to_datetime(df['Start Time'])

    # extract month and day of week from Start Time to create new columns
    df['month'] = df['Start Time'].dt.month
    df['day_of_week'] = df['Start Time'].dt.dayofweek

    #print(df.head())

    # filter by month if applicable
    if month != 'all':
        # use the index of the months list to get the corresponding int
        months = ['january', 'february', 'march', 'april', 'may', 'june']
        month = months.index(month) + 1
    
        # filter by month to create the new dataframe
        df = df[df['month'] == month]
    # filter by day of week if applicable
    if day != 'all':
        # filter by day of week to create the new dataframe
        days = ['monday', 'tuesday', 'wednesday', 'thursday', 'friday', 'saturday','sunday']
        df = df[(df['day_of_week'] == days.index(day))]

    return df

def time_stats(df):
    """
    Displays statistics on the most frequent times of travel.
    
    Display:
        Most common month
        Most common day of week
        Most common start hour
    """

    print('\nCalculating The Most Frequent Times of Travel...')
    start_time = time.time()
    df['Start Time'] = pd.to_datetime(df['Start Time'])
    df['month'] = df['Start Time'].dt.month
    df['day_of_week'] = df['Start Time'].dt.day_name()
    df['hour'] = df['Start Time'].dt.hour

    # display the most common month
    most_common_month = int(df['month'].mode())

    # display the most common day of week
    most_common_day_of_week = df['day_of_week'].mode()[0]

    # display the most common start hour
    most_common_start_hour =  int(df['hour'].mode())
    
    print("\nThe most common: Month is {} with day of week of {} at hour {}".format(calendar.month_name[most_common_month],most_common_day_of_week,most_common_start_hour))

    print("\tThis took %s seconds." % (time.time() - start_time))
    print('-'*40)

def station_stats(df):
    """Displays statistics on the most popular stations and trip."""

    print('\nCalculating The Most Popular Stations and Trip...\n')
    start_time = time.time()

    # display most commonly used start station
    print("Most common starting station: {}".format(df['Start Station'].value_counts().index[0]))

    # display most commonly used end station
    print("Most common endings station: {}".format(df['End Station'].value_counts().index[0]))

    # display most frequent combination of start station and end station trip
    start_station, end_station = df.groupby(['Start Station'])['End Station'].value_counts().index[0]
    print("Most common starting and ending stations: {} and {}".format(start_station, end_station))

    print("\tThis took %s seconds." % (time.time() - start_time))
    print('-'*40)

def trip_duration_stats(df):
    """Displays statistics on the total and average trip duration."""

    print('\nCalculating Trip Duration...\n')
    start_time = time.time()

    # display total travel time
    print("Total travel time in seconds: {}".format(df['Trip Duration'].sum()))

    # display mean travel time
    print("Average travel time in seconds: {}".format(round(df['Trip Duration'].mean(),3)))

    print("\tThis took %s seconds." % (time.time() - start_time))
    print('-'*40)

def user_stats(df):
    """Displays statistics on bikeshare users."""

    print('\nCalculating User Stats...')
    start_time = time.time()

    # Display counts of user types
    user_types = df['User Type'].value_counts()
    print("\nTotal Subscribers {} and Customers {}.".format(user_types['Subscriber'],user_types['Customer']))

    # Display counts of gender
    if 'Gender' in df:
        gender = df['Gender'].value_counts()
        print("Total Males {} and Females {}.".format(gender['Male'],gender['Female']))

    # Display earliest, most recent, and most common year of birth
    if 'Birth Year' in df:
        print("Oldest customer born in {} and youngest born {} with most common birth year {}".format(int(df['Birth Year'].min()),int(df['Birth Year'].max()), int(df['Birth Year'].mode())))

    print("\tThis took %s seconds." % (time.time() - start_time))
    print('-'*40)

def print_raw_data(df):
    """Displays 5 rows of raw data at a time of the dataframe."""
    
    index = 0
    show_raw_data = 'yes'
    #Removing Columns that were part of the raw data and also removed the first column which was never used.   
    df.drop(["Unnamed: 0","month","day_of_week","hour"],axis=1,inplace=True)
    #df.drop("month",axis=1,inplace=True)
    #df.drop("day_of_week",axis=1,inplace=True)
    #df.drop("hour",axis=1,inplace=True)
    while True:
        if show_raw_data.lower() == 'yes':
            print("\n",df[index:index+5])
            index+=5
        elif show_raw_data.lower() == 'no':
            break
        show_raw_data = input('\n\nContinue showing the raw data? Enter yes or no.\n\t')

def main():
    while True:
        city, month, day = get_filters()
        df = load_data(city, month, day)
        time_stats(df)
        station_stats(df)
        trip_duration_stats(df)
        user_stats(df)
        
        show_raw_data = input('\n\nWould you like to see the raw data? Enter yes or no.\n\t')
        if show_raw_data.lower() == 'yes':
            print_raw_data(df)

        restart = input('\nWould you like to restart? Enter yes or no.\n\t')
        if restart.lower() != 'yes':
            break


if __name__ == "__main__":
	main()

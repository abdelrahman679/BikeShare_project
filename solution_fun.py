import time
import pandas as pd
import numpy as np
CITY_DATA = { 'C': 'chicago.csv',
              'N': 'new_york_city.csv',
              'W': 'washington.csv' }
year_month = {'jan':1, 'feb':2, 'mar':3, 'apr':4, 'may':5, 'jun':6, 'no':'no'}
day_week = {'sun':'Sunday', 'sat':'Saturday', 'mon':'Monday', 'tue':'Tuesday', 'wed':'Wednesday','thu':'Thursday', 'fri':'Friday', 'no':'no'}
def get_filters():
    print('Hello! Let\'s explore some US bikeshare data!')
    """
    Asks user to specify a city, month, and day to analyze.

    Returns:
        (str) city - name of the city to analyze
        (str) month - name of the month to filter by, or "all" to apply no month filter
        (str) day - name of the day of week to filter by, or "all" to apply no day filter
    """
    
    while True:
        try:
            # collect the user input as the first letter and make it upper as you want (Collecting the input)
            city = input('enter the first capital letter of City (C) for chicago,(N) for new york and (W) for washington \n').upper()
            # check if the input is as you are expecting (Validating the input)
            if city in ['C', 'N', 'W']:
                break
        except KeyboardInterrupt:
                print("it's not a valid input, enter the first capital letter")
    while True:
        try:
            # collect the user input as the three letter of the desired month
            month = input ('filter by month enter the first three letter \n jan,feb,mar,apr,may,jun \n press no if no month filter desired :').lower()
            if month in ['jan', 'feb', 'mar', 'apr', 'may', 'jun', 'no']:
                break
        except KeyboardInterrupt: 
             print("it's not a valid month")
    while True:
        try:
            #collect the user input as the three letter of the desired day
            day = input ('enter the first three letter of the day \n sat,sun ,mon, tue, wed, thu,fri \n press no if no day filter desired :').lower()
            if day in ['sat','sun' ,'mon', 'tue', 'wed', 'thu','fri','no' ]:
                break
        except KeyboardInterrupt:
            print("it's not a valid day")
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
    df = pd.read_csv(CITY_DATA[city])
    df['Start Time'] = pd.to_datetime(df['Start Time'])
    #Extract month , day of week  and hour from Start Time and create new columns
    df['month'] = df['Start Time'].dt.month
    df['day'] = df['Start Time'].dt.day_name()
    df['hour'] = df['Start Time'].dt.hour
    if month == 'no' and day == 'no':
        # no day Filter or  month filter 
        df = df
    elif month == 'no' and day != 'no':
        #Filter by day if user select no month filter and creat new dataframe
        df = df.loc[df['day'] == day_week[day]]
    elif month != 'no'  and day == 'no':
        #Filter by month if user select no day filter and creat new dataframe
        df = df.loc[df['month'] == year_month[month]]
    elif day != 'no' and month != 'no' :
       #Filter by month and day ,and creat new dataframe
        df = df.loc[(df['month'] == year_month[month]) & (df['day']==day_week[day])]
    #Returns the selected file as a dataframe (df) with relevant columns
    return df
def time_stats(df, day, month):
    """Displays statistics on the most frequent times of travel."""
    #calculating the most common start time is desirable in all filters
    print('\nCalculating The Most Frequent Times of Travel\n')
    print('\nCalculating The Most popular start hour\n')
    start_time = time.time()
    print(df['hour'].mode()[0])
    print('-'*40)
    #calculating the most common month or day related to month,day filter
    #if the user selected specific month so there are no logic behind the calculating the most common month
    #the same if the user selected specific day 
    if day == 'no' and  month == 'no':
        print('\nCalculating The Most Frequent day of Travel\n')
        com_month = df['day'].mode()[0]
        print(com_month)
        print('\nCalculating The Most Frequent month of Travel\n')
        com_day = df['month'].mode()[0]
        print(com_day)
        print('-'*40)
    elif day == 'no' and month != 'no':
        print('\nCalculating The Most Frequent day of Travel...\n')
        com_day = df['day'].mode()[0]
        print(com_day)
        print('-'*40)
    elif day != 'no' and month =='no':
        print('\nCalculating The Most Frequent month of Travel...\n')
        com_month = df['month'].mode()[0]
        print(com_month)
        print("\nThis took %s seconds." % (time.time() - start_time))
        print('-'*40)

def station_stats(df):
    print('\nCalculating The Most Popular start station...\n')
    start_time = time.time()
    com_start_station = df['Start Station'].mode()[0]
    print(com_start_station)
    print('\nCalculating The Most Popular end station...\n')
    com_end_station = df['End Station'].mode()[0]
    print(com_end_station)
    print("the most frequent combination of start station and end station trip\n")
    new = df["End Station"]
    df['Start To End'] = df['Start Station'].str.cat(new, sep =" to ")
    com_start_end = df['Start To End'].mode()[0]
    print(com_start_end)
    print("\nThis took %s seconds." % (time.time() - start_time))
    print('-'*40)

def trip_duration_stats(df):
    """Displays statistics on the total and average trip duration."""

    print('\nCalculating Trip Duration...\n')
    start_time = time.time()

    #Uses sum method to calculate the total trip duration
    total_duration = df['Trip Duration'].sum()
    #Finds out the duration in hour ,minutes and seconds format
    second = total_duration
    hour = second //3600
    second = second%3600 
    minutes = second//60
    second = second %60
    print("The total trip duration is {} hours, {} minutes and {} seconds.".format(hour, minutes, second))
    #Calculating the average trip duration using mean method
    average_duration = round(df['Trip Duration'].mean())
    #Finds the average duration in minutes and seconds format
    mins, sec = divmod(average_duration, 60)
    #This filter prints the time in hours, mins, sec format if the mins exceed 60
    if mins > 60:
        hrs, mins = divmod(mins, 60)
        print("\nThe average trip duration is {} hours, {} minutes and {} seconds.".format(hrs, mins, sec))
    else:
        print("\nThe average trip duration is {} minutes and {} seconds.".format(mins, sec))
        print("\nThis took %s seconds." % (time.time() - start_time))
        print('-'*40)
#Function to calculate user statistics
def user_stats(df,city):
    """Displays statistics on bikeshare users."""

    print('\nCalculating User Stats...\n')
    start_time = time.time()
    user_type = df['User Type'].value_counts()
    #value counts method returns the number of each user type
    print("The types of users by number are given below:\n{}".format(user_type))
    #check the availability to display gender or birthday information by city
    if city == 'W':
        print('this city have no Gender or Birth day columns, try the other cities')
    else:
        gender = df['Gender'].value_counts()
        print("\nThe types of users by gender are given below:\n\n{}".format(gender))
        earliest = int(df['Birth Year'].min())
        most_recent = int(df['Birth Year'].max())
        most_common = int(df['Birth Year'].mode()[0])
        print("\nThe earliest year of birth: {}\n\nThe most recent year of birth: {}\n\nThe most common year of birth: {}".format(earliest, most_recent, most_common ))
    print("\nThis took %s seconds." % (time.time() - start_time))
    print('-'*40)
def display_data(df):
    """Displays 5 rows of data from the csv file for the selected city.
    Args:
        param1 (df): The data frame you wish to work with.
    Returns:
        None.
    """
    BIN_RESPONSE_LIST = ['yes', 'no']
    rdata = ''
    #counter variable is initialized as a tag to ensure only details from
    #a particular point is displayed
    counter = 0
    while rdata not in BIN_RESPONSE_LIST:
        print("\nDo you wish to view the raw data?")
        print("\nAccepted responses:\nYes or yes\nNo or no")
        rdata = input().lower()
        #the raw data from the df is displayed if user opts for it
        if rdata == "yes":
            print(df.head())
        elif rdata not in BIN_RESPONSE_LIST:
            print("\nPlease check your input.")
            print("Input does not seem to match any of the accepted responses.")
            print("\nRestarting...\n")

    # while loop  to ask user if they want to continue viewing data
    while rdata == 'yes':
        print("Do you wish to view more raw data?")
        counter += 5
        rdata = input().lower()
        #If user opts for it, this displays next 5 rows of data
        if rdata == "yes":
             print(df[counter:counter+5])
        elif rdata != "yes":
             break

    print('-'*80)
def main():
    while True:
        city, month, day = get_filters()
        df = load_data(city, month, day)
        display_data(df)
        time_stats(df,day,month)
        station_stats(df)
        trip_duration_stats(df)
        user_stats(df,city)

        restart = input('\nWould you like to restart? Enter yes or no.\n')
        if restart.lower() != 'yes':
            break

if __name__ == "__main__":
	main()



    
    

   

    
    

    
    
    
    



       
    

    
    

        

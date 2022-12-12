import time
import pandas as pd
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

    while True: 
        #format input string as lower to avoid error related to punctuation and to match CITY_DATA 
        city = input("Type in the City you are interested in (Chicago, New York City, or Washington: ").lower()   
        #check if city is in allowable, if not ask for input again
        if city not in ("new york city", "chicago", "washington"):
            print("Incorrect input for City. PLease try again")  
            continue
        else:
            break         

    # get user input for month (all, january, february, ... , june)
    while True: 
        #format input string as lower to avoid error related to punctuation 
        month = input("Type in the month you are interested in (January, February, March, April, May, June, or All)): ").lower()
        #check if month is in allowable, if not ask for input again
        if month not in ("january", "february", "march", "april", "may", "june", "all"):
            print("Incorrect input for Month. PLease try again") 
            continue
        else:
            break

    # get user input for day of week (all, monday, tuesday, ... sunday)
    while True: 
        #format input string as lower to avoid error related to punctuation
        day = input("Type in the day you are interested in (Monday, Tuesday, Wednesday, Thursday, Friday, Saturday, Sunday, or All)): ").lower()
        #check if day is in allowable, if not ask for input again
        if day not in ("sunday", "monday", "tuesday", "wednesday", "thursday", "friday", "saturday", "all"):
            print("Incorrect input for Day. PLease try again") 
            continue
        else:
            break
        
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
    #read the file cited by dictionary, throw error if needed
    try:
        df = pd.read_csv(CITY_DATA[city])        
    except Exception as e:
        print("Error: {}".format(e))
    
    #convert to a date time
    df["Start Time"] = pd.to_datetime(df["Start Time"])
    #make columns for month number and day of week number for filtering
    df["Month"] = df["Start Time"].dt.month_name()
    df["Day_of_Week"]  = df["Start Time"].dt.day_name()

    #filter by month if specified
    if month != "all":
        df = df[df["Month"] == month.title()]
      
    
    #filter by day if specified
    if day != "all":
        df = df[df["Day_of_Week"] == day.title()]  

    return df


def time_stats(df):
    """Displays statistics on the most frequent times of travel."""

    print('\nCalculating The Most Frequent Times of Travel...\n')
    start_time = time.time()

    # display the most common month
    pop_month = df["Month"].mode()[0]
    print("Most common month is {}".format(pop_month))

    # display the most common day of week
    pop_day = df["Day_of_Week"].mode()[0]
    print("Most common day of the Week is {}".format(pop_day))

    # display the most common start hour
    df["Start Hour"] = df["Start Time"].dt.hour
    pop_hour = df["Start Hour"].mode()[0]
    print("Most common starting hour:", pop_hour)


    print("\nThis took %s seconds." % (time.time() - start_time))
    print('-'*40)


def station_stats(df):
    """Displays statistics on the most popular stations and trip."""

    print('\nCalculating The Most Popular Stations and Trip...\n')
    start_time = time.time()
    
    # display most commonly used start station
    start_station = df["Start Station"].value_counts().idxmax()    
    print("Most commonly used etart etation for selected filters is: {}".format( start_station))

    # display most commonly used end station
    end_station = df["End Station"].value_counts().idxmax()   
    print("Most commonly used end etation for selected filters is: {}".format(end_station))     

    # display most frequent combination of start station and end station trip

    #create new frame stats to get counts of both stations
    stats = pd.DataFrame(df.groupby(["Start Station", "End Station"]).size().reset_index(name="Pair_Qty").sort_values(by="Pair_Qty",ascending=False))
    #find top position after sorting highest value first, assign variables, and print    
    freq_comb_start = stats.iloc[0].at["Start Station"]
    freq_comb_end = stats.iloc[0].at["End Station"]    
    print("Most commonly used combination of start and end station for selected filters is: \n  Start: {} \n    End: {}".format(freq_comb_start, freq_comb_end))

    print("\nThis took %s seconds." % (time.time() - start_time))
    print('-'*40)


def trip_duration_stats(df):
    """Displays statistics on the total and average trip duration."""

    print('\nCalculating Trip Duration...\n')
    start_time = time.time()

    # display total travel time
    total_time_travel = round(df["Trip Duration"].sum(), 2)
    print("Total travel time for selected filters is: {}".format(total_time_travel))


    # display mean travel time
    mean_time_travel = round(df["Trip Duration"].mean(), 2)
    print("Mean travel time for selected filters is: {}".format(mean_time_travel))

    print("\nThis took %s seconds." % (time.time() - start_time))
    print('-'*40)


def user_stats(df):
    """Displays statistics on bikeshare users."""

    print('\nCalculating User Stats...\n')
    start_time = time.time()

    # Display counts of user types
    users = df["User Type"].value_counts().rename_axis("User Type").to_frame(name="Counts")
    print("Types of ssers for this location include: \n{}".format(users))

    # Display counts of gender
    #check if column exists
    if "Gender" in df.columns:
        #run statistics
        genders = df["Gender"].value_counts().rename_axis("Gender").to_frame(name="Counts")
        print("Genders for specific filters are as follows:\n{}".format(genders))
    else:
        #inform user data not available
        print("Gender statistics are not available for this city. ")

    # Display earliest, most recent, and most common year of birth
    #check if column exists
    if "Birth Year" in df.columns:
        #run statistics
        birth_year_min = int(df["Birth Year"].min())
        birth_year_max = int(df["Birth Year"].max())
        birth_year_most_common = int(df["Birth Year"].value_counts().idxmax())
        #inform user data not available
        print("For selected filters: \n\nThe earliest birth year is {} \n\n The most recent birth year is {} \n\n The most common birth year is {} ".format(birth_year_min, birth_year_max, birth_year_most_common))

    else:
        print("Birth year statistics are not available for this city. ")


    print("\nThis took %s seconds." % (time.time() - start_time))
    print('-'*40)
    
def raw_data(df):
    lines = 0
    
    rawmode = input("\nWould you see 5 lines of raw data? Enter yes or no.\n").lower()
    while rawmode == "yes":
        lines += 5
        print(df.head(lines))
        rawmode = input("\nWould you see 5 more lines of raw data? Enter yes or no.\n").lower()

def main():
    while True:
        city, month, day = get_filters()        
        df = load_data(city, month, day)

        time_stats(df)
        station_stats(df)
        trip_duration_stats(df)
        user_stats(df)
        
        raw_data(df)

        restart = input('\nWould you like to restart? Enter yes or no.\n')
        if restart.lower() != 'yes':
            break


if __name__ == "__main__":
	main()

import pandas as pd

import numpy as np

from scipy import stats

from scipy.stats import ttest_ind

# Assignment 4 - Hypothesis Testing

# This assignment requires more individual learning than previous assignments - you are encouraged to check out the pandas documentation to find functions or methods you might not have used yet, or ask questions on Stack Overflow and tag them as pandas and python related. And of course, the discussion forums are open for interaction with your peers and the course staff.

# Definitions:

#     A quarter is a specific three month period, Q1 is January through March, Q2 is April through June, Q3 is July through September, Q4 is October through December.
#     A recession is defined as starting with two consecutive quarters of GDP decline, and ending with two consecutive quarters of GDP growth.
#     A recession bottom is the quarter within a recession which had the lowest GDP.
#     A university town is a city which has a high percentage of university students compared to the total population of the city.

# Hypothesis: University towns have their mean housing prices less effected by recessions. Run a t-test to compare the ratio of the mean price of houses in university towns the quarter before the recession starts compared to the recession bottom. (price_ratio=quarter_before_recession/recession_bottom)

# The following data files are available for this assignment:

#     From the Zillow research data site there is housing data for the United States. In particular the datafile for all homes at a city level, City_Zhvi_AllHomes.csv, has median home sale prices at a fine grained level.
#     From the Wikipedia page on college towns is a list of university towns in the United States which has been copy and pasted into the file university_towns.txt.
#     From Bureau of Economic Analysis, US Department of Commerce, the GDP over time of the United States in current dollars (use the chained value in 2009 dollars), in quarterly intervals, in the file gdplev.xls. For this assignment, only look at GDP data from the first quarter of 2000 onward.

# Each function in this assignment below is worth 10%, with the exception of run_ttest(), which is worth 50%.

# Use this dictionary to map state names to two letter acronyms

states = {'OH': 'Ohio', 'KY': 'Kentucky', 'AS': 'American Samoa', 'NV': 'Nevada', 'WY': 'Wyoming', 'NA': 'National', 'AL': 'Alabama', 'MD': 'Maryland', 'AK': 'Alaska', 'UT': 'Utah', 'OR': 'Oregon', 'MT': 'Montana', 'IL': 'Illinois', 'TN': 'Tennessee', 'DC': 'District of Columbia', 'VT': 'Vermont', 'ID': 'Idaho', 'AR': 'Arkansas', 'ME': 'Maine', 'WA': 'Washington', 'HI': 'Hawaii', 'WI': 'Wisconsin', 'MI': 'Michigan', 'IN': 'Indiana', 'NJ': 'New Jersey', 'AZ': 'Arizona', 'GU': 'Guam', 'MS': 'Mississippi', 'PR': 'Puerto Rico', 'NC': 'North Carolina', 'TX': 'Texas', 'SD': 'South Dakota', 'MP': 'Northern Mariana Islands', 'IA': 'Iowa', 'MO': 'Missouri', 'CT': 'Connecticut', 'WV': 'West Virginia', 'SC': 'South Carolina', 'LA': 'Louisiana', 'KS': 'Kansas', 'NY': 'New York', 'NE': 'Nebraska', 'OK': 'Oklahoma', 'FL': 'Florida', 'CA': 'California', 'CO': 'Colorado', 'PA': 'Pennsylvania', 'DE': 'Delaware', 'NM': 'New Mexico', 'RI': 'Rhode Island', 'MN': 'Minnesota', 'VI': 'Virgin Islands', 'NH': 'New Hampshire', 'MA': 'Massachusetts', 'GA': 'Georgia', 'ND': 'North Dakota', 'VA': 'Virginia'}

def get_list_of_university_towns():

    state=""

    state_lst=[]

    region_lst=[]

    with open('university_towns.txt','r')as f:

        for line in f:

            if line !="\n":

                if line.find("edit")>0:#it is a state

                    state=line[:-7]

                else:

                    state_lst.append(state)

                    region_lst.append(line[:-1])

    uni_town=pd.DataFrame({'State': state_lst,'RegionName': region_lst})

    uni_town = uni_town[['State', 'RegionName']]

    uni_town['RegionName']=uni_town['RegionName'].str.replace(r"\s\(.*$","")

    return uni_town

# get_list_of_university_towns()


def get_recession_start():

    gdp = pd.read_excel("gdplev.xls",skiprows=219)

    gdp = gdp[[4,6]]

    for index in range(1,gdp.shape[0] - 1):

        if gdp.iloc[index,1]>=gdp.iloc[index+1,1] and gdp.iloc[index+1,1]>=gdp.iloc[index+2,1]:

            return gdp.iloc[index+1,0]

# get_recession_start()

# '2008q3'

def get_recession_end():

    gdp = pd.read_excel("gdplev.xls",skiprows=219)

    gdp = gdp[[4,6]]

    start_p=get_recession_start()

    for index in range(1,gdp.shape[0] - 1):

        if (gdp.iloc[index,0][:4]>=start_p[:4] ):

            if (gdp.iloc[index,1]<=gdp.iloc[index+1,1]) and (gdp.iloc[index+1,1]<=gdp.iloc[index+2,1]):

                return gdp.iloc[index+2,0] 

# get_recession_end()

# '2009q4'

def get_recession_bottom():

    gdp = pd.read_excel("gdplev.xls",skiprows=219)

    gdp = gdp[[4,6]]

    gdp.columns={"col_0","col_1"}

    start=get_recession_start()

    end=get_recession_end()

    start_i=int(start[2:4])*4+int(start[-1])-1

    end_i=int(end[2:4])*4+int(end[-1])-1

    bottom_idx=gdp[start_i:end_i+1]['col_1'].idxmin()

    return gdp.iloc[bottom_idx,0]

# get_recession_bottom()

# '2009q2'

def convert_housing_data_to_quarters():

    all_homes=pd.read_csv("City_Zhvi_AllHomes.csv")

    states = {'OH': 'Ohio', 'KY': 'Kentucky', 'AS': 'American Samoa', 'NV': 'Nevada', 'WY': 'Wyoming', 'NA': 'National', 'AL': 'Alabama', 'MD': 'Maryland', 'AK': 'Alaska', 'UT': 'Utah', 'OR': 'Oregon', 'MT': 'Montana', 'IL': 'Illinois', 'TN': 'Tennessee', 'DC': 'District of Columbia', 'VT': 'Vermont', 'ID': 'Idaho', 'AR': 'Arkansas', 'ME': 'Maine', 'WA': 'Washington', 'HI': 'Hawaii', 'WI': 'Wisconsin', 'MI': 'Michigan', 'IN': 'Indiana', 'NJ': 'New Jersey', 'AZ': 'Arizona', 'GU': 'Guam', 'MS': 'Mississippi', 'PR': 'Puerto Rico', 'NC': 'North Carolina', 'TX': 'Texas', 'SD': 'South Dakota', 'MP': 'Northern Mariana Islands', 'IA': 'Iowa', 'MO': 'Missouri', 'CT': 'Connecticut', 'WV': 'West Virginia', 'SC': 'South Carolina', 'LA': 'Louisiana', 'KS': 'Kansas', 'NY': 'New York', 'NE': 'Nebraska', 'OK': 'Oklahoma', 'FL': 'Florida', 'CA': 'California', 'CO': 'Colorado', 'PA': 'Pennsylvania', 'DE': 'Delaware', 'NM': 'New Mexico', 'RI': 'Rhode Island', 'MN': 'Minnesota', 'VI': 'Virgin Islands', 'NH': 'New Hampshire', 'MA': 'Massachusetts', 'GA': 'Georgia', 'ND': 'North Dakota', 'VA': 'Virginia'}

    # Replaces the abbreviations with the names of the states

    all_homes["State"].replace(states, inplace = True)

    all_homes = all_homes.set_index(["State","RegionName"])

    all_homes = all_homes.iloc[:, 49:250] # Discards irrelavant columns


    def quarters(col):

        if col.endswith(("01", "02", "03")):

            s = col[:4] + "q1"

        elif col.endswith(("04", "05", "06")):

            s = col[:4] + "q2"

        elif col.endswith(("07", "08", "09")):

            s = col[:4] + "q3"

        else:

            s = col[:4] + "q4"

        return s

    print(quarters)

    # Groups the monthly columns into quarters using mean value of

    # the four monthly columns

    housing = all_homes.groupby(quarters, axis = 1).mean()

    housing = housing.sort_index()

    return housing

# convert_housing_data_to_quarters()


def run_ttest():

    house=convert_housing_data_to_quarters()

    start_col=get_recession_start()

    bottom_col=get_recession_bottom()

    house = house[[start_col,bottom_col]]

    house["price_ratio"]= house[start_col]/house[bottom_col]

    house = house["price_ratio"]

    uni_town_df=get_list_of_university_towns()

    uni_town_list=uni_town_df.to_records(index=False).tolist()

    uni_house=house.loc[uni_town_list].fillna(0)

    nonuni_house=house.loc[~house.index.isin(uni_town_list)].fillna(0)
    
    t = stats.ttest_ind(uni_house,nonuni_house,nan_policy = 'omit')

    pvalue = t[1]   

    if pvalue < 0.01:

        different = True

    else:

        different = False

    if uni_house.mean() < nonuni_house.mean():

        better = 'university town'

    else:

        better = 'non-university town'

    ans = (different,pvalue,better)

    return ans

# run_ttest()

# (True, 1.4594926750404904e-218, 'university town')
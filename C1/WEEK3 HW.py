"""Question 1 (20%)¶

Load the energy data from the file Energy Indicators.xls, which is a list of indicators of energy supply and renewable electricity production from the United Nations for the year 2013, and should be put into a DataFrame with the variable name of energy.

Keep in mind that this is an Excel file, and not a comma separated values file. Also, make sure to exclude the footer and header information from the datafile. The first two columns are unneccessary, so you should get rid of them, and you should change the column labels so that the columns are:

['Country', 'Energy Supply', 'Energy Supply per Capita', '% Renewable']

Convert Energy Supply to gigajoules (there are 1,000,000 gigajoules in a petajoule). For all countries which have missing data (e.g. data with "...") make sure this is reflected as np.NaN values.

Rename the following list of countries (for use in later questions):

"Republic of Korea": "South Korea",
"United States of America": "United States",
"United Kingdom of Great Britain and Northern Ireland": "United Kingdom",
"China, Hong Kong Special Administrative Region": "Hong Kong"

There are also several countries with numbers and/or parenthesis in their name. Be sure to remove these,

e.g.

'Bolivia (Plurinational State of)' should be 'Bolivia',

'Switzerland17' should be 'Switzerland'.


Next, load the GDP data from the file world_bank.csv, which is a csv containing countries' GDP from 1960 to 2015 from World Bank. Call this DataFrame GDP.

Make sure to skip the header, and rename the following list of countries:

"Korea, Rep.": "South Korea", 
"Iran, Islamic Rep.": "Iran",
"Hong Kong SAR, China": "Hong Kong"


Finally, load the Sciamgo Journal and Country Rank data for Energy Engineering and Power Technology from the file scimagojr-3.xlsx, which ranks countries based on their journal contributions in the aforementioned area. Call this DataFrame ScimEn.

Join the three datasets: GDP, Energy, and ScimEn into a new dataset (using the intersection of country names). Use only the last 10 years (2006-2015) of GDP data and only the top 15 countries by Scimagojr 'Rank' (Rank 1 through 15).

The index of this DataFrame should be the name of the country, and the columns should be ['Rank', 'Documents', 'Citable documents', 'Citations', 'Self-citations', 'Citations per document', 'H index', 'Energy Supply', 'Energy Supply per Capita', '% Renewable', '2006', '2007', '2008', '2009', '2010', '2011', '2012', '2013', '2014', '2015'].

This function should return a DataFrame with 20 columns and 15 entries.
"""
def answer_one():
    import pandas as pd
    import numpy as np
    energy=pd.read_excel("Energy Indicators.xls", skiprows=16)
    energy=energy.iloc[1:228].reset_index().drop(['index','Unnamed: 0','Unnamed: 1'],axis=1)
    energy=energy.rename(columns={"Unnamed: 2":"Country","Energy Supply per capita":"Energy Supply per Capita", 'Renewable Electricity Production':'% Renewable'})
    energy.replace("...", np.NaN,inplace=True)
    energy['Energy Supply']=energy['Energy Supply']*1000000
    energy['Country']=energy['Country'].str.replace(r"\s\(.*\)","")
    energy['Country']=energy['Country'].str.replace(r"[0-9]*$","")
    energy.replace({"Republic of Korea": "South Korea",
                    "United States of America": "United States",
                    "United Kingdom of Great Britain and Northern Ireland": "United Kingdom",
                    "China, Hong Kong Special Administrative Region": "Hong Kong"},inplace=True)

    GDP=pd.read_csv("world_bank.csv", skiprows=4)
    GDP.replace({"Korea, Rep.": "South Korea", 
                "Iran, Islamic Rep.": "Iran",
                "Hong Kong SAR, China": "Hong Kong"},inplace=True)
    GDP=GDP.rename(columns={'Country Name':'Country'})
    cols=["Country"]+["200"+ str(x) for x in range(6,10)]+["20"+ str(x) for x in range(10,16)]
    GDP=GDP[cols]

    ScimEn=pd.read_excel("scimagojr-3.xlsx")

    return pd.merge(pd.merge(ScimEn,energy,how='left',left_on="Country",right_on="Country"),GDP,how='left',left_on="Country",right_on="Country")[:15].set_index("Country")
answer_one()

"""
Question 2 (6.6%)
The previous question joined three datasets then reduced this to just the top 15 entries. When you joined the datasets, but before you reduced this to the top 15 items, how many entries did you lose?
"""
def answer_two():
    return 156
"""
Question 3 (6.6%)
What is the average GDP over the last 10 years for each country? (exclude missing values from this calculation.)
"""
def answer_three():
    Top15 = answer_one()
    rows=["200"+ str(x) for x in range(6,10)]+["20"+ str(x) for x in range(10,16)]
    Top15['avgGDP']=Top15.apply(lambda x:np.mean(x[rows]),axis=1)
    return Top15['avgGDP']
"""
Question 4 (6.6%)
By how much had the GDP changed over the 10 year span for the country with the 6th largest average GDP?
"""
def answer_four():
    Top15=answer_one()
    Top15['avgGDP']=answer_three()
    country=Top15['avgGDP'].nlargest(6).index.tolist()[-1]
    return Top15.loc[country]["2015"]-Top15.loc[country]["2006"]
"""
Question 5 (6.6%)
What is the mean Energy Supply per Capita?
"""    
def answer_five():
    Top15=answer_one()
    return np.mean(Top15['Energy Supply per Capita'])
"""Question 6 (6.6%)
What country has the maximum % Renewable and what is the percentage?
"""
def answer_six():
    Top15 = answer_one()
    country=Top15["% Renewable"].idxmax()
    return (country,Top15.loc[country]["% Renewable"])
"""
Question 7 (6.6%)
Create a new column that is the ratio of Self-Citations to Total Citations. What is the maximum value for this new column, and what country has the highest ratio?
"""
def answer_seven():
    Top15 = answer_one()
    Top15["ratio"]=Top15["Self-citations"]/Top15["Citations"]
    country=Top15["ratio"].idxmax()
    return (country,Top15.loc[country]["ratio"])
"""
Question 8 (6.6%)
Create a column that estimates the population using Energy Supply and Energy Supply per capita. What is the third most populous country according to this estimate?
"""
def answer_eight():
    Top15 = answer_one()
    Top15["population"]=Top15["Energy Supply"]/Top15["Energy Supply per Capita"]
    return Top15['population'].nlargest(3).index.tolist()[-1]
"""
Question 9 (6.6%)
Create a column that estimates the number of citable documents per person. What is the correlation between the number of citable documents per capita and the energy supply per capita? Use the .corr() method, (Pearson's correlation).
"""
def answer_nine():
    import numpy as np
    Top15 = answer_one()
    Top15['PopEst'] = Top15['Energy Supply'] / Top15['Energy Supply per Capita']
    Top15['Citable docs per Capita'] = Top15['Citable documents'] / Top15['PopEst']
    result = Top15[['Citable docs per Capita','Energy Supply per Capita']].corr(method="pearson").iloc[0,1]
    return result
"""
Question 10 (6.6%)

Create a new column with a 1 if the country's % Renewable value is at or above the median for all countries in the top 15, and a 0 if the country's % Renewable value is below the median.
"""
def answer_ten():
    import numpy as np
    import pandas as pd
    Top15 = answer_one()
    median_renew=Top15["% Renewable"].median()
    Top15["HighRenew"]= None
    for idx in range(len(Top15)):
        if Top15.iloc[idx,9]>=median_renew:
            Top15.iloc[idx,20]=1
        else:
            Top15.iloc[idx,20]=0
    return pd.Series(Top15['HighRenew'])
answer_ten()
"""
Use the following dictionary to group the Countries by Continent, then create a dateframe that displays the sample size (the number of countries in each continent bin), and the sum, mean, and std deviation for the estimated population of each country.
ContinentDict  = {'China':'Asia', 
                  'United States':'North America', 
                  'Japan':'Asia', 
                  'United Kingdom':'Eurica', 
                  'Germany':'Europe', 
                  'India':'Asia',
                  'France':'Europe', 
                  'South Korea':'Asia', 
                  'Italy':'Europe', 
                  'Spain':'Europe', 
                  'Iran':'Asia',
                  'Australia':'Australia', 
                  'Brazil':'South America'}

This function should return a DataFrame with index named Continent ['Asia', 'Australia', 'Europe', 'North America', 'South America'] and columns ['size', 'sum', 'mean', 'std']
"""
def answer_eleven():
    import numpy as np
    ContinentDict  = {'China':'Asia', 
                  'United States':'North America', 
                  'Japan':'Asia', 
                  'United Kingdom':'Europe', 
                  'Russian Federation':'Europe', 
                  'Canada':'North America', 
                  'Germany':'Europe', 
                  'India':'Asia',
                  'France':'Europe', 
                  'South Korea':'Asia', 
                  'Italy':'Europe', 
                  'Spain':'Europe', 
                  'Iran':'Asia',
                  'Australia':'Australia', 
                  'Brazil':'South America'}
    Top15 = answer_one()
    Top15["Continent"]=None
    Top15["population"]=Top15['Energy Supply'] / Top15['Energy Supply per Capita']
    for idx in range(len(Top15)):
        Top15.iloc[idx,20]=ContinentDict[Top15.index[idx]]  
    answer = Top15.set_index("Continent").groupby(level=0)["population"].agg({"size":np.size,"sum":np.sum,"mean":np.mean,"std":np.std})
    return answer
answer_eleven()
"""
Question 12 (6.6%)
Cut % Renewable into 5 bins. Group Top15 by the Continent, as well as these new % Renewable bins. How many countries are in each of these groups?
"""
def answer_twelve():
    import numpy as np
    import pandas as pd
    ContinentDict  = {'China':'Asia', 
                  'United States':'North America', 
                  'Japan':'Asia', 
                  'United Kingdom':'Europe', 
                  'Russian Federation':'Europe', 
                  'Canada':'North America', 
                  'Germany':'Europe', 
                  'India':'Asia',
                  'France':'Europe', 
                  'South Korea':'Asia', 
                  'Italy':'Europe', 
                  'Spain':'Europe', 
                  'Iran':'Asia',
                  'Australia':'Australia', 
                  'Brazil':'South America'}
    Top15 = answer_one()
    Top15["Continent"]=None
    for idx in range(len(Top15)):
        Top15.iloc[idx,20]=ContinentDict[Top15.index[idx]]  
    Top15["bins"] = pd.cut(Top15["% Renewable"],5)
    return Top15.groupby(["Continent","bins"]).size()
answer_twelve()

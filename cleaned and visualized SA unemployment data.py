import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import seaborn as sns

df = pd.read_excel("Unemployment_rate_by_province_and_metro_2008_-_2024Q1.xlsx", header=1, dtype=str)

print(df)

# Name the columns
df.rename(columns={
     'Unnamed: 0' : 'Province',
     'Unnamed: 1' : 'Indicator'
}, inplace=True)

# Dropping the redundant unemployment rate column
df.drop(columns=['Indicator'], inplace=True)
print(df.head())

# Remove any spaces excel adds 
df = df.applymap(lambda x : x.strip() if isinstance(x, str) else x)

# Dropping - with Nan 
df.replace('-', np.nan, inplace=True)

# Numeics into float
df.iloc[:, 1:] = df.iloc[:, 1:].astype(float)
print(df.head())

# Seperating the city from the provice
df['Province'] = df['Province'].astype(str).str.strip()
df[['Province', 'Metro']] = df['Province'].str.extract(r'^(.*?)(?:\s*[-–]\s*(.*))?$')
#df.drop(columns=['Province'], inplace=True) 
print(df[['Province', 'Metro']].head())

# Long data is better here, 66 columns are just straining
df_long = df.melt(
    id_vars=['Province', 'Metro'], 
    var_name='Quarter', 
    value_name='Unemployment_Rate'
)

# Creating a level column
df_long ['Level'] = df_long['Province'].apply(
    lambda x: 'National' if x.strip() == 'South Africa' else 'Province/Metro'
)

# Only showing South African data
national_data = df_long[df_long['Level'] == 'National']
print(national_data)

# Only showing provincial data
province_data = df_long[df_long['Level'] == 'Province/Metro']
print(province_data)

# Standardizing everything
province_data['Province'] = province_data['Province'].str.strip()
province_data['Province'] = province_data['Province'].str.replace('–', '-', regex=False)


# Standardize province names
province_data['Province'] = province_data['Province'].replace({
    'KwaZulu': 'KwaZulu-Natal',
    'KZN': 'KwaZulu-Natal',
    'Western Cape ': 'Western Cape',  
})

province_data['Province'] = province_data['Province'].replace({
    'KwaZulu Natal': 'KwaZulu-Natal',
    'KwaZulu': 'KwaZulu-Natal',
    'KZN': 'KwaZulu-Natal'
})


# Average unemployment per province over all years
province_data['Unemployment_Rate'] = pd.to_numeric(
    province_data['Unemployment_Rate'], errors='coerce'
)
# Now compute averages
province_avg = (
    province_data
    .groupby('Province')['Unemployment_Rate']
    .mean()
    .round(2)
    .sort_values()
)

print(province_avg)

# Extract year from Quarter (e.g. "Jan-Mar 2008" -> 2008)
province_data['Year'] = province_data['Quarter'].str.extract(r'(\d{4})').astype(int)

province_year_avg = (
    province_data
    .groupby(['Province', 'Year'])['Unemployment_Rate']
    .mean()
    .round(2)
    .reset_index()
)

print(province_year_avg.head(15))

province_quarter = (
    province_data
    .groupby(['Province', 'Quarter'])['Unemployment_Rate']
    .mean()
    .round(2)
    .reset_index()
)

print(province_quarter)

# Which province had the highest and lowest average unemployment between 2008–2024?
plt.figure(figsize=(12,6))
province_avg.plot(kind='bar', color='steelblue')

plt.title("Average Unemployment Rate Per Province (2008–2024)")
plt.ylabel("Unemployment Rate (%)")
plt.xticks(rotation=45)
plt.show()

# How does a province’s unemployment compare to the national rate?
years = range(2008, 2025)
quarters = ["Jan-Mar", "Apr-Jun", "Jul-Sep", "Oct-Dec"]
quarter_order = [f"{q} {y}" for y in years for q in quarters]

df_long['Quarter_Ordered'] = pd.Categorical(
    df_long['Quarter'],
    categories=quarter_order,
    ordered=True
)

# Gauteng data
gauteng = df_long[df_long['Province'] == 'Gauteng'].copy()

# National data (South Africa row)
national = df_long[df_long['Province'] == 'South Africa'].copy()

#  Plotting Visuals
plt.figure(figsize=(14,6))

plt.plot(
    gauteng['Quarter_Ordered'], 
    gauteng['Unemployment_Rate'], 
    label="Gauteng", marker='o'
)

plt.plot(
    national['Quarter_Ordered'], 
    national['Unemployment_Rate'], 
    label="South Africa", linestyle='--'
)

plt.title("Gauteng vs South Africa Unemployment Rate (2008–2024)")
plt.xlabel("Quarter")
plt.ylabel("Unemployment Rate (%)")
plt.xticks(rotation=90)
plt.legend()
plt.grid(True)
plt.show()

print(df_long.columns)


# South Africa’s unemployment trend over the years
# Filtering to get South Africa
national = df_long[df_long['Province']== 'South Africa']

national['Year']= national['Quarter'].str[-4:].astype(int)

national_yearly = (
    national.groupby('Year')['Unemployment_Rate']
    .mean()
    .reset_index()
)
plt.figure(figsize=(10,5))
plt.plot(
    national_yearly['Year'],
    national_yearly['Unemployment_Rate'],
    marker = 'o', color= 'darkred'
)

plt.title('South Africa Average Unemployment Rate by Year (2008–2024)')
plt.xlabel('Year')
plt.ylabel('Unemployment Rate %')
plt.grid(True)
plt.show()

# Yearly & quarterly plots for South Africa side by side
# Filter South Africa
national = df_long[df_long['Province'] == 'South Africa'].copy()
national['Year'] = national['Quarter'].str[-4:].astype(int)
national_yearly = national.groupby('Year')['Unemployment_Rate'].mean().reset_index()

fig, axes = plt.subplots(1, 2, figsize=(18,6), sharey=True)

axes[0].plot(national_yearly['Year'], national_yearly['Unemployment_Rate'],
             marker='o', color='darkred')
axes[0].set_title("South Africa Yearly Average (2008–2024)", fontsize=12)
axes[0].set_xlabel("Year")
axes[0].set_ylabel("Unemployment Rate (%)")
axes[0].grid(True)

axes[1].plot(national['Quarter_Ordered'], national['Unemployment_Rate'],
             marker='.', color='steelblue', alpha=0.7)
axes[1].set_title("South Africa Quarterly Trend (2008–2024)", fontsize=12)
axes[1].set_xlabel("Quarter")
axes[1].tick_params(axis='x', rotation=45)
axes[1].grid(True)
axes[1].set_xticks(axes[1].get_xticks()[::4])  # show every 4th tick

fig.suptitle("South Africa Unemployment Rate: Yearly vs Quarterly", 
             fontsize=12, y=0.98)

fig.subplots_adjust(top=0.85)

plt.show()

# Highlight the COVID period
# Filter South Africa
national = df_long[df_long['Province'] == 'South Africa'].copy()
national['Year'] = national['Quarter'].str[-4:].astype(int)
national_yearly = national.groupby('Year')['Unemployment_Rate'].mean().reset_index()

fig, axes = plt.subplots(1, 2, figsize=(18,6), sharey=True)

axes[0].plot(national_yearly['Year'], national_yearly['Unemployment_Rate'],
             marker='o', color='darkred')
axes[0].set_title("South Africa Yearly Average (2008–2024)", fontsize=12)
axes[0].set_xlabel("Year")
axes[0].set_ylabel("Unemployment Rate (%)")
axes[0].grid(True)

axes[0].axvspan(2020, 2021, color='grey', alpha=0.3, label='COVID Period')

axes[1].plot(national['Quarter_Ordered'], national['Unemployment_Rate'],
             marker='.', color='steelblue', alpha=0.7)
axes[1].set_title("South Africa Quarterly Trend (2008–2024)", fontsize=12)
axes[1].set_xlabel("Quarter")
axes[1].tick_params(axis='x', rotation=45)
axes[1].grid(True)
axes[1].set_xticks(axes[1].get_xticks()[::4])

covid_quarters = national['Quarter_Ordered'].between("Apr-Jun 2020", "Apr-Jun 2021")
axes[1].fill_between(national['Quarter_Ordered'][covid_quarters],
                     national['Unemployment_Rate'][covid_quarters].min(),
                     national['Unemployment_Rate'][covid_quarters].max(),
                     color='grey', alpha=0.3, label='COVID Period')


fig.suptitle("South Africa Unemployment Rate: Yearly vs Quarterly (COVID Highlighted)", 
             fontsize=12, y=0.98)

fig.subplots_adjust(top=0.85)
axes[0].legend()
axes[1].legend()

plt.show()

fig.savefig("SA_Unemployment_Trend_COVID.png", dpi=300, bbox_inches='tight')

print(df_long)

# Seperating Province and Metro
# Only keep metros (exclude NaN in Metro)
metros = df_long[df_long['Metro'].notna()]

# Merge with provincial average (Province row only, no metro)
province_only = df_long[(df_long['Metro'].isna()) & (df_long['Province'] != 'South Africa')]
province_only = province_only[['Province', 'Quarter_Ordered', 'Unemployment_Rate']]
province_only = province_only.rename(columns={'Unemployment_Rate': 'Province_Rate'})

# Merge metro with its province
comparison = metros.merge(province_only, on=['Province', 'Quarter_Ordered'])

# Compute difference
comparison['Difference'] = comparison['Unemployment_Rate'] - comparison['Province_Rate']

plt.figure(figsize=(14,6))

for metro_name in comparison['Metro'].unique():
    metro_data = comparison[comparison['Metro'] == metro_name]
    plt.plot(
        metro_data['Quarter_Ordered'], 
        metro_data['Difference'], 
        label=metro_name
    )

plt.axhline(0, color='black', linestyle='--', linewidth=1)  # baseline at 0
plt.xticks(rotation=90)
plt.ylabel("Metro vs Province Unemployment Rate Difference (%)")
plt.title("Metro vs Provincial Unemployment Differences Over Time")
plt.legend()
plt.grid(True)
plt.show()
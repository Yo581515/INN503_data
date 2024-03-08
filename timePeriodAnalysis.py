import pandas as pd

# Load the Excel files with project and organization details
df_projects_h2020 = pd.read_excel("additive_manufacturing_Horizon2020.xlsx", sheet_name='projects')
df_orgs_h2020 = pd.read_excel("additive_manufacturing_Horizon2020.xlsx", sheet_name='organizations')
df_projects_heurope = pd.read_excel("additive_manufacturing_HorizonEurope.xlsx", sheet_name='projects')
df_orgs_heurope = pd.read_excel("additive_manufacturing_HorizonEurope.xlsx", sheet_name='organizations')

# Filter for Norwegian organizations
norwegian_orgs_h2020 = df_orgs_h2020[df_orgs_h2020['country'] == 'NO']
norwegian_orgs_heurope = df_orgs_heurope[df_orgs_heurope['country'] == 'NO']

# Get unique project IDs involving Norwegian organizations
norwegian_projects_ids_h2020 = norwegian_orgs_h2020['projectID'].unique()
norwegian_projects_ids_heurope = norwegian_orgs_heurope['projectID'].unique()

# Filter projects involving Norwegian organizations
norwegian_projects_details_h2020 = df_projects_h2020[df_projects_h2020['id'].isin(norwegian_projects_ids_h2020)].copy()
norwegian_projects_details_heurope = df_projects_heurope[df_projects_heurope['id'].isin(norwegian_projects_ids_heurope)].copy()

# Convert 'startDate' to datetime and 'ecMaxContribution' to numeric
norwegian_projects_details_h2020['startDate'] = pd.to_datetime(norwegian_projects_details_h2020['startDate'])
norwegian_projects_details_h2020['ecMaxContribution'] = pd.to_numeric(norwegian_projects_details_h2020['ecMaxContribution'].str.replace(',', '.'), errors='coerce')

# Create 'Time Interval' based on 'startDate' year
norwegian_projects_details_h2020['Time Interval'] = norwegian_projects_details_h2020['startDate'].dt.year

# Analyze projects per time interval
projects_per_interval = norwegian_projects_details_h2020.groupby('Time Interval').size()

# Calculate average funding per time interval
average_funding_per_interval = norwegian_projects_details_h2020.groupby('Time Interval')['ecMaxContribution'].mean()

# Print the results
print("Projects per Time Interval:")
print(projects_per_interval)
print("\nAverage Funding per Time Interval:")
print(average_funding_per_interval)

# Print details for each project row
for index, row in norwegian_projects_details_h2020.iterrows():
    print(f"ID: {row['id']}\nTitle: {row['title']}\nStart Date: {row['startDate'].date()}\nEnd Date: {row['endDate']}\nTotal Cost: {row['totalCost']}\nContent Update Date: {row['contentUpdateDate']}\n\n")
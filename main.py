import pandas as pd

# pip install pandas
# pip install openpyxl

# Load the datasets provided by the user
files = [
    "additive_manufacturing_Horizon2020.xlsx",
    "additive_manufacturing_HorizonEurope.xlsx"
]

# Read the Excel files
dfs = [pd.read_excel(file) for file in files]
# Display basic information about each dataset for a quick overview
dataset_overviews = [df.info() for df in dfs]

# Correct approach to load the "organizations" sheet specifically
df_orgs_h2020 = pd.read_excel("additive_manufacturing_Horizon2020.xlsx", sheet_name='organizations')
df_orgs_heurope = pd.read_excel("additive_manufacturing_HorizonEurope.xlsx", sheet_name='organizations')

# Now try filtering for Norwegian organizations again
norwegian_orgs_h2020 = df_orgs_h2020[df_orgs_h2020['country'] == 'NO']
norwegian_orgs_heurope = df_orgs_heurope[df_orgs_heurope['country'] == 'NO']

norwegian_projects_ids_h2020 = norwegian_orgs_h2020['projectID'].unique()
norwegian_projects_ids_heurope = norwegian_orgs_heurope['projectID'].unique()

df_projects_h2020 = dfs[0]
df_projects_heurope = dfs[1]

# Filter projects DataFrames for rows where the project ID is in the list of Norwegian project IDs
norwegian_projects_details_h2020 = df_projects_h2020[df_projects_h2020['id'].isin(norwegian_projects_ids_h2020)]
norwegian_projects_details_heurope = df_projects_heurope[df_projects_heurope['id'].isin(norwegian_projects_ids_heurope)]


norwegian_projects_count_h2020 = len(norwegian_projects_ids_h2020)
norwegian_projects_count_heurope = len(norwegian_projects_ids_heurope)

print(f"Number of Norwegian projects in H2020: {norwegian_projects_count_h2020}")
print(f"Number of Norwegian projects in Horizon Europe: {norwegian_projects_count_heurope}")


# Assuming norwegian_projects_details_h2020 is your DataFrame
for index, row in norwegian_projects_details_h2020.iterrows():
    print(f"ID: {row['id']}\nTitle: {row['title']}\nStart Date: {row['startDate']}\nEnd Date: {row['endDate']}\nTotal Cost: {row['totalCost']}\nContent Update Date: {row['contentUpdateDate']}\n\n")


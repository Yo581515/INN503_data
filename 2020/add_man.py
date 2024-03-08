import pandas as pd

# Load the Excel files with project and organization details for Horizon 2020 and Horizon Europe
df_projects_h2020 = pd.read_excel("additive_manufacturing_Horizon2020.xlsx", sheet_name='projects')
df_orgs_h2020 = pd.read_excel("additive_manufacturing_Horizon2020.xlsx", sheet_name='organizations')
df_projects_heurope = pd.read_excel("additive_manufacturing_HorizonEurope.xlsx", sheet_name='projects')
df_orgs_heurope = pd.read_excel("additive_manufacturing_HorizonEurope.xlsx", sheet_name='organizations')

# Filter for organizations located in Norway across both datasets
norwegian_orgs_h2020 = df_orgs_h2020[df_orgs_h2020['country'] == 'NO']
norwegian_orgs_heurope = df_orgs_heurope[df_orgs_heurope['country'] == 'NO']


# Extract unique project acronyms involving Norwegian organizations for both Horizon 2020 and Horizon Europe
unique_acronyms_h2020 = norwegian_orgs_h2020['projectAcronym'].unique()
unique_acronyms_heurope = norwegian_orgs_heurope['projectAcronym'].unique()

# Filter the project and organizations DataFrames for rows with acronyms in total_unique_acronyms
filtered_projects_h2020 = df_projects_h2020[df_projects_h2020['acronym'].isin(unique_acronyms_h2020)]
filtered_orgs_h2020 = df_orgs_h2020[df_orgs_h2020['projectAcronym'].isin(unique_acronyms_h2020)]

filtered_projects_heurope = df_projects_heurope[df_projects_heurope['acronym'].isin(unique_acronyms_heurope)]
filtered_orgs_heurope = df_orgs_heurope[df_orgs_heurope['projectAcronym'].isin(unique_acronyms_heurope)]
print(unique_acronyms_h2020)

#
#
#


# Assuming 'filtered_orgs_h2020' and 'filtered_orgs_heurope' are already defined
# and contain the filtered organization data for Horizon 2020 and Horizon Europe, respectively.

# Concatenate the organization data from both datasets
orgs_combined = pd.concat([filtered_orgs_h2020[['projectAcronym', 'country']], filtered_orgs_heurope[['projectAcronym', 'country']]])

# Group by 'projectAcronym' and aggregate unique 'country' values
grouped = orgs_combined.groupby('projectAcronym')['country'].unique().reset_index()

# Convert to a list of dictionaries
list_of_dicts = [{row['projectAcronym']: row['country'].tolist()} for _, row in grouped.iterrows()]

# Example output
for dic in (list_of_dicts):
    print(dic)
    print()
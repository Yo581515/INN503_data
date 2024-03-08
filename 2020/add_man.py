import pandas as pd
from ploter import plot_3d, plot_2d
from vars import country_names

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
print("Unique acronyms for Horizon 2020 involving Norwegian organizations:")
print(unique_acronyms_h2020)
print()
print("Unique acronyms for Horizon Europe involving Norwegian organizations:")
print(unique_acronyms_heurope)

#
#
#

# For Horizon 2020
# Group by 'projectAcronym' and aggregate unique 'country' values
grouped_h2020 = filtered_orgs_h2020.groupby('projectAcronym')['country'].unique().reset_index()
# Convert to a list of dictionaries
list_of_dicts_h2020 = [{row['projectAcronym']: row['country'].tolist()} for _, row in grouped_h2020.iterrows()]

# For Horizon Europe
# Group by 'projectAcronym' and aggregate unique 'country' values
grouped_heurope = filtered_orgs_heurope.groupby('projectAcronym')['country'].unique().reset_index()
# Convert to a list of dictionaries
list_of_dicts_heurope = [{row['projectAcronym']: row['country'].tolist()} for _, row in grouped_heurope.iterrows()]

# Now, modify your data to replace country codes with names
for project_dict in list_of_dicts_h2020:
    for project, countries in project_dict.items():
        project_dict[project] = [country_names.get(country, country) for country in countries]

# Now, modify your data to replace country codes with names
for project_dict in list_of_dicts_heurope:
    for project, countries in project_dict.items():
        project_dict[project] = [country_names.get(country, country) for country in countries]

# Example output for Horizon 2020
print("Horizon 2020:")
for dic in list_of_dicts_h2020:
    print(dic)
    print()

# Example output for Horizon Europe
print("Horizon Europe:")
for dic in list_of_dicts_heurope:
    print(dic)
    print()

list_of_dicts_h2020_title_text_3d = "3D network graph of Horizon 2020 projects and countries colaborating with Norwegian organizations",
list_of_dicts_h2020_title_text_2d = '2D Network Graph of Horizon 2020 Projects and Countries colaborating with Norwegian organizations'
plot_3d(list_of_dicts_h2020, list_of_dicts_h2020_title_text_3d)
plot_2d(list_of_dicts_h2020, list_of_dicts_h2020_title_text_2d)
print()

list_of_dicts_heurope_title_text_3d = "3D network graph of Horizon Europe projects and countries colaborating with Norwegian organizations",
list_of_dicts_heurope_title_text_2d = '2D Network Graph of Horizon Europe Projects and Countries colaborating with Norwegian organizations'
plot_3d(list_of_dicts_heurope, list_of_dicts_heurope_title_text_3d)
plot_2d(list_of_dicts_heurope, list_of_dicts_heurope_title_text_2d)

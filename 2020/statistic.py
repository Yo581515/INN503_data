import pandas as pd
from matplotlib import pyplot as plt
from pytz import country_names
from statistics_ploter import plot_histogramh, plot_histogram

activity_type_mapping = {
    'REC': 'Research',
    'OTH': 'Other',
    'PRC': 'Private Company',
    'HES': 'Higher Education',
    'PUB': 'Public Sector'
}
df_projects = pd.read_excel("additive_manufacturing_Horizon2020.xlsx", sheet_name='projects')
df_orgs = pd.read_excel("additive_manufacturing_Horizon2020.xlsx", sheet_name='organizations')

# Convert columns to appropriate data types
df_projects['startDate'] = pd.to_datetime(df_projects['startDate'])
df_projects['endDate'] = pd.to_datetime(df_projects['endDate'])
df_orgs['ecContribution'] = pd.to_numeric(df_orgs['ecContribution'], errors='coerce')

norwegian_orgs_h2020 = df_orgs[df_orgs['country'] == 'NO']
unique_projectID_h2020 = norwegian_orgs_h2020['projectID'].unique()

filtered_projects_h2020 = df_projects[df_projects['id'].isin(unique_projectID_h2020)].copy()
filtered_orgs_h2020 = df_orgs[df_orgs['projectID'].isin(unique_projectID_h2020)].copy()

df_projects = filtered_projects_h2020
df_orgs = filtered_orgs_h2020

# Number of organizations involved in projects concluded vs ongoing
df_projects['status'] = df_projects['status'].str.lower()
closed_projects = df_projects[df_projects['status'] == 'closed']
signed_projects = df_projects[df_projects['status'] == 'signed']
orgs_in_concluded_projects = df_orgs[df_orgs['projectID'].isin(closed_projects['id'])].groupby(
    'projectID').size().sum()
orgs_in_ongoing_projects = df_orgs[df_orgs['projectID'].isin(signed_projects['id'])].groupby('projectID').size().sum()

orgs_in_concluded_projects, orgs_in_ongoing_projects

#
#
#

# Convert relevant columns to appropriate data types
df_projects['startDate'] = pd.to_datetime(df_projects['startDate'])
df_projects['endDate'] = pd.to_datetime(df_projects['endDate'])
df_orgs['ecContribution'] = pd.to_numeric(df_orgs['ecContribution'], errors='coerce')

# Derive additional information as per requirements
df_projects['year'] = df_projects['startDate'].dt.year

# Descriptive statistics for funds received by project
funds_stats = df_projects['ecMaxContribution'].describe()

# Counting organizations per project
orgs_per_project = df_orgs.groupby('projectID').size()

# Counting types of organizations (assuming 'activityType' represents the type) per project
types_per_project = df_orgs.groupby(['projectID', 'activityType']).size().unstack(fill_value=0)
types_per_project_renamed = types_per_project.rename(columns=activity_type_mapping).copy()

# Counting organizations per country
orgs_per_country = df_orgs.groupby('country').size()
orgs_per_country_named = orgs_per_country.rename(index=country_names).copy()
project_id_to_acronym = df_projects.set_index('id')['acronym'].to_dict().copy()

# Replace the index of types_per_project_renamed with project acronyms
types_per_project_renamed.index = types_per_project_renamed.index.map(project_id_to_acronym).copy()

orgs_per_country_named.head()
# Preparing data for potential diagrams or charts
# Number of projects per year
projects_per_year = df_projects.groupby('year').size().copy()

print(orgs_per_country_named.head())
plot_histogramh(orgs_per_country_named, title_text="Number of Organizations per Country ",
                xlabel="Number of Organizations", ylabel="Country")
print()
print(orgs_per_project.head())
print(type(orgs_per_project.head()))
project_id_to_acronym = df_projects.set_index('id')['acronym'].to_dict()
orgs_per_project.index = orgs_per_project.index.map(project_id_to_acronym)
plot_histogramh(orgs_per_project, title_text="Number of Organizations per Project", xlabel="Number of Organizations",
                ylabel="Project")
print()
print(types_per_project_renamed.head())
types_per_project_renamed.plot(kind='bar', stacked=True, figsize=(12, 8),
                               color=['#1f77b4', '#ff7f0e', '#2ca02c', '#d62728', '#9467bd'])
plt.title('Organization Types per Project')
plt.xlabel('Project')
plt.ylabel('Number of Organizations')
plt.legend(title='Activity Type')
plt.tight_layout()
plt.xticks(rotation=45)  # Rotate the x-tick labels for better readability
plt.show()
print()

print()
print(projects_per_year)
plot_histogram(projects_per_year, title_text="Number of Projects per Year", xlabel="Number of Projects", ylabel="Year")
print()
print("closed projects")
list_closed_projects = closed_projects['id'].tolist()
print(list_closed_projects)
print()
print("signed projects")
list_signed_projects = signed_projects['id'].tolist()
print(list_signed_projects)

# Assuming list_closed_projects contains the IDs of closed projects
closed_projects_df = df_projects[df_projects['id'].isin(list_closed_projects)].copy()

# Stringify 'startDate' and 'endDate' columns with a specific format, e.g., YYYY-MM-DD
closed_projects_df['startDate'] = closed_projects_df['startDate'].dt.strftime('%Y-%m-%d')
closed_projects_df['endDate'] = closed_projects_df['endDate'].dt.strftime('%Y-%m-%d')

# Now, save the updated DataFrame to an Excel file
closed_projects_df.to_excel("closed_projects.xlsx", index=False)

print("Closed projects have been saved to 'closed_projects.xlsx' with stringified dates.")


signed_projects_df = df_projects[df_projects['id'].isin(list_signed_projects)].copy()
# Stringify 'startDate' and 'endDate' columns with a specific format, e.g., YYYY-MM-DD
signed_projects_df['startDate'] = signed_projects_df['startDate'].dt.strftime('%Y-%m-%d')
signed_projects_df['endDate'] = signed_projects_df['endDate'].dt.strftime('%Y-%m-%d')
signed_projects_df.to_excel("signed_projects.xlsx", index=False)
print("Signed projects have been saved to 'signed_projects.xlsx' with stringified dates.")


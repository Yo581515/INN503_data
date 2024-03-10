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


print("closed projects")
list_closed_projects = closed_projects['id'].tolist()
print(list_closed_projects)
list_closed_projects_len = len(list_closed_projects)
print(list_closed_projects_len)
print()
print("signed projects")
list_signed_projects = signed_projects['id'].tolist()
print(list_signed_projects)
list_signed_projects_len = len(list_signed_projects)
print(list_signed_projects_len)


# Data to plot
statuses = ['CLOSED', 'SIGNED/ONGOING']
values = [list_closed_projects_len, list_signed_projects_len]

# Create the histogram
plt.figure(figsize=(8, 6))
plt.bar(statuses, values, color=['#1f77b4', '#ff7f0e'])
plt.title('Distribution of Project Statuses in Additive Manufacturing for Horizon 2020')
plt.xlabel('Status')
plt.ylabel('Number of Projects')
plt.show()



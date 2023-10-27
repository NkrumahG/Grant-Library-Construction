import pandas as pd

# Read the Lux_Search_Windows.csv and SearchFile_LuxO.csv files
lux_windows_df = pd.read_csv('Lux_Search_Windows.csv')
search_df = pd.read_csv('SearchFile_LuxO.csv')

# Initialize an empty list to store matching data rows
matching_data = []

# Initialize an empty dictionary to keep track of sampled entries
sampled_entries = {}

# Iterate through each row in the Lux_Search_Windows dataframe
for _, window_row in lux_windows_df.iterrows():
    window_index = window_row['Window_Index']
    
    # Skip rows with Window_Index 0 and 11
    if window_index == 0 or window_index == 11:
        continue
    
    lb_ds = window_row['DS']
    lb_us = window_row['US']
    
    # Find matching entries in the SearchFile_LuxO dataframe
    matching_rows = search_df[(search_df['Genomic_Location'] >= lb_ds) & (search_df['Genomic_Location'] <= lb_us)]
    
    if not matching_rows.empty:
        # Sample a matching row without replacement
        sampled_index = matching_rows.sample(n=1, replace=False).index[0]
        
        # Append the sampled row to the matching_data list
        matching_row = search_df.loc[sampled_index].copy()
        matching_row['Window_Index'] = window_index
        matching_data.append(matching_row)
        
        # Record the sampled entry
        sampled_entries[sampled_index] = True

# Create a new dataframe from the matching data
result_df = pd.DataFrame(matching_data)

# Save the result dataframe to a CSV file
result_df.to_csv('LuxO_window_results.csv', index=False)




import pandas as pd
import os

#----------------------------------------------------- Makes a Dataframe containing process relevant data
file_path = 'Oct_2006_Boorondara_Traffic_Flow_Data.csv'
df = pd.read_csv(file_path)

# Selecting only V00 to V95 columns
v_columns = [f'V{str(i).zfill(2)}' for i in range(0, 96)]
selected_columns = ['SCATS Number'] + v_columns  # Include 'SCATS Number' for filtering by SCATS
filtered_df = df[selected_columns]

print(filtered_df.head())

#----------------------------------------------------- Splitting the Dataset by SCAT-SITE
unique_scats = filtered_df['SCATS Number'].unique()
output_dir = 'SCATS_Data'
os.makedirs(output_dir, exist_ok=True)

for scat in unique_scats:
    folder_path = os.path.join(output_dir, str(scat))
    os.makedirs(folder_path, exist_ok=True)
    df_filtered = filtered_df[filtered_df['SCATS Number'] == scat]
    output_file = os.path.join(folder_path, f'{scat}.csv')
    test_output_file = os.path.join(folder_path, f'{scat}_test.csv')
    df_values = df_filtered.drop(columns='SCATS Number')
    reshaped_values = df_values.values.flatten()
    reshaped_df = pd.DataFrame(reshaped_values, columns=['Values'])
    last_values = reshaped_df.iloc[-2880:]
    last_values.to_csv(test_output_file, index=False, header=True)
    train_values = reshaped_df.iloc[:-2304]
    train_values.to_csv(output_file, index=False, header=True)

    print(f'Saved {output_file}')
    print(f'Saved {test_output_file}')

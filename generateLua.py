import pandas as pd

csv_file = "test1.csv"

# Read the CSV file
df = pd.read_csv(csv_file)

# Create the image filename column
df['image_filename'] = df['grey_level_R'].astype(str) + '_' + df['grey_level_G'].astype(str) + '_' + df['grey_level_B'].astype(str)

# Create the a1 filename column
df['a1_files'] = df['image_filename'].astype(str)+'.a1'

# Access the 'a1_files' column and print formatted entries
for entry in df['a1_files']:
    print(f'"{entry}"')
import pandas as pd
import os
import yaml
import time


def get_filepaths(root_location):
    """
        Get the file names of the csv files.
    """
    csv_file_paths = []

    directory = f"{root_location}/Downloaded_Data/"

    for file in os.listdir(directory):
        # Check if the file is a CSV file
        if file.endswith('.csv'):
            # Construct the full path to the CSV file
            file_path = os.path.join(directory, file)
            # Append the file path to the list
            csv_file_paths.append(file_path)
    
    return csv_file_paths

def process(file_paths,fields):

    for file in file_paths:
        try:
            df = pd.read_csv(file)
            # change the format of DATE to calculate monthly averages.
            df['DATE'] = pd.to_datetime(df['DATE']).dt.strftime('%m-%Y')
            for col in fields:
                df[col] = pd.to_numeric(df[col], errors='coerce')
            df = df[['DATE']+fields]
            df.dropna()

            df = df.groupby(['DATE']).mean()
            
            cur_path = os.getcwd()

            # store the monthly averages data in processed_data folder
            os.makedirs(os.path.join(cur_path,'Processed_Data'),exist_ok=True)
            full_path = f"{cur_path}/Processed_Data"
            os.makedirs(full_path,exist_ok=True)

            df.to_csv(f"{full_path}/{file.split('/')[-1]}",index=True)
        except:
            continue

    


if __name__ == '__main__':

    st = time.time()

    with open('params.yaml','r') as file:
        params = yaml.safe_load(file)

    
    fields = params['daily_fields']

    root_loc = os.getcwd()

    file_paths = get_filepaths(root_loc)
    process(file_paths,fields)

    print('-'*100)
    print(f'Task completed in {time.time() - st} sec.')



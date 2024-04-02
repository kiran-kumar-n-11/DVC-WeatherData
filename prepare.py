import pandas as pd
import os
import yaml
import time


def get_filepaths(root_location,year):

    csv_file_paths = []

    directory = f"{root_location}/Data/{year}/"

    for file in os.listdir(directory):
        # Check if the file is a CSV file
        if file.endswith('.csv'):
            # Construct the full path to the CSV file
            file_path = os.path.join(directory, file)
            # Append the file path to the list
            csv_file_paths.append(file_path)
    
    return csv_file_paths

def prepare(file_paths,fields,year):

    for file in file_paths:
        try:
            df = pd.read_csv(file)
            df['DATE'] = pd.to_datetime(df['DATE']).dt.strftime('%m-%Y')
            df = df[['DATE']+fields]

            cur_path = os.getcwd()
            os.makedirs(os.path.join(cur_path,'Extracted_Data'),exist_ok=True)
            full_path = f"{cur_path}/Extracted_Data/{year}"
            os.makedirs(full_path,exist_ok=True)

            df.to_csv(f"{full_path}/{file.split('/')[-1]}",index=False)
        except:
            continue
    


if __name__ == '__main__':

    st = time.time()

    with open('params.yaml','r') as file:
        params = yaml.safe_load(file)

    year = params['year']
    fields = params['monthly_fields']
    root_loc = os.getcwd()

    file_paths = get_filepaths(root_loc,year)
    prepare(file_paths,fields,year)

    print('-'*100)
    print(f'Task completed in {time.time() - st} sec.')



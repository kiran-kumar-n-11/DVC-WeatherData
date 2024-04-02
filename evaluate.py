import pandas as pd
import os
import yaml
import time
from sklearn.metrics import r2_score

def get_filepaths(root_location):

    csv_file_paths = []

    directory = f"{root_location}/Processed_Data/"

    for file in os.listdir(directory):
        # Check if the file is a CSV file
        if file.endswith('.csv'):
            # Append the file path to the list
            csv_file_paths.append(file)

    return csv_file_paths

def evaluate(file_paths):
    r2score_metric = {}
    consistent_stations = 0
    inconsistent_stations = 0
    under_data_stations = 0

    cwd = os.getcwd()

    for file in file_paths:
        try:
            processed_df = pd.read_csv(f"{cwd}/Processed_Data/{file}") # contains calc monthly average
            extracted_df = pd.read_csv(f"{cwd}/Extracted_Data/{file}") # contains original monthly average
            extracted_df = extracted_df.dropna()
            if(extracted_df.shape[0]!=0):
                merged_df = pd.merge(processed_df , extracted_df, on='DATE')
                merged_df = merged_df.dropna()
    #             display(merged_df)
                if(merged_df.shape[0]>2):
                    R2Score = r2_score(merged_df['MonthlyDepartureFromNormalAverageTemperature'],
                                    merged_df['DailyDepartureFromNormalAverageTemperature'])
                    r2score_metric[file[:-4]] = R2Score
                    if(R2Score>=0.9):
                        consistent_stations+=1
                    else:
                        inconsistent_stations+=1
                else:
                    under_data_stations += 1
            else:
                under_data_stations += 1
                
        except:
            under_data_stations += 1
            continue

        
    os.makedirs(f"{cwd}/Metrics",exist_ok=True)
    path = f"{cwd}/Metrics/"
    diis = [(key, value) for key, value in r2score_metric.items()]
    metrics_df = pd.DataFrame(diis,columns=['Station','R2 Score'])
    metrics_df.to_csv(f"{path}r2_score.csv")

    return [consistent_stations,inconsistent_stations,under_data_stations]

    


if __name__ == '__main__':

    st = time.time()

    with open('params.yaml','r') as file:
        params = yaml.safe_load(file)

    year = params['year']

    root_loc = os.getcwd()

    file_paths = get_filepaths(root_loc)
    consistent_stations, inconsistent_stations, under_data_stations = evaluate(file_paths)
    print('-'*100)
    print()
    print("YEAR: ",year)
    print("Number of consistent stations: ",consistent_stations)
    print("Number of inconsistent stations: ",inconsistent_stations)
    print("Number of stations with insufficient or no data: ",under_data_stations)
    print()
    print('-'*100)
    print(f'Task completed in {time.time() - st} sec.')



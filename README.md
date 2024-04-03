### This repository conatins project to check if the monthly average weather data on the NCEI website is consistent with calculated monthly average using daily average data available.

### The repository contains the following:

- download.py --> To download the weather data based on year and nlocs(no. of stations data required) specified.  
- process.py --> To fetch the monthly average data based on weather data fields specified if any exists.
- prepare.py --> To calculate monthly average data for the specified fields based on daily average data available.
- evaluate.py --> To calculate consistency using R2 Score for fetched monthly averages and calculated monthly averages.
<br></br>
- params.yaml --> To specify parameters required like year, nlocs, weather data fields.
- dvc.yaml --> To create pipeline based on dependencies, outputs and to keep track record. Consequently dvc.lock is created.
<br></br>
- commands.txt --> sample CLI command to add a stage in dvc pipeline.

The data is stored in the local machine itself and tracked using dvc.

  

This repository conatins project to check if the monthly average weather data on the NCEI website is consistent with calculated monthly average using 
daily average data available.

The repository contains the following:
- download.py --> To download the weather data based on year and nlocs(no. of stations data required) specified.
  - outs: Downloaded_Data/ --> used dvc to track it. Hence Downloaded_Data.dvc is added.  
- process.py --> To fetch the monthly average data based on weather data fields specified if any exists.
- prepare.py --> To calculate monthly average data for the specified fields based on daily average data available.
- evaluate.py --> To calculate consistency using R2 Score for fetched monthly averages and calculated monthly averages. 

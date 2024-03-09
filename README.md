# Currency Data Fetching and Analysis

This Python script fetches exchange rates for specified currency pairs from the National Bank of Poland's API (https://api.nbp.pl/) and provides functionality for data selection, saving, user interaction, error handling, and data analysis.

## Fetching Currency Data:

- Utilizing the website https://api.nbp.pl/ and Python, retrieve exchange rates for EUR/PLN, USD/PLN, and CHF/PLN for the last 60 days.
- Save this data in separate columns. Additionally, create two more columns containing the EUR/USD and CHF/USD rates, calculated based on the retrieved data.

## Data Selection:

- Allow the user to input the name of the currency pairs they wish to access information for. Ideally, enable the user to specify multiple currency pairs.
- Filter the data to only include rows relevant to the chosen currency pairs.

## Saving Data:

- Save all the previously mentioned data (dates and rates for five pairs) into a CSV file named "all_currency_data.csv".
- Develop a function to permit the saving of only the user-selected currency pairs to a CSV file named "selected_currency_data.csv".
    - The CSV should retain the columns from the original file but only for the currencies selected by the user.
    - Store the filtered data in the CSV file.

## User Interaction:

- After saving the data, display a confirmation message such as "Data for [Currency] has been saved!"

## Error Handling:

- Create and implement appropriate error handling mechanisms for potential issues that might arise during the execution of the script. Ensure that the user is informed in a user-friendly manner about any errors that occur.

## Data Analysis:

- Develop a Python function that calculates and displays the average rate value, median, minimum, and maximum for the selected currency pair.

## Automated Daily Execution:

- Implement functionality for the script to run daily at 12:00 PM and automatically save the data to the "all_currency_data.csv" file. Ensure that each script execution overwrites the file only with new entries.

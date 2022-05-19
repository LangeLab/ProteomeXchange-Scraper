# ProteomeXchange-Scraper
Automated web scraper to collect and filter pediatric cancer datasets from ProteomeXchange.

## TODOs - Features To Add:

- Allow for the user to provide the keyword list for filtering. Ex: through a text file w/ each keyword separated by a new line or comma. Then pass in the input file as an argument when running the script.

- Include a more detailed search by accessing the inside of a particular metadata entry, then searching for the keywords within the summary/abstract.

- Only add newly uploaded ProteomXchange datasets to a preloaded version of the full dataframe. Ex: have the script compare the most recent entry from the preloaded data to the ProteomeXchange metadata to know where/which page the new run should stop.

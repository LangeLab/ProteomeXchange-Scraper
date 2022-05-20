# ProteomeXchange-Scraper
Automated web scraper to collect and filter pediatric cancer datasets from ProteomeXchange.

## Usage
A user can either filter ProteomeXchange datasets using a default pediatric cancer related keyword list, or input their own keyword list.

```
  usage: proteomeXchange_scraper.py [-h] [-i INPUTFILE]
  options:
  -h, --help            show this help message and exit
  -i INPUTFILE, --inputFile INPUTFILE
                        name of text file w/ each keyword on a new line (default: None)
```                        
                        
## TODOs - Features To Add:

- Include a more detailed search by accessing the inside of a particular metadata entry, then searching for the keywords within the summary/abstract.

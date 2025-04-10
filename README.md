# N2YO-Scraper
Scrapes the N2YO website for satellite passes per the users location.

## Setup
This tool requires the user to signup for an account on N2YO [here](https://www.n2yo.com/login/register/).

Once the user has an account, an API key can be generated [here](https://www.n2yo.com/login/edit/)

This API key must be added to the user's config.ini file as the "myKey" value.

## Usage
The tool is meant to be run as a cronjob, one part fetching data from the N2YO API and another converting that data into
individual calendar events. Both script pull configuration information from the single user-created config.ini file,
whose example format can be found as "config.ini.example".

## Requirements
The following packages must be installed to use this tool:
* requests
* python-dateutil

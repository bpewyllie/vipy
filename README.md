# vipy
 Python webscraper for Vegas Insider line history pages.

## Installation


## Usage

1. Construct a Matchup instance, e.g.,
```
jazz_raps = Matchup(league="nba", away="jazz", home="raptors", date="01-01-19")
```

2. Explore data about the Matchup by exploring its attributes.

## Release notes

## To do

- Finish NBA money line history scraper

  - ~~Scrape and store NBA schedules from past 10 years from basketball reference.~~

  - Use schedule data to store matchup start time, results, and other data to 
  attributes.

  - Create fully fleshed example analysis of using trends in betting lines histories to 
  predict game results.

  - Publish to pypi for pip install.

- Generalize money line history scraper to work for MLB, NFL, and potentially other 
leagues.

  - Store nicknames file for each league in assets folder.

  - Download and store schedules for each league.

  - Create mini examples documenting use.

- Generalize money line history scraper to work for other odds types (spread, total, 
first half, second half, etc.)

- Create scraper for VI betting trends pages.
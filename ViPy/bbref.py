import pandas
import requests
import bs4


def get_season_url(season_start_year: int, month: str, covid_october: int = 1) -> str:
    """
    Retrieves string of basketball-reference url for the provided season start year and
    desired month in the schedule.

    - covid_october : the interrupted 2019-2020 season and subsequent 2020 bubble
    season are represented together as the 2019-2020 season in basketball-reference.
    Because of this, there are two October months in the season, and so the user must
    specify whether they prefer the first of these months (1, the default), or the
    second (2).
    """
    base = "https://www.basketball-reference.com/leagues/NBA_{}_games-{}{}.html"

    if (season_start_year == 2019) & (month.lower() == "october"):
        url = base.format(
            season_start_year + 1,
            month.lower(),
            "-" + str(season_start_year + covid_october - 1),
        )
    else:
        url = base.format(season_start_year + 1, month.lower(), "")
    return url


def get_schedule(
    season_start_year: int, month: str, covid_october: int = 1
) -> pandas.DataFrame:
    """
    Retrieves pandas DataFrame of all matchups for the specified month in the season
    defined by the specified season start year.
    """
    url = get_season_url(season_start_year, month, covid_october)

    try:
        html = requests.get(url).content
    except:
        return None

    soup = bs4.BeautifulSoup(html, "html.parser")

    schedule_table = soup.find(id="schedule")
    schedule_df = pandas.read_html(str(schedule_table))[0]

    return schedule_df


def get_season_schedule(season_start_year: int) -> pandas.DataFrame:
    """
    Retrieves pandas DataFrame of all matchups for the season specified by the season
    start year.
    """
    start_url = "https://www.basketball-reference.com/leagues/NBA_{}_games.html".format(
        season_start_year + 1
    )
    html = requests.get(start_url).content
    soup = bs4.BeautifulSoup(html, "html.parser")

    raw_months = [x.text for x in soup.find_all("div", attrs={"class": "filter"})][0]
    months = [x.split(" ")[0].lower() for x in raw_months.split("\n") if x != ""]

    season_df = pandas.DataFrame()

    if season_start_year == 2019:

        for month in months[:-1]:
            season_df = season_df.append(get_schedule(season_start_year, month, 1))

        for month in months[-1:]:
            season_df = season_df.append(get_schedule(season_start_year, month, 2))

    else:

        for month in months:
            season_df = season_df.append(get_schedule(season_start_year, month, 1))

    season_df.reset_index(drop=True, inplace=True)

    season_df.rename(
        columns={
            "Visitor/Neutral": "away_team",
            "PTS": "away_points",
            "Home/Neutral": "home_team",
            "PTS.1": "home_points",
            "Attend.": "attendance",
            "Notes": "notes",
        },
        inplace=True,
    )

    # create indicator for whether game was a playoff game
    try:
        playoff_index = season_df.loc[season_df["Date"] == "Playoffs"].index[0]
        season_df["playoff"] = (season_df.index > playoff_index)
    except:
        season_df["playoff"] = None
    
    season_df = season_df.loc[season_df["Date"] != "Playoffs"]

    # create start datetime column; old seasons don't have time data
    season_df["start"] = pandas.to_datetime(
        season_df["Date"] + " " + season_df.get("Start (ET)", default="")
    )

    # identify overtime and box score columns based on contents

    # drop unneeded columns
    # season_df.drop(columns={"Date", "Unnamed: 6"}, inplace=True)

    # if "Start (ET)" in season_df:
    #     season_df.drop(columns={"Start (ET)"}, inplace=True)

    return season_df
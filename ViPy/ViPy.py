import pandas
import requests
import bs4


class Matchup:
    """
    Defines a Matchup object from a given league, home team, away team, and date.

    Parameters
    ----------
    league : one of "nba", "mlb", or "nfl", the big 3 usa professional sports leagues
    home   : the nickname of the home team of the matchup; must follow Vegas Insider's
             nicknames
    away   : the away team of the matchup
    date   : date the match took (or will take) place in mm-dd-yy string format

    Examples
    --------
    Creating an NBA Matchup object.

    >>> jazz_raps = Matchup(
        league="nba", away="jazz", home="raptors", date="01-01-19"
        )

    The Matchup object itself returns nothing, but its attributes hold information
    about the game, its betting line history, and its betting trends.

    >>> jazz_raps.money_line_history.head()
	fav	fav_odds	dog	dog_odds
    Date				
    2019-12-31 15:10:00	TOR	-153	UTH	138
    2019-12-31 15:10:00	TOR	-153	UTH	138
    2019-12-31 15:15:00	TOR	-160	UTH	140
    2019-12-31 16:00:00	TOR	-160	UTH	140
    2019-12-31 17:35:00	TOR	-150	UTH	130
    """

    def __init__(self, league: str, away: str, home: str, date):

        self.league = league
        self.home = home
        self.away = away
        self.date = date

        self.money_line_url = self._get_line_movement_page_url()
        self.money_line_history = self.get_line_history(odds_type="money line")

        self.betting_trend_url = self._get_betting_trend_page_url()
        self.betting_trends = self.get_betting_trends(odds_type="money line")

    def _get_matchup_info(self) -> dict:
        """
        Returns dict of matchup details and result.
        """

        return None

    def _get_line_movement_page_url(self) -> str:
        """
        Returns url of Vegas Insider page displaying the matchup's line history.
        """
        url = (
            "https://www.vegasinsider.com/"
            "{}/odds/las-vegas/line-movement/{}-@-{}.cfm/date/{}".format(
                self.league, self.away, self.home, self.date
            )
        )

        return url

    def _get_line_movement_page_content(self) -> str:
        """
        Returns HTML page content of the matchup's line history from Vegas Insider.
        """
        html = requests.get(self.money_line_url).content

        return html

    def get_line_history(
        self, odds_type: str = "money line", book_code: str = "BT"
    ) -> pandas.DataFrame:
        """
        Returns pandas dataframe of the matchup's money line history.

        - odds_type : specifies the line history to pull from the following:
            - money line  : straight bet on the winner of the matchup (default)
            - spread      : bet on the margin of victory
            - total       : bet on the total points scored
            - first half  : bet on the margin of victory in the first half (if
                            applicable) with even odds
            - second half : bet on the margin of victory in the second half (if
                            applicable) with even odds
            - all         : returns a dictionary of dataframes of all odds types

        - book_code : specifies the sportsbook supplying the odds:
            - BO          : Atlantis
            - E           : Caesar's/Harrah's
            - BQ          : CG Technology
            - CG          : Coasts
            - H           : Golden Nugget
            - CK          : Jerry's Nugget
            - N           : Mirage-MGM
            - P           : Peppermill
            - CA          : Southpoint
            - X           : Stations
            - Y           : Stratosphere
            - CL          : Treasure Island
            - BT          : Vegas Insider Consensus (default)
            - J           : Westgate Superbook
            - L           : William Hill
            - AA          : Wynn
        """
        html = self._get_line_movement_page_content()
        soup = bs4.BeautifulSoup(html, "html.parser")

        try:

            odds_hist = pandas.read_html(
                soup.find("a", attrs={"name": book_code})
                .find_parent("table")
                .find_next_sibling("table")
                .prettify(),
                header=[0, 1],
            )[0]

            odds_hist.columns = [
                "_".join(col).strip() for col in odds_hist.columns.values
            ]
            odds_hist["Date"] = pandas.to_datetime(
                odds_hist["Unnamed: 0_level_0_Date"]
                + "/"
                + self.date[-2:]
                + " "
                + odds_hist["Unnamed: 1_level_0_Time"]
            )
            odds_hist.drop(
                columns=["Unnamed: 0_level_0_Date", "Unnamed: 1_level_0_Time"],
                inplace=True,
            )

            odds_hist.set_index("Date", inplace=True)

            if odds_type == "money line":

                # money line dataframe
                money_line = (
                    odds_hist[["Money Line_Fav", "Money Line_Dog"]]
                    .dropna()
                    .drop_duplicates(subset=["Money Line_Fav", "Money Line_Dog"])
                )

                money_line[["fav", "fav_odds"]] = money_line[
                    "Money Line_Fav"
                ].str.split("-", expand=True)
                money_line["fav"] = money_line["fav"].str.strip()
                money_line["fav_odds"] = -pandas.to_numeric(money_line["fav_odds"])

                money_line[["dog", "dog_odds"]] = money_line[
                    "Money Line_Dog"
                ].str.split("+", expand=True)
                money_line["dog"] = money_line["dog"].str.strip()
                money_line["dog_odds"] = pandas.to_numeric(money_line["dog_odds"])

                money_line.drop(
                    columns=["Money Line_Fav", "Money Line_Dog"], inplace=True
                )

                return money_line

            else:
                return "odds_type not supported"

        # spread dataframe
        # spread = odds_hist[["Spread_Fav", "Spread_Dog"]].dropna().drop_duplicates(subset=["Spread_Fav", "Spread_Dog"])
        # spread[["fav", "spread", "fav_odds"]] = spread["Spread_Fav"].str.split(r"\+|-", expand=True)

        except:
            return None





    def _get_betting_trend_page_url(self) -> str:
        """
        Returns url of Vegas Insider page displaying the matchup's betting trend
        history.
        """

        return None

    def _get_betting_trend_page_content(self) -> str:
        """
        Returns HTML page content of the matchup's betting trend history from Vegas
        Insider.
        """

        return None

    def get_betting_trends(self, odds_type: str = "money line") -> pandas.DataFrame:
        """
        Returns pandas dataframe of the matchup's betting trends.

        - odds_type : specifies the line history to pull from the following:
            - money line  : straight bet on the winner of the matchup (default)
            - spread      : bet on the margin of victory
            - total       : bet on the total points scored
        """

        return None

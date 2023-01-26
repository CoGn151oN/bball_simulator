from typing import Union
from urllib.parse import urljoin
import requests
from loguru import logger


class ApiError(Exception):
    pass


class FaceitApi:

    faceit_api_key = "put key here"
    faceit_base_url = "https://open.faceit.com/data/"
    faceit_db_version = "v4"

    @property
    def faceit_headers(self):
        return {
            "Authorization": "Bearer " + self.faceit_api_key,
            "Accept": "application/json",
        }

    def get_response(self, entity: Union[int, str], query_type: str = "game_player_id") -> dict:
        """
        Parameters
        ----------
        entity :  str, int
            Can accept string representing a player's Faceit name or the match ID string, OR, (hopefully)
            a player's Steam ID.
        query_type : str
            Type of query.  Accepts: "game_player_id" (Steam ID), "nickname" (Faceit nickname), or
            "game" (Faceit match ID).

        Returns
        -------
        dict
            Json dict of response data.
        """
        if query_type not in ["game_player_id", "nickname", "game"]:
            raise Exception("Invalid query type.")
        if query_type == "game_player_id":
            game_param = "&game=csgo"
        else:
            game_param = ''
        url = urljoin(self.faceit_base_url, f"{self.faceit_db_version}/players?{query_type}={entity}{game_param}")
        logger.info("Fetching player info from {}".format(url))

        resp = requests.get(url, headers=self.faceit_headers)

        no_faceit_account = (resp.status_code == 404) & (query_type == "game_player_id")
        other_error = (resp.status_code != 200) and not no_faceit_account
        if other_error:
            raise ApiError(resp.status_code, resp.text, url)
        elif no_faceit_account:
            logger.info("Steam ID does not have a Faceit account.")
            return {}
        return resp.json()

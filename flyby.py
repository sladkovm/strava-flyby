"""
1. Get IDs from flyby:
    - distance
    - elapsedTime
    - startTime

>>> fb = flyby(activity_id=12345)

"""
import os
import requests
import json
import pandas as pd
from loguru import logger


def flyby(activity_id):
    """Find flybys for a given activity

    Parameters
    ----------
    activity_id : int
        Strava activity id

    Returns
    -------
    obj : Flyby
    """
    return Flyby(_request_strava_flyby(activity_id))


def _request_strava_flyby(activity_id):
    """Request the Strava Labs Flyby and return the json content
    
    Returns:
    --------
    dict with keys 'activity', 'matches', 'athletes'
    """
    __base_url = 'https://nene.strava.com/flyby/matches/'
    __headers = {'referer': 'https://labs.strava.com/flyby/viewer/',
                 'origin': 'https://labs.strava.com'}
    logger.info("Requesting Strava Flyby for activity ID = {}".format(activity_id))
    r = requests.get('{}{}'.format(__base_url, activity_id), headers=__headers)
    if r.ok:
        content = json.loads(r.text)
        return content
    else:
        raise ConnectionError("Flyby returned {}".format(r.status_code))


class Flyby():
    """Results of Flyby search


    Attributes
    ----------
    raw_content: dict
        Deserialized and unprocessed JSON reponse of the Strava Flyby API

    """

    def __init__(self, content=None):
        """Create Flyby object

        This objects serves as a convenience wrapper
        around the Strava Flyby API JSON response. The easiest way to initialite is
        to call the factory function flyby(activity_id).

        Parameters
        ----------
        raw_content : dict
            Deserialized and unprocessed JSON response of the Strava Flyby API
        raw_activity: dict
            Requesting activity
        raw_matches: list
            Found list of matches
        matches: List
            Flattened list of matches ready to use for DataFrame
        """

        self.raw_content = content


    def __str__(self):
        return f"{self.raw_content}"


    def __repr__(self):
        n_matches = len(self.matches)
        return f"""Flyby object with {n_matches} matches. 
        Attributes: ids, activity, matches, athletes
        Methods: matches_to_list(), matches_to_json()"""


    def matches_to_list(self, **kwargs):
        """Dump flattened matches into a list

        Parameters
        ----------
        kwargs : see to_json

        Returns
        -------
        list
        """

        return self.matches_to_json(**kwargs)


    def matches_to_json(self, path_or_buf=None, **kwargs):
        """Dump flattened matches into json or a list

        Parameters
        ----------
        path_or_buf : file path, optional
            default=None, which means the results will be dumped into a list of dicts
        distance : number, optional
            Distance in km, default=None, which means all ids are returned
        tol : float from 0 to 1, optional
            Tolerance +/- on `distance`, only applicable if former is not None, default=0.1

        Returns
        -------
        None or list
        """

        df = pd.DataFrame(self._flatten_matches())

        rv = df[self._distance_filter(**kwargs)]

        if path_or_buf:

            rv.to_json(path_or_buf, orient=kwargs.get('orient', 'records'))

        else:

            return json.loads(rv.to_json(orient=kwargs.get('orient', 'records')))


    def get_ids(self, **kwargs):
        """IDs returned by Flyby

        Parameters
        ----------
        distance : number, optional
            Distance in km, default=None, which means all ids are returned
        tol : float from 0 to 1, optional
            Tolerance +/- on `distance`, only applicable if former is not None, default=0.1

        Returns
        -------
        list
        """

        df = pd.DataFrame(self._flatten_matches())

        return df[self._distance_filter(**kwargs)]['id'].tolist()



    def _distance_filter(self, **kwargs):
        """

        Parameters
        ----------
        distance : number or a tuple, optional
            If number, than distance is treated as a center distance and the range
            is calculated as `distance` +/- `tol`*`distance`
            If tuple, than the tuple is treated as a range
        tol : float, optional
            Only relevant with center distance, default=0.1

        Returns
        -------
        pd.Series
        """

        df = pd.DataFrame(self._flatten_matches())

        if not kwargs.get('distance', None):

            return df['distance'] > -1

        if (type(kwargs.get('distance')) == int) or (type(kwargs.get('distance')) == float):

            rv = ((df['distance'] > (1.0 - kwargs.get('tol', 0.1)) * kwargs.get('distance') * 1000) &
                  (df['distance'] < (1.0 + kwargs.get('tol', 0.1)) * kwargs.get('distance') * 1000))

        elif type(kwargs.get('distance')) == tuple:

            rv = ((df['distance'] > kwargs.get('distance')[0] * 1000) &
                  (df['distance'] < kwargs.get('distance')[1] * 1000))

        else:

            raise ValueError("Distance must be either a number or a tuple of numbers")

        return rv


    def _flatten_matches(self):
        """Convert all matches into flat dict

        Returns
        -------
        dict
            With keys: ['activityType', 'athleteId', 'closestDistance', 'closestPoint',
                'correlation', 'distance', 'elapsedTime', 'id', 'name', 'spatialCorrelation', 'startTime' ]
        """

        rv = []
        for m in self.matches:

            _a = m['otherActivity']
            _c = m['correlation']
            _a.update(_c)

            rv.append(_a)

        return rv

    @property
    def ids(self):
        """List of found activities ids

        Returns
        -------
        list
        """
        if self.raw_content:
            return self.get_ids()
        else:
            return None

    @property
    def activity(self):
        """Requesting activity

        Returns
        -------
        dict
        """
        if self.raw_content:
            return self.raw_content.get('activity', None)
        else:
            return None

    @property
    def matches(self):
        """Flattend matches

        Returns
        -------
        list of dict ready to use as input for DataFrame
        """

        if self.raw_content:
            return self.matches_to_list()
        else:
            return None

    @property
    def matches(self):
        """Matches returned by Flyby

        Returns
        -------
        list
        """
        if self.raw_content:
            return self.raw_content.get('matches', None)
        else:
            return None


    @property
    def athletes(self):
        """Athletes returned by Flyby

        Returns
        -------
        dict
        """
        if self.raw_content:
            return self.raw_content.get('athletes', None)
        else:
            return None

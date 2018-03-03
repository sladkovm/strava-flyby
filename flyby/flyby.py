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


def flyby(activity_id):
    """"""

    fb = Flyby()
    fb.get(activity_id)

    return fb


class Flyby():
    """Access to Strava Flyby"""

    __base_url = 'https://nene.strava.com/flyby/matches/'


    def __init__(self):

        self.content = None


    def get(self, activity_id):
        """Make a request to Flyby

        Parameters
        ----------
        activity_id : int

        Returns
        -------
        self : Flyby
            self.content has dict_keys(['activity', 'matches', 'athletes'])

        """

        r = requests.get('{}{}'.format(self.__base_url, activity_id))

        if r.ok:

            rv = json.loads(r.text)

            self.content = rv

        else:

            raise ConnectionError("Flyby returned {}".format(r.status_code))

        return self


    def to_json(self, path_or_buf=None, **kwargs):
        """Dump flattened results into json or a list

        Flattened results will have following keys:
            dict_keys([
                'activityType',
                'athleteId',
                'closestDistance',
                'closestPoint',
                'correlation',
                'distance',  # in meters
                'elapsedTime',  # in seconds
                'id',
                'name',  #Activity name
                'spatialCorrelation',
                'startTime'  #seconds since epoch
                ])

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

        df = pd.DataFrame(self._flatten())

        if kwargs.get('distance', None):

            rv = df[(df['distance'] > (1.0 - kwargs.get('tol', 0.1)) * kwargs.get('distance') * 1000) &
                      (df['distance'] > (1.0 - kwargs.get('tol', 0.1)) * kwargs.get('distance') * 1000)]

        else:

            rv = df

        if path_or_buf:

            rv.to_json(path_or_buf, orient=kwargs.get('orient', 'records'))

        else:

            return json.loads(rv.to_json(orient=kwargs.get('orient', 'records')))


    def ids(self, **kwargs):
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

        df = pd.DataFrame(self._flatten())

        if kwargs.get('distance', None):
            return df[(df['distance'] > (1.0 - kwargs.get('tol', 0.1)) * kwargs.get('distance') * 1000) &
                      (df['distance'] > (1.0 - kwargs.get('tol', 0.1)) * kwargs.get('distance') * 1000)]['id'].tolist()

        else:
            return df['id'].tolist()


    def _flatten(self):
        """Flatten the matches dict

        Returns
        -------
        dict
        """

        rv = []
        for m in self.matches:

            _a = m['otherActivity']
            _c = m['correlation']
            _a.update(_c)

            rv.append(_a)

        return rv


    @property
    def activity(self):
        """Requesting activity

        Returns
        -------
        dict
        """
        if self.content:
            return self.content.get('activity', None)
        else:
            return None


    @property
    def matches(self):
        """Matches returned by Flyby

        Returns
        -------
        list
        """
        if self.content:
            return self.content.get('matches', None)
        else:
            return None


    @property
    def athletes(self):
        """Athletes returned by Flyby

        Returns
        -------
        dict
        """
        if self.content:
            return self.content.get('athletes', None)
        else:
            return None
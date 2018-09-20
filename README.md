# Python client for Strava Flyby

[![Build Status](https://travis-ci.org/sladkovm/strava-flyby.svg?branch=master)](https://travis-ci.org/sladkovm/strava-flyby)


## Install

$ pip install strava-flyby


## Usage

*strava-flyby* provides a convenience object wrapping of the *Strava Labs Flyby API* response. Next to providing a direct access to the unmodified content of the *Flyby API* response, the object will expose number of convenience attributes and methods to access the list of activity ids, matches and athletes.  

Create a *flyby* object using the Strava activity ID with a help of the `flyby()` factory function:
```
from flyby import flyby
fb = flyby(activity_id=12345)
print(fb)
>>> <flyby.Flyby object at 0x000002D65BE952E8>
```

List of implemented methods and attributes:
```
dir(fb)
>>> [..., 'raw_activity', 'raw_athletes', 'raw_content', 'raw_matches',
          'ids', 'get_ids', 'matches_to_json', 'matches_to_list']
```

Filter by distance in km and print all matched ids:
```
print(fb.get_ids(distance=(110, 130)))
```

Dump filtered by distance flattened matches into a list:
```
print(fb.matches_to_list(distance=120, tol=0.1))
```

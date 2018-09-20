# Python client for Strava Flyby

[![Build Status](https://travis-ci.org/sladkovm/strava-flyby.svg?branch=master)](https://travis-ci.org/sladkovm/strava-flyby)


## Install

$ pip install strava-flyby


## Usage

*strava-flyby* provides a convenience object wrapping of the *Strava Labs Flyby API* response. Next to providing a direct access to the unmodified content of the *Flyby API* response, the object will expose number of convenience attributes and methods to access the list of activity ids, matches and athletes.  

Create a *flyby* object from the activity using the `flyby()` factory function:
```
from flyby import flyby
fb = flyby(activity_id=12345)
print(fb)
>>> <flyby.Flyby object at 0x000002D65BE952E8>
```

List implemented methods and attributes:
```
dir(fb)
>>> [..., 'activity', 'athletes', 'content', 'ids','matches',
          'get_ids', 'to_json', 'to_list']
```

Print deserialized output of Strava Flyby API:
```
print(fb.content)
```

Print raw matches:
```
print(fb.matches)
```

Filter by distance in km and print all matched ids:
```
print(fb.get_ids(distance=(110, 130)))
```

Dump filtered by distance flattened matches into a list:
```
print(fb.to_list(distance=120, tol=0.1))
```

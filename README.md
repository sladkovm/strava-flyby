# Python client for Strava Flyby

[![Build Status](https://travis-ci.org/sladkovm/strava-flyby.svg?branch=master)](https://travis-ci.org/sladkovm/strava-flyby)

## Install

$ pip install strava-flyby


## Usage

Create a *flyby* object using the `flyby()` function:
```
from flyby import flyby
fb = flyby(activity_id=12345)
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

Dump all flattened matches into a list and filter by distance:
```
print(fb.to_list(distance=120, tol=0.1))
```

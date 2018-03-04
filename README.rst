Python client for Strava Flyby
==============================


pip install strava-flyby


>>> from flyby import flyby
>>> fb = flyby(activity_id=12345)

# Print raw matches
>>> print(fb.matches)

# Print all matched ids filtered by distance in km
>>> print(fb.ids(distance=(110, 130)))

# Dump all flattened matches into a list and filter by distance
>>> print(fb.to_list(distance=120, tol=0.1))
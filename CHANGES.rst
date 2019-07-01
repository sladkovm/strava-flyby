Changelog
=========

0.0.6 (2019-07-01)
------------------

Breaking changes:

- Attributes raw_activity, raw_matches, raw_athletes are accessed as activity, matches and athletes respectively

New features:

- added __str__ and __repr__ to Flyby object

Bug fixes:

- Fixed requests to Strava Labs



0.0.5 (2018-12-28)
------------------

Bug fixes:

- updated dependencies

0.0.4 (2018-12-28)
------------------

Bug fixes:

- updated dependencies

0.0.3 (2018-09-20)
------------------

Breaking changes:

- ids becomes and attribute wrapper
- get_ids() is a full function to filter the ids
- explicit prefixes raw_ for all attributes that return original data or their
subset
- matches is an attribute wrapper that returns the flattened ready to use in
DataFrame list of matched activities

New features:

- pipenv
- travisio

Bug fixes:

- *add item here*


0.0.2 (2018-03-05)
------------------

Breaking changes:

- *add item here*

New features:

- to_list and to_json methods to dump flattened matches
- distance filter by center distance with +/- tolerance
- distance filter by range (start, end)

Bug fixes:

- distance filter


0.0.1 (2018-03-04)
------------------

Breaking changes:

- *add item here*

New features:

- First release

Bug fixes:

- *add item here*



0.X.X (unreleased)
------------------

Breaking changes:

- *add item here*

New features:

- Stress in zone

Bug fixes:

- *add item here*

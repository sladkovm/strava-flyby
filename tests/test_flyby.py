import pytest
import json
import os
import httpretty
from flyby import Flyby, flyby


@pytest.fixture
def flyby_response():

    current_dir = os.path.dirname(os.path.abspath(__file__))
    f_name = os.path.join(current_dir, 'flyby.json')

    with open(f_name, encoding='utf-8') as f:

        rv = json.dumps(json.load(f))

    return rv


def test_constructor_with_none():

    fb = Flyby()

    assert fb.raw_content is None
    assert fb.raw_activity is None
    assert fb.raw_matches is None
    assert fb.raw_athletes is None
    assert fb.ids is None
    assert fb.matches is None


def test_constructor_with_real_data(flyby_response):

    expected = json.loads(flyby_response)

    fb = Flyby(expected)

    assert fb.raw_content == expected
    assert fb.raw_activity == expected['activity']
    assert fb.raw_matches == expected['matches']
    assert fb.raw_athletes == expected['athletes']
    assert len(fb.ids) == 751
    assert len(fb.matches) == 751

    assert fb._distance_filter().sum() == 751
    assert fb._distance_filter(distance=100).sum() == 222
    assert fb._distance_filter(distance=100, tol=0.05).sum() == 68
    assert fb._distance_filter(distance=(90, 110)).sum() == 222

    assert len(fb.get_ids()) == 751
    assert len(fb.get_ids(distance=100)) == 222
    assert len(fb.get_ids(distance=100, tol=0.05)) == 68
    assert len(fb.get_ids(distance=(90, 110), tol=0.05)) == 222

    assert len(fb.matches_to_json()) == 751
    assert len(fb.matches_to_json(distance=100)) == 222

    assert len(fb.matches_to_list()) == 751
    assert len(fb.matches_to_list(distance=100)) == 222


@httpretty.activate
def test_flyby(flyby_response):

    test_id = 12345
    httpretty.register_uri(httpretty.GET,
                           "https://nene.strava.com/flyby/matches/{}".format(test_id),
                           body=flyby_response,
                           content_type="application/json")

    expected = json.loads(flyby_response)

    fb = flyby(test_id)

    assert fb.raw_content == expected
    assert fb.raw_activity == expected['activity']
    assert fb.raw_matches == expected['matches']
    assert fb.raw_athletes == expected['athletes']

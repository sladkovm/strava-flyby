import pytest
import json
import os
import httpretty
from flyby.flyby import Flyby


@pytest.fixture
def flyby_response():

    current_dir = os.path.dirname(os.path.abspath(__file__))

    with open(os.path.join(current_dir, 'flyby.json')) as f:

        rv = json.dumps(json.load(f))

    return rv


def test_constructor():

    fb = Flyby()

    assert fb.content is None
    assert fb.activity is None
    assert fb.matches is None
    assert fb.athletes is None


@httpretty.activate
def test_get(flyby_response):

    test_id = 12345
    httpretty.register_uri(httpretty.GET, "https://nene.strava.com/flyby/matches/{}".format(test_id),
                           body=flyby_response,
                           content_type="application/json")

    expected = json.loads(flyby_response)

    fb = Flyby()
    fb = fb.get(test_id)

    assert fb.content == expected
    assert fb.activity == expected['activity']
    assert fb.matches == expected['matches']
    assert fb.athletes == expected['athletes']
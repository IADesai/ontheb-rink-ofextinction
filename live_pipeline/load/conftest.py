import pytest


@pytest.fixture
def fake_row():
    return ['', 21, 'Carl Linnaeus', 'carl.linnaeus@lnhm.co.uk', '146)994-1635x35992', '2023-08-31 14:44:00+01:00',
            'Ficus', 'Ficus carica', '2023-08-31 16:20:15+01:00', 'Perennial', 13.055716804469082, 94.25274582786069,
            "full sun, part sun/part shade"]

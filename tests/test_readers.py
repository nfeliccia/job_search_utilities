from readers import collabera_reader, mission_staff_reader, tandymtech_reader, \
    tech_in_motion_reader, susquehanna_international as susquehanna_international_reader, jacobs_reader


def universal_tester(reader):
    """
    Tests the reader function.
    Args:
        reader: function to test

    Returns:
        Assertion: True or False

    """
    assertion_value = None
    try:
        reader(testmode=True)
        assertion_value = True
    except Exception as e:
        print(e)
        assertion_value = False
    assert assertion_value


def test_collabera_reader():
    universal_tester(collabera_reader.collabera_reader)


def test_mission_staff_reader():
    universal_tester(mission_staff_reader.mission_staff_reader)


def test_susquehanna_international_reader():
    universal_tester(susquehanna_international_reader.susquehanna_international_reader)


def test_tech_in_motion_reader():
    universal_tester(tech_in_motion_reader.tech_in_motion_reader)


def test_tandym_tech_reader():
    universal_tester(tandymtech_reader.tandym_tech_reader)


def test_jacobs_reader():
    universal_tester(jacobs_reader.jacobs_reader)


if __name__ == '__main__':
    test_collabera_reader()
    test_mission_staff_reader()
    test_susquehanna_international_reader()
    test_tech_in_motion_reader()
    test_tandym_tech_reader()

from readers import read_comcast, fedex_reader_uploader, aramark_reader

"""
This is a simple test to make sure testing a reader doesnt' fail.
"""


def test_reader(input_reader_function):
    """
    This is a simple tester which takes in a specific function and tests it.
    Args:
        input_reader_function:

    Returns:

    """
    reader_ok = True
    try:
        input_reader_function()
    except Exception as e:
        print("Error in read_comcast {}".format(e))
        reader_ok = False
    assert reader_ok is True


def test_multi_readers():
    reader_functions = [read_comcast, fedex_reader_uploader, aramark_reader]
    for reader_function in reader_functions:
        test_reader(reader_function)

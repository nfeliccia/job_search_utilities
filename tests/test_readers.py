from readers import sig_reader, collabera_reader


def test_susquehanna_international_reader():
    try:
        sig_reader.susquehanna_international_reader(testmode=True)
    except Exception as e:
        print(e)
        assert False
    else:
        assert True


def test_collabera_reader():
    try:
        collabera_reader.collabera_reader(testmode=True)
    except Exception as e:
        print(e)
        assert False
    else:
        assert True

def test_func(x):
    print(x)
    return {
        'original':x['value'],
        'new':x['value']**2
    }
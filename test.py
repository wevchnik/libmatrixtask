from libmatrixtask import *

'''
SOURCE_URL = 'https://pastebin.com/raw/KAqis9Fy'
TRAVERSAL = [
    10, 50, 90, 130,
    140, 150, 160, 120,
    80, 40, 30, 20,
    60, 100, 110, 70,
]

def test_get_matrix():
    assert asyncio.run(get_matrix(SOURCE_URL)) == TRAVERSAL
'''

result = asyncio.run(get_matrix('https://pastebin.com/raw/KAqis9Fy')) #original
#result = asyncio.run(get_matrix('https://pastebin.com/raw/AfvdJhZ9')) #test 1
#result = asyncio.run(get_matrix('https://pastebin.com/raw/2UKeUPqX')) #test 2

print (result)



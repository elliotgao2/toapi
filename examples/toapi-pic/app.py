from toapi import Api

from items.pexels import Pexels
from items.pixabay import Pixabay
from settings import MySettings

api = Api(settings=MySettings)
api.register(Pixabay)
api.register(Pexels)

if __name__ == '__main__':
    api.serve()


from os.path import exists, isfile, expanduser
from ConfigParser import SafeConfigParser, NoOptionError


class Config(object):

    SECTION = 'ypod'
    DEFAULT_PATH = expanduser('~/.ypod')

    MOUNT = 'mount'
#    DEFAULT_MOUNT = '/mnt/ipod'
    DEFAULT_MOUNT = '/media/andrew@acooke.org ipod'

    DB = 'db'
    DEFAULT_DB = 'sqlite://~/.ypod.db'
#    DEFAULT_DB = 'sqlite://:memory:'

    MP3 = 'mp3'
    DEFAULT_MP3 = expanduser('~/project/ypod/music')

    def __init__(self, mount=DEFAULT_MOUNT, db=DEFAULT_DB, mp3=DEFAULT_MP3):
        self.mount = mount
        self.db = db
        self.mp3 = mp3

    def from_config(self, scp):
        self.get_option(scp, Config.MOUNT)
        self.get_option(scp, Config.DB)
        self.get_option(scp, Config.MP3)

    def get_option(self, scp, name):
        try:
            setattr(self, name, scp.get(Config.SECTION, name))
        except NoOptionError:
            pass

    @staticmethod
    def read(path=DEFAULT_PATH):
        config = Config()
        if exists(path) and isfile(path):
            with open(path) as input:
                scp = SafeConfigParser.readfp(input, filename=path)
                config.from_conf(scp)
        return config


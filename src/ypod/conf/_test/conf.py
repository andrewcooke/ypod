
from unittest import TestCase
from ypod.conf import Config


class ConfTest(TestCase):

    def test_read_default(self):
        config = Config.read("/does not exist")
        assert config.db == "sqlite://~/.ypod.db", config.db
        assert config.mount == "/media/andrew@acooke.org ipod", config.mount


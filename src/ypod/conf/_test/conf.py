
from unittest import TestCase
from ypod.conf import Config


class ConfTest(TestCase):

    def test_read_default(self):
        config = Config.read("/does not exist")
        assert config.db == "~/.ypod.db"
        assert config.mount == "/mnt/ipod"



from unittest import TestCase

from gpod.gpod import itdb_device_set_sysinfo
from gpod.ipod import Database


class BasicTest(TestCase):

    def test_load(self):
        db = Database('/media/andrew@acooke.org ipod')
        itdb_device_set_sysinfo(db._itdb.device, "ModelNumStr", "xB150")
        db.import_file('/home/andrew/project/ypod/music/Various/Underground Communication/Bassnectar - 07 - Kick It Complex (Bassnectar remix).mp3')
        db.copy_delayed_files()
        db.close()

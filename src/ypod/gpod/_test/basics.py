
from unittest import TestCase

from gpod.gpod import itdb_device_set_sysinfo, ITDB_IPOD_GENERATION_CLASSIC_3
from gpod.ipod import Database


class BasicTest(TestCase):

    def test_load(self):
        db = Database('/media/andrew@acooke.org')
#        db = Database('/mnt/usb')
        itdb_device_set_sysinfo(db._itdb.device, "ModelNumStr", "C297")
#        itdb_device_set_sysinfo(db._itdb.device, "ModelNumStr", "xB150")
#        itdb_device_set_sysinfo(db._itdb.device, "ModelNumStr", ITDB_IPOD_GENERATION_CLASSIC_3)
#        db.import_file("/home/andrew/project/ypod/music/ZZ Top/Tres Hombres/ZZ Top - 01 - Waitin' for the Bus.mp3")
        db.import_file('/home/andrew/project/ypod/music/Various/Underground Communication/Bassnectar - 07 - Kick It Complex (Bassnectar remix).mp3')
        db.copy_delayed_files()
        db.close()


import unittest

from dsatest.bench import bench
from dsatest.tests.helpers import up_and_wait, get_address

@unittest.skipIf(not bench.links, "Empty link list")
class TestPing(unittest.TestCase):

    def setUp(self):
        links = bench.links

        for i, link in enumerate(links):
            up_and_wait(link)
            link.host_if.flush_addresses()
            link.host_if.add_address(get_address(i, "host", 24))
            link.target_if.flush_addresses()
            link.target_if.add_address(get_address(i, "target", 24))


    def tearDown(self):
        links = bench.links

        for i, link in enumerate(links):
            link.host_if.del_address(get_address(i, "host", 24))
            link.host_if.down()
            link.target_if.del_address(get_address(i, "target", 24))
            link.target_if.down()


    def test_port_ping_all(self):
        for i, link in enumerate(bench.links):
            addr = get_address(i, "target")
            link.host_if.ping(addr, count=1, deadline=10)


import unittest

from dsatest.bench import bench

@unittest.skipIf(not bench.links, "test requires at least 1 link")
class TestBridge(unittest.TestCase):

    def setUp(self):
        links = bench.links

        self.bridge = bench.target.add_bridge("br0")
        self.bridge.up()
        self.bridge.add_address("192.168.10.1/24")
        for i, link in enumerate(links, start=1):
           link.host_if.flush_addresses()
           self.bridge.add_interface(link.target_if)

    def tearDown(self):
        links = bench.links
        for i, link in enumerate(links, start=1):
            self.bridge.del_interface(link.target_if)
        self.bridge.down()
        bench.target.del_bridge(self.bridge)

    def test_bridge_ping_one(self):
        links = bench.links
        for i, link in enumerate(links, start=1):
            host_addr = "192.168.10.{}/24".format(str(i * 2))
            link.host_if.add_address(host_addr)
            """
            No deadline, since we need the bridge to learn our MAC address first
            """
            link.host_if.ping("192.168.10.1", count=1)
            link.host_if.flush_addresses()

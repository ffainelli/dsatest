import unittest

from dsatest.bench import bench

@unittest.skipIf(not bench.links, "test requires at least 1 link")
class TestMany(unittest.TestCase):
    bridges = []

    def setUp(self):
        links = bench.links

        for i, link in enumerate(links, start=0):
           link.host_if.flush_addresses()
           self.bridges.insert(i, bench.target.add_bridge("br{}".format(str(i))))
           self.bridges[i].add_address("192.168.1{}.1/24".format(str(i)))
           self.bridges[i].add_interface(link.target_if)
           self.bridges[i].up()

    def tearDown(self):
        links = bench.links
        for i, link in enumerate(links, start=0):
            self.bridges[i].del_interface(link.target_if)
            self.bridges[i].down()
            bench.target.del_bridge(self.bridges[i])

    def test_ping_many(self):
        links = bench.links
        for i, link in enumerate(links, start=0):
            host_addr = "192.168.1{}.2/24".format(str(i))
            link.host_if.flush_addresses()
            link.host_if.add_address(host_addr)
            link.host_if.ping("192.168.1{}.1".format(str(i)), count=1, deadline=1)
            link.host_if.flush_addresses()

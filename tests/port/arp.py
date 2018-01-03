
import unittest

from dsatest.bench import bench

class TestArp(unittest.TestCase):


    def setUp(self):
        links = bench.links
        if len(links) == 0:
            self.skipTest("Empty link list")

        for i, l in enumerate(links, start=1):
            l.host_if.flush_addresses()
            l.target_if.flush_addresses()

    def tearDown(self):
        pass

    def test_port_arp(self):
        links = bench.links

        for i, l in enumerate(links, start=1):
            host_addr = "192.168.10.{}/24".format(str(i * 2))
            target_addr = "192.168.10.{}/24".format(str(i * 2 + 1))

            l.host_if.add_address(host_addr)
            l.target_if.add_address(target_addr)

            host_addr = "192.168.10.{}".format(str(i * 2))
            target_addr = "192.168.10.{}".format(str(i * 2 + 1))

            l.host_if.ping(target_addr, count=1, deadline=10)
            host_resp = l.host_if.arp_get(target_addr)
            if host_resp["iface"] != l.host_if.get_name():
                raise ValueError("Interface mismatch. Got {}, expected {}".
                                format(l.host_if.get_name(), host_resp["iface"]))
            target_resp = l.target_if.arp_get(host_addr)
            if target_resp["iface"] != l.target_if.get_name():
                raise ValueError("Interface mismatch. Got {}, expected {}".
                                format(l.target_if.get_name(), target_resp["iface"]))
            l.host_if.flush_addresses()
            l.target_if.flush_addresses()

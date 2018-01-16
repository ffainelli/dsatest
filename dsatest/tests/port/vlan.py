
import unittest

from dsatest.bench import bench
from dsatest.tests.helpers import up_and_wait, get_address

@unittest.skipIf(not bench.links, "Empty link list")
class TestPingVlan(unittest.TestCase):

    VID_START = 0
    VID_END = 10

    def setUp(self):
        links = bench.links

        for i, link in enumerate(links):
            up_and_wait(link)
            link.host_if.flush_addresses()
            link.target_if.flush_addresses()
            for vid in range(TestPingVlan.VID_START, TestPingVlan.VID_END):
                link.host_if.add_vlan(vid)
                link.target_if.add_vlan(vid)


    def tearDown(self):
        links = bench.links

        for i, link in enumerate(links):
            for vid in range(TestPingVlan.VID_START, TestPingVlan.VID_END):
                link.target_if.del_vlan(vid)
                link.host_if.del_vlan(vid)
            link.host_if.down()
            link.target_if.down()


    def test_port_ping_vlan_all(self):
        for i, link in enumerate(bench.links):
            for vid in range(TestPingVlan.VID_START, TestPingVlan.VID_END):
                host_vlan = link.host_if.vlan_interfaces[vid]
                target_vlan = link.target_if.vlan_interfaces[vid]
                host_vlan.add_address(get_address(vid, "host", 24))
                host_vlan.up()
                target_vlan.add_address(get_address(vid, "target", 24))
                target_vlan.up()
                addr = get_address(vid, "target")
                host_vlan.ping(addr, count=1, deadline=10)
                host_vlan.flush_addresses()
                target_vlan.flush_addresses()
                host_vlan.down()
                target_vlan.down()

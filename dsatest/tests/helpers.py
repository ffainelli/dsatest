
import time

from dsatest.bench import Bridge, Link

def _expand_interfaces(interfaces, item, expand):
    if isinstance(item, Link):
        interfaces.extend((item.host_if, item.target_if))
    else:
        interfaces.append(item)

        if expand:
            if isinstance(item, Bridge):
                interfaces.extend(item.interfaces)


def up_and_wait(up_interfaces, monitored=None, expand=True):
    """
    Take an instance, or a list, of Interface, Bridge, or Link, and put it in
    the 'up' state, and wait for its operstate to become 'up'. One can wait on
    a different set of interfaces to become 'up' by passing
      monitored=[if1, if2]
    Note that by default, interfaces within a Bridge will also be up'ed when
    the bridge interface is up'ed. To prevent that, pass Expand=False.
    """
    interfaces = list()

    # accept a list or just one instance
    try:
        for item in up_interfaces:
            _expand_interfaces(interfaces, item, expand)
    except TypeError:
        _expand_interfaces(interfaces, up_interfaces, expand)

    for interface in interfaces:
        interface.up()

    if not monitored:
        monitored = interfaces

    timeout = 10
    while timeout:
        for interface in monitored:
            read_operstate_cmd = "cat /sys/class/net/{}/operstate".format(interface.name)
            ret, stdout, _ = interface.machine.execute(read_operstate_cmd)
            if ret == 0 and stdout == "up":
                monitored.remove(interface)

        if not monitored:
            return

        time.sleep(1)
        timeout = timeout - 1

    raise RuntimeError("some interfaces did not up within alloted period")

def get_address(offset, side, prefix_length=None):
    if side == "host":
        side = "1"
    elif side == "target":
        side = "2"
    else:
        raise ValueError("unexpected side")

    address = "192.168.{}.{}".format(str(10 + offset), side)
    if prefix_length:
        address = "{}/{}".format(address, prefix_length)

    return address



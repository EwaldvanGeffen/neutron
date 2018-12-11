# Copyright 2018 Red Hat, Inc.
#
#    Licensed under the Apache License, Version 2.0 (the "License"); you may
#    not use this file except in compliance with the License. You may obtain
#    a copy of the License at
#
#         http://www.apache.org/licenses/LICENSE-2.0
#
#    Unless required by applicable law or agreed to in writing, software
#    distributed under the License is distributed on an "AS IS" BASIS, WITHOUT
#    WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied. See the
#    License for the specific language governing permissions and limitations
#    under the License.

import errno
import socket

from neutron_lib import constants as n_constants

from neutron import privileged
from neutron.privileged.agent.linux import ip_lib


_IP_VERSION_FAMILY_MAP = {n_constants.IP_VERSION_4: socket.AF_INET,
                          n_constants.IP_VERSION_6: socket.AF_INET6}


@privileged.default.entrypoint
def add_tc_qdisc(device, namespace=None, **kwargs):
    """Add TC qdisc"""
    index = ip_lib.get_link_id(device, namespace)
    try:
        with ip_lib.get_iproute(namespace) as ip:
            ip.tc('replace', index=index, **kwargs)
    except OSError as e:
        if e.errno == errno.ENOENT:
            raise ip_lib.NetworkNamespaceNotFound(netns_name=namespace)
        raise


@privileged.default.entrypoint
def list_tc_qdiscs(device, namespace=None):
    """List all TC qdiscs of a device"""
    index = ip_lib.get_link_id(device, namespace)
    try:
        with ip_lib.get_iproute(namespace) as ip:
            return ip_lib.make_serializable(ip.get_qdiscs(index=index))
    except OSError as e:
        if e.errno == errno.ENOENT:
            raise ip_lib.NetworkNamespaceNotFound(netns_name=namespace)
        raise

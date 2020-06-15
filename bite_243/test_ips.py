import os
from pathlib import Path
from ipaddress import IPv4Network
from urllib.request import urlretrieve

import pytest

from ips import (ServiceIPRange, parse_ipv4_service_ranges,
                 get_aws_service_range)

URL = "https://bites-data.s3.us-east-2.amazonaws.com/ip-ranges.json"
TMP = os.getenv("TMP", "/tmp")
PATH = Path(TMP, "ip-ranges.json")
IP = IPv4Network('192.0.2.8/29')


@pytest.fixture(scope='module')
def json_file():
    """Import data into tmp folder"""
    urlretrieve(URL, PATH)
    return PATH


import dataclasses
import sys


@pytest.fixture(scope='module')
def regions(json_file):
    return parse_ipv4_service_ranges(json_file)


def test_ip_range_dataclass():
    service = ServiceIPRange('Service', 'Region', IP)
    assert isinstance(service.cidr, IPv4Network)
    assert str(service) == (
            "192.0.2.8/29 is allocated to the Service "
            "service in the Region region"
        )


@pytest.mark.xfail(raises=dataclasses.FrozenInstanceError)
def test_dataclass_is_frozen():
    service = ServiceIPRange('Service', 'Region', IP)
    service.service = 'New Service'


def test_ipv4_service_ranges(regions):
    assert len(regions) == 1886
    assert isinstance(regions[0], ServiceIPRange)


def test_aws_service_ranges(regions):
    range_ = get_aws_service_range('192.168.1.1', regions)
    assert range_ == []

    range_ = get_aws_service_range('18.201.1.5', regions)
    assert len(range_) == 2
    assert range_[0].region == 'eu-west-1'
    assert range_[1].service == 'EC2'


@pytest.mark.xfail(raises=ValueError)
def test_aws_service_range_with_network(regions):
    try:
        get_aws_service_range(IP, regions)
    except ValueError:
        err = sys.exc_info()
        if err[1].args[0] == 'Address must be a valid IPv4 address':
            raise ValueError('Address must be a valid IPv4 address')
        else:
            raise TypeError

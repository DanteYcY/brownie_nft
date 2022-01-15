from scripts.helpful_scripts import (
    LOCAL_BLOCKCHAIN_ENVIRONMENT,
    FORKED_LOCAL_ENVIRONMENTS,
    get_account,
)
from brownie import network
import pytest
from scripts.deploy_create import deploy_and_create


def test_can_create_simple_collectible():
    if network.show_active() not in LOCAL_BLOCKCHAIN_ENVIRONMENT:
        pytest.skip()
    simple_collectible = deploy_and_create()
    assert simple_collectible.ownerOf(0) == get_account()
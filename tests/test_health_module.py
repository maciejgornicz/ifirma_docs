# test_health_module.py
from ifirma_docs.modules.health import Health
from time import sleep


def test_singleton():
    health1 = Health()
    health2 = Health()
    assert health1 == health2


def test_start_living():
    health = Health(0.2)
    sleep(0.1)
    assert health.alive


def test_dying():
    health = Health(0.1)
    sleep(0.2)
    assert not health.alive


def test_hearbeat():
    health = Health(0.2)
    sleep(0.1)
    health.heartbeat()
    sleep(0.19)
    assert health.alive


def test_die_after_heartbeat():
    health = Health(0.2)
    sleep(0.1)
    health.heartbeat()
    sleep(0.21)
    assert not health.alive

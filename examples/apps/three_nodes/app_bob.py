from netqasm.sdk import EPRSocket
from netqasm.sdk.external import NetQASMConnection

from netqasm.logging import get_netqasm_logger

logger = get_netqasm_logger()


def main(app_config=None):
    epr_socket_alice = EPRSocket(
        remote_node_name="alice",
        epr_socket_id=0,
        remote_epr_socket_id=0
    )
    epr_socket_charlie = EPRSocket(
        remote_node_name="charlie",
        epr_socket_id=1,
        remote_epr_socket_id=1
    )

    node_name = app_config.node_name
    if node_name is None:
        node_name = app_config.app_name

    bob = NetQASMConnection(
        node_name=node_name,
        log_config=app_config.log_config,
        epr_sockets=[epr_socket_alice, epr_socket_charlie]
    )
    with bob:
        epr_alice = epr_socket_alice.recv()[0]
        m_alice = epr_alice.measure()

        bob.flush()

        epr_charlie = epr_socket_charlie.create()[0]
        m_charlie = epr_charlie.measure()

    logger.info(f"bob:      m_alice:  {m_alice}")
    logger.info(f"bob:      m_charlie:{m_charlie}")


if __name__ == "__main__":
    main()

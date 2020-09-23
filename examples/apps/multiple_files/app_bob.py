from netqasm.sdk import Qubit
from netqasm.logging import get_netqasm_logger
from netqasm.sdk.external import NetQASMConnection, Socket

from shared.myfuncs import custom_recv, custom_measure

logger = get_netqasm_logger()


def main(app_config=None):
    socket = Socket("bob", "alice", log_config=app_config.log_config)

    # Initialize the connection to the backend
    node_name = app_config.node_name
    if node_name is None:
        node_name = app_config.app_name

    bob = NetQASMConnection(
        node_name=node_name,
        log_config=app_config.log_config
    )
    with bob:
        q = Qubit(bob)
        custom_measure(q)

    socket.recv()
    custom_recv(socket)


if __name__ == "__main__":
    main()

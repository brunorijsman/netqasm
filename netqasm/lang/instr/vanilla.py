from dataclasses import dataclass

import numpy as np

from netqasm.util.quantum_gates import get_rotation_matrix

from . import core

# Explicit instruction types in the Vanilla flavour.


@dataclass
class GateXInstruction(core.SingleQubitInstruction):
    id: int = 20
    mnemonic: str = "x"

    def to_matrix(self) -> np.ndarray:
        return np.array([[0, 1], [1, 0]])


@dataclass
class GateYInstruction(core.SingleQubitInstruction):
    id: int = 21
    mnemonic: str = "y"

    def to_matrix(self) -> np.ndarray:
        return np.array([[0, -1j], [1j, 0]])


@dataclass
class GateZInstruction(core.SingleQubitInstruction):
    id: int = 22
    mnemonic: str = "z"

    def to_matrix(self) -> np.ndarray:
        return np.array([[1, 0], [0, -1]])


@dataclass
class GateHInstruction(core.SingleQubitInstruction):
    id: int = 23
    mnemonic: str = "h"

    def to_matrix(self) -> np.ndarray:
        X = GateXInstruction().to_matrix()
        Z = GateZInstruction().to_matrix()
        return (X + Z) / np.sqrt(2)  # type: ignore


@dataclass
class GateSInstruction(core.SingleQubitInstruction):
    id: int = 24
    mnemonic: str = "s"

    def to_matrix(self) -> np.ndarray:
        return np.array([[1, 0], [0, 1j]])


@dataclass
class GateKInstruction(core.SingleQubitInstruction):
    id: int = 25
    mnemonic: str = "k"

    def to_matrix(self) -> np.ndarray:
        Y = GateYInstruction().to_matrix()
        Z = GateZInstruction().to_matrix()
        return (Y + Z) / np.sqrt(2)  # type: ignore


@dataclass
class GateTInstruction(core.SingleQubitInstruction):
    id: int = 26
    mnemonic: str = "t"

    def to_matrix(self) -> np.ndarray:
        return np.array([[1, 0], [0, (1 + 1j) / np.sqrt(2)]])


@dataclass
class RotXInstruction(core.RotationInstruction):
    id: int = 27
    mnemonic: str = "rot_x"

    def to_matrix(self) -> np.ndarray:
        axis = [1, 0, 0]
        angle = self.angle_num.value * np.pi / 2**self.angle_denom.value
        return get_rotation_matrix(axis, angle)


@dataclass
class RotYInstruction(core.RotationInstruction):
    id: int = 28
    mnemonic: str = "rot_y"

    def to_matrix(self) -> np.ndarray:
        axis = [0, 1, 0]
        angle = self.angle_num.value * np.pi / 2**self.angle_denom.value
        return get_rotation_matrix(axis, angle)


@dataclass
class RotZInstruction(core.RotationInstruction):
    id: int = 29
    mnemonic: str = "rot_z"

    def to_matrix(self) -> np.ndarray:
        axis = [0, 0, 1]
        angle = self.angle_num.value * np.pi / 2**self.angle_denom.value
        return get_rotation_matrix(axis, angle)


@dataclass
class CnotInstruction(core.TwoQubitInstruction):
    id: int = 30
    mnemonic: str = "cnot"

    def to_matrix(self) -> np.ndarray:
        return np.array([[1, 0, 0, 0], [0, 1, 0, 0], [0, 0, 0, 1], [0, 0, 1, 0]])

    def to_matrix_target_only(self) -> np.ndarray:
        return np.array([[0, 1], [1, 0]])


@dataclass
class CphaseInstruction(core.TwoQubitInstruction):
    id: int = 31
    mnemonic: str = "cphase"

    def to_matrix(self) -> np.ndarray:
        return np.array([[1, 0, 0, 0], [0, 1, 0, 0], [0, 0, 1, 0], [0, 0, 0, -1]])

    def to_matrix_target_only(self) -> np.ndarray:
        return np.array([[1, 0], [0, -1]])


@dataclass
class ControlledRotZInstruction(core.ControlledRotationInstruction):
    # TODO It seems obvious that the id should be 32, but if we change this from 31 to 32 then
    #      any application that uses and epr_socket crashes with the following exception:
    #    
    # Error encountered while running the experiment
    # {'exception': 'CalledProcessError', 'message': 'NetQASM returned with exit status 1.', 'trace': 'Traceback (most recent call last):
    #   File "/Users/brunorijsman/.pyenv/versions/3.10.4/bin/netqasm", line 8, in <module>
    #     sys.exit(cli())
    #   File "/Users/brunorijsman/.pyenv/versions/3.10.4/lib/python3.10/site-packages/click/core.py", line 1130, in __call__
    #     return self.main(*args, **kwargs)
    #   File "/Users/brunorijsman/.pyenv/versions/3.10.4/lib/python3.10/site-packages/click/core.py", line 1055, in main
    #     rv = self.invoke(ctx)
    #   File "/Users/brunorijsman/.pyenv/versions/3.10.4/lib/python3.10/site-packages/click/core.py", line 1657, in invoke
    #     return _process_result(sub_ctx.command.invoke(sub_ctx))
    #   File "/Users/brunorijsman/.pyenv/versions/3.10.4/lib/python3.10/site-packages/click/core.py", line 1404, in invoke
    #     return ctx.invoke(self.callback, **ctx.params)
    #   File "/Users/brunorijsman/.pyenv/versions/3.10.4/lib/python3.10/site-packages/click/core.py", line 760, in invoke
    #     return __callback(*args, **kwargs)
    #   File "/Users/brunorijsman/.pyenv/versions/3.10.4/lib/python3.10/site-packages/netqasm/runtime/cli.py", line 330, in simulate
    #     simulate_application = importlib.import_module(
    #   File "/Users/brunorijsman/.pyenv/versions/3.10.4/lib/python3.10/importlib/__init__.py", line 126, in import_module
    #     return _bootstrap._gcd_import(name[level:], package, level)
    #   File "<frozen importlib._bootstrap>", line 1050, in _gcd_import
    #   File "<frozen importlib._bootstrap>", line 1027, in _find_and_load
    #   File "<frozen importlib._bootstrap>", line 1006, in _find_and_load_unlocked
    #   File "<frozen importlib._bootstrap>", line 688, in _load_unlocked
    #   File "<frozen importlib._bootstrap_external>", line 883, in exec_module
    #   File "<frozen importlib._bootstrap>", line 241, in _call_with_frames_removed
    #   File "/Users/brunorijsman/.pyenv/versions/3.10.4/lib/python3.10/site-packages/netqasm/sdk/external.py", line 34, in <module>
    #     from squidasm.nqasm.multithread import (
    #   File "/Users/brunorijsman/.pyenv/versions/3.10.4/lib/python3.10/site-packages/squidasm/__init__.py", line 3, in <module>
    #     raise NotImplementedError("SquidASM is still WIP and this is currently just a placeholder package")
    # NotImplementedError: SquidASM is still WIP and this is currently just a placeholder package
    #
    id: int = 31
    mnemonic: str = "crot_z"

    def to_matrix(self) -> np.ndarray:
        tm = self.to_matrix_target_only()
        return np.array(
            [
                [1, 0, 0, 0],
                [0, 1, 0, 0],
                [0, 0, tm[0][0], tm[0][1]],
                [0, 0, tm[1][0], tm[1][1]],
            ]
        )

    def to_matrix_target_only(self) -> np.ndarray:
        axis = [0, 0, 1]
        angle = self.angle_num.value * np.pi / 2**self.angle_denom.value
        return get_rotation_matrix(axis, angle)


@dataclass
class MovInstruction(core.TwoQubitInstruction):
    """Move source qubit to target qubit (target is overwritten)"""

    id: int = 41
    mnemonic: str = "mov"

    def to_matrix(self) -> np.ndarray:
        # NOTE: Currently this is represented as a full SWAP.
        return np.array([[1, 0, 0, 0], [0, 0, 1, 0], [0, 1, 0, 0], [0, 0, 0, 1]])

    def to_matrix_target_only(self) -> np.ndarray:  # type: ignore
        # NOTE: The mov instruction is not meant to be viewed as control-target gate.
        # Therefore, it is OK to not explicitly define a matrix.
        return None  # type: ignore

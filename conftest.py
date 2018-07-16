import pytest

import magma
magma.set_mantle_target('spartan6')

@pytest.fixture(autouse=True)
def bit1_test():
    """
    Clear the circuit cache before running, allows name reuse across tests
    without collisions
    """
    import magma.config
    magma.config.set_compile_dir('callee_file_dir')

    from magma import clear_cachedFunctions
    clear_cachedFunctions()

    from magma.circuit import magma_clear_circuit_cache
    magma_clear_circuit_cache()



import pytest

from swan.common.utils import parse_resource_string


@pytest.mark.parametrize("test_input,expected_output", [
    (
            'CPU only · 4 vCPU · 4 GiB',
            {"cpu": 4, "memory": 4, "gpu_count": 0, "gpu_model": None, "storage": 30}
    ),
    (
            'Nvidia 3070 Ti · 12 vCPU · 64 GiB',
            {"cpu": 12, "memory": 64, "gpu_count": 1, "gpu_model": "Nvidia 3070 Ti", "storage": 30}
    ),
    (
            'Quadro RTX 8000 · 16 vCPU · 128 GiB',
            {"cpu": 16, "memory": 128, "gpu_count": 1, "gpu_model": "Quadro RTX 8000", "storage": 30}
    ),
])
def test_parse_resource_string_success(test_input, expected_output):
    """Test that the function correctly parses a resource string with valid input."""
    result = parse_resource_string(test_input)
    assert result == expected_output
    assert result['storage'] == 30


def test_parse_resource_string_invalid_cpu_raises_error():
    """Test that the function raises an error when CPU value is invalid."""
    invalid_input = 'CPU only · abc vCPU · 4 GiB'
    with pytest.raises(ValueError):
        parse_resource_string(invalid_input)


def test_parse_resource_string_invalid_memory_raises_error():
    """Test that the function raises an error when memory value is invalid."""
    invalid_input = 'CPU only · 4 vCPU · abc GiB'
    with pytest.raises(ValueError):
        parse_resource_string(invalid_input)

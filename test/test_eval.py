import subprocess
import xarray as xr
import numpy as np
import pytest


@pytest.fixture
def dummy_input_file(tmp_path):
    """
    Fixture to create a dummy NetCDF input file.
    """
    dummy_data = xr.Dataset(
        {"temperature": (("lat", "lon"), np.random.rand(10, 10))},
        coords={
            "lat": np.linspace(-90, 90, 10),
            "lon": np.linspace(0, 360, 10, endpoint=False),
        },
    )
    input_file = tmp_path / "input.nc"
    dummy_data.to_netcdf(input_file)
    return input_file


@pytest.fixture
def output_file_path(tmp_path):
    """
    Fixture to provide an output file path.
    """
    return tmp_path / "output.nc"


def test_integration_with_dummy_files(dummy_input_file, output_file_path):
    """
    Integration test using fixtures for input and output files.
    """
    result = subprocess.run(
        ["python", "main.py", str(dummy_input_file), str(output_file_path)],
        capture_output=True,
        text=True,
    )

    # Check it ran successfully
    assert result.returncode == 0, f"stderr: {result.stderr}"

    # Check output file was created and is valid
    assert output_file_path.exists()

    # Check the contents of the output file
    ds_out = xr.open_dataset(output_file_path)
    assert "expected_variable" in ds_out.variables

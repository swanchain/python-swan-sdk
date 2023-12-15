import requests
from mock.mock import Mock, MagicMock, patch

from src.api.stats import get_general_stats


class TestStats:
    def test_returns_general_stats_if_request_successful(self):
        # Mock the requests.get method to return a successful response
        mock_response = Mock()
        mock_response.raise_for_status.return_value = None
        mock_response.json.return_value = {
            "total_jobs": 100,
            "running_jobs": 50,
            "leading_jobs": 20,
        }
        requests.get = MagicMock(return_value=mock_response)

        # Call the function under test
        result = get_general_stats()

        # Assert that the result is a dictionary containing general statistics
        assert isinstance(result, dict)
        assert "total_jobs" in result
        assert "running_jobs" in result
        assert "leading_jobs" in result

    def test_invalid_data_response(self):
        # Mock the requests.get method to return a response with invalid data
        with patch("requests.get") as mock_get:
            mock_get.return_value.json.return_value = "invalid_data"

            # Call the function under test
            result = get_general_stats()

            # Assert that the result is an error message
            assert result == "invalid_data"

    def test_missing_fields(self):
        # Mock the requests.get method to return a response with missing fields
        with patch("requests.get") as mock_get:
            mock_response = Mock()
            mock_response.json.return_value = {
                "total_jobs": 100,
                "running_jobs": 50,
                "leading_jobs": 20,
                "job_duration": None,
                "total_users": None,
                "space_builders": None,
            }
            mock_get.return_value = mock_response

            # Call the function under test
            result = get_general_stats()

            # Assert that the result is equal
            assert result == {
                "total_jobs": 100,
                "running_jobs": 50,
                "leading_jobs": 20,
                "job_duration": None,
                "total_users": None,
                "space_builders": None,
            }


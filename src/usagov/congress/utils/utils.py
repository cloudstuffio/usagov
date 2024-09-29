from typing import Any, Dict


def filter_parameters(parameters: Dict[str, Any]) -> Dict[str, Any]:
    """
    Filter out the parameters that are not required for the API request.

    Args:
        parameters (dict): A dictionary containing the parameters for the API request.

    Returns:
        dict: A dictionary containing only the required parameters for the API request.
    """
    parameters = {
        key: value for key, value in parameters.items() if value is not None
    }

    return parameters

from flask import request, jsonify


def validate_json(required_fields):
    """
    Validates incoming JSON payloads for required fields.

    Args:
        required_fields (list): A list of fields expected in the JSON payload.

    Returns:
        tuple: (data, error_response, status_code)
            - data (dict): The parsed JSON data if valid, otherwise None.
            - error_response (Response): Flask JSON response with an error message.
            - status_code (int): HTTP status code corresponding to the error.
    """
    data = request.get_json()
    if not data:
        return None, jsonify({'error': 'Invalid or missing JSON payload'}), 400
    for field in required_fields:
        if field not in data:
            return None, jsonify({'error': f'Missing field: {field}'}), 400
    return data, None, None
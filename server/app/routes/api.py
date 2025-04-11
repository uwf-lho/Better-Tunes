from flask import Blueprint, request, jsonify, current_app

from app.utils.tools import validate_json

# Create a Blueprint for API routes
api_bp = Blueprint('api', __name__)

@api_bp.route('/search', methods=['POST'])
def search():
    """
    Endpoint to perform a search using the Spotify service.
    Requires 'query_type' and 'payload' in the JSON payload.

    Returns:
        JSON: Search results from the Spotify service.
    """
    data, error_response, status_code = validate_json(['query_type', 'payload', 'username'])
    if error_response:
        return error_response, status_code

    search_results = current_app.spotify_service.search(
        query_type=data['query_type'],
        query=data['payload'],
        username=data['username']
    )
    return jsonify(search_results)

@api_bp.route('/update-song', methods=['POST'])
def update_song():
    """
    Endpoint to update a song's metadata by liking or disliking it.
    Requires 'song_id' and exactly one of 'like' or 'dislike' to be True.

    Returns:
        JSON: The result of the like or dislike operation.
    """

    action_to_function = {
        'like': current_app.metadata_service.add_like_to_song,
        'dislike': current_app.metadata_service.add_dislike_to_song,
        'unlike': current_app.metadata_service.unlike_song,
        'undislike': current_app.metadata_service.undislike_song,
    }

    data, error_response, status_code = validate_json(['songId', 'action', 'userId'])
    if error_response:
        return error_response, status_code

    songId, action, userId = data['songId'], data['action'], data['userId']

    print(action)

    # Choose the appropriate service based on action
    service = action_to_function.get(action, None)

    if service is None:
        return jsonify({'msg': 'Invalid action.'}), 400

    return jsonify(service(song_id=songId, user_id=userId))

# @api_bp.route('/get-song-metadata', methods=['POST'])
# def get_song_metadata():
#     """
#     Endpoint to retrieve metadata for a specific song.
#     Requires 'song_id' in the JSON payload.
#
#     Returns:
#         JSON: Metadata information about the specified song.
#     """
#     data, error_response, status_code = validate_json(['song_id'])
#     if error_response:
#         return error_response, status_code
#
#     metadata = current_app.metadata_service.get_song_metadata(song_id=data['song_id'])
#     return jsonify(metadata)

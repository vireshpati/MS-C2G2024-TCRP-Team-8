from flask import Flask, request, jsonify
from sqlite.py import *

app = Flask(__name__)

# method to create a post to request help
@app.route('/posts', methods=['POST'])
def create_post():
    data = request.json
    result = sql_create_post(data)
    return jsonify(result), 201

# method to comment on a request post
# need fields: post_uid, comment_author, comment_content
@app.route('/posts/<int:post_id>/comments', methods=['POST'])
def create_comment(post_id):
    data = request.json
    result = sql_create_comment(post_id, data)
    return jsonify(result), 201

# method to display requests
# sorts by post_creation_date, newest to oldest.
@app.route('/bulletin', methods=['GET'])
def load_bulletin():
    result = query_request()
    return jsonify(result), 200

# method to display requests
# sort by post_creation_date, confirm_by, date_help_needed. asc or des.
# can filter by tag.
# need fields: 'sort_by'=(post_creation_date, confirm_by, date_help_needed, none), 'order'=(asc, desc), 
# 'tag'=('babysitting', 'tutoring', 'pickupchild', 'mealshare', 'needride', 'others', none), 
@app.route('/bulletin/sort', methods=['GET'])
def sort_bulletin():
    data = request.json
    result = sql_load_bulletin(data)
    return jsonify(result), 200

@app.route('/posts/<int:post_id>', methods=['DELETE'])
def delete_post(post_id):
    result = sql_delete_post(post_id)
    return jsonify(result), 204

if __name__ == '__main__':
    app.run(debug=True)

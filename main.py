from apiflask import APIFlask
from flask import jsonify, request, abort
from db_crud import *
from flask_cors import CORS
app = APIFlask(__name__, docs_path='/docs')
CORS(app)

limit = 50

# get 
@app.route('/api/posts', methods=['GET'])
def fetch_posts():
    return jsonify(get_posts(amount=limit))

@app.route('/api/posts/<int:post_id>', methods=['GET'])
def fetch_post_from_post_id(post_id):

    if get_post(post_id):
        return jsonify({"post": get_post(post_id), "comments": get_comments(post_id)})
    else:
        abort(404)

@app.route('/api/user/<int:user_id>', methods=['GET'])
def fetch_user(user_id):
    if not find_user_from_id(user_id):
        abort(404)

    return jsonify({"user": find_user_from_id(user_id)})

@app.route('/api/user/<int:user_id>/posts', methods=['GET'])
def fetch_posts_from_user_id(user_id):
    if not find_user_from_id(user_id):
        abort(404)

    return jsonify(get_posts(amount=limit, user_id=user_id))

# post
@app.route('/api/post', methods=['POST'])
def post():
    data = request.json
    content = data.get('content')
    user = data.get('user')

    if not content or not user:
        abort(400)

    create_post(user, content)

    return jsonify({"status": "success", "message": "Post created"}), 201

@app.route('/api/comment/<int:post_id>', methods=['POST'])
def comment(post_id):
    data = request.json
    content = data.get('content')
    user = data.get('user')

    if get_post(post_id):
        create_comment(user, content, post_id)
        return jsonify({"status": "success", "message": "Post created"}), 201
    else:
        abort(404)


app.run(debug=True, port=5000)
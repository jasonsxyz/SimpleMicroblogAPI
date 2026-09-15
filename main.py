from flask import Flask, jsonify, request, abort
from db_crud import *
from flask_cors import CORS
app = Flask(__name__)
CORS(app)
# get 
@app.route('/api/posts', methods=['GET'])
def fetch_posts():
    from_user = request.args.get('user')
    select = request.args.get('select')

    if select:
        if get_post(select):
            return jsonify({"post": get_post(select)}, {"comments": get_comments(select)})

    if not from_user:
        posts = get_posts(50, None)
    else:
        if not find_user_from_id(from_user):
            abort(404)
        posts = get_posts(50, from_user)

    return jsonify(posts)

@app.route('/api/posts/<int:post_id>', methods=['GET'])
def fetch_post_from_id(post_id):

    if get_post(post_id):
        return jsonify({"post": get_post(post_id), "comments": get_comments(post_id)})
    else:
        abort(404)

@app.route('/api/user/<int:user_id>', methods=['GET'])
def fetch_user(user_id):
    if not find_user_from_id(user_id):
        abort(404)

    return jsonify({"user": find_user_from_id(user_id)})

# post
@app.route('/api/post', methods=['POST'])
def post():
    data = request.json
    content = data.get('content')
    user = data.get('user')
    post = data.get('post_id')

    if post:
        if get_post(post):
            create_comment(user, content, post)
            return jsonify({"status": "success", "message": "Post created"}), 201
        else:
            return jsonify({"post_id": post})


    if not content or not user:
        abort(400)

    create_post(user, content)

    return jsonify({"status": "success", "message": "Post created"}), 201


app.run(debug=True, port=5000)
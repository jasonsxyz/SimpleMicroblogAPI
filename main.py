from flask import Flask, jsonify, request, abort
from db_crud import *
app = Flask(__name__)

@app.route('/api/posts', methods=['GET'])
def fetch_posts():
    from_user = request.args.get('user')

    if not from_user:
        posts = get_posts(50, None)
    else:
        if not find_user_from_id(from_user):
            abort(404)
        posts = get_posts(50, from_user)

    return jsonify(posts)

@app.route('/api/user', methods=['GET'])
def fetch_user():
    user_id = request.args.get('id')

    if not find_user_from_id(user_id):
        abort(404)

    return jsonify(find_user_from_id(user_id))


app.run(debug=True, port=5000)
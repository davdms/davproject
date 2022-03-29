from flask import Flask
from flask import render_template
from flask import redirect
from flask import url_for
from flask import request
from flask import json

app = Flask(__name__)

def get_posts():
    with open('data.json') as f:
        all_posts = json.load(f)
    return all_posts

@app.route('/')
def home():
    return redirect(url_for('posts'))

@app.route('/posts')
def posts():
    all_posts = get_posts()
    if request.args.get('q'):
        q = request.args.get('q')
        filtered_posts = []
        for val in all_posts:
            if q in val['title'] or q in val['description']:
                filtered_posts.append(val)
        return render_template('posts.html', posts=filtered_posts, q=q)
    return render_template('posts.html', posts=all_posts)

@app.route("/post/<int:post_id>")
def post(post_id):
    all_posts = get_posts()
    for val in all_posts:
        if val['post_id'] == post_id:
            return render_template('post.html', thepost=val)
    return None

if __name__ == "__main__":
    app.run()




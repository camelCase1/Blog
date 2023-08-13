from flask import Flask, render_template, request, redirect, url_for
import psycopg2

app = Flask(__name__)

# Database setup
conn = psycopg2.connect(
    dbname="blog",
    user="postgres",
    password="",
    host="localhost",
    port="5432"
)
cursor = conn.cursor()
cursor.execute('''
    CREATE TABLE IF NOT EXISTS blog_post (
        id SERIAL PRIMARY KEY,
        title TEXT,
        description TEXT,
        image_url TEXT
    )
''')
conn.commit()
conn.close()


@app.route('/add_post')
def index():
    return render_template('add_post.html')


@app.route('/submit_post', methods=['POST'])
def submit_post():
    title = request.form['title']
    description = request.form['description']
    image_url = request.form['image_url']

    conn = psycopg2.connect(
        dbname="blog",
        user="postgres",
        password="",
        host="localhost",
        port="5432"
    )
    cursor = conn.cursor()
    cursor.execute('INSERT INTO blog_post (title, description, image_url) VALUES (%s, %s, %s) RETURNING id',
                   (title, description, image_url))
    # Fetch the ID of the newly inserted post
    new_post_id = cursor.fetchone()[0]
    conn.commit()
    conn.close()

    # Redirect to the view_post route
    return redirect(url_for('view_post', post_id=new_post_id))


@app.route('/')
def blog_list():
    conn = psycopg2.connect(
        dbname="blog",
        user="postgres",
        password="",
        host="localhost",
        port="5432"
    )
    cursor = conn.cursor()
    cursor.execute('SELECT id, title, description, image_url FROM blog_post')
    blog_posts = cursor.fetchall()
    conn.close()

    return render_template('index.html', blog_posts=blog_posts)


@app.route('/view_post/<int:post_id>')
def view_post(post_id):
    conn = psycopg2.connect(
        dbname="blog",
        user="postgres",
        password="",
        host="localhost",
        port="5432"
    )
    cursor = conn.cursor()
    cursor.execute(
        'SELECT title, description, image_url FROM blog_post WHERE id = %s', (post_id,))
    post = cursor.fetchone()
    conn.close()

    return render_template('view_post.html', post=post)


if __name__ == '__main__':
    app.run(debug=True)

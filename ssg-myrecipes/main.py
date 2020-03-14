import os
import codecs
from datetime import datetime
from jinja2 import Environment, PackageLoader
from markdown2 import markdown

# hvar eru Markdown skjölin og skilgreining CSV gagna (yaml)
POSTS = {}

for markdown_post in os.listdir('content'):
    file_path = os.path.join('content', markdown_post)

    with open(file_path, 'r') as file:
        POSTS[markdown_post] = markdown(file.read(), extras=['metadata'])

# Uppröðun pósta eftir dagsetningu - nýjast efst
POSTS = {
    post: POSTS[post] for post in sorted(POSTS, key=lambda post: datetime.strptime(POSTS[post].metadata['date'], '%Y-%m-%d'), reverse=True)
}

# Samsetning Markdown í Jinja template
env = Environment(loader=PackageLoader('main', 'templates', 'Environment'))
index_template = env.get_temmplate('index.html')
home_template = env.get_template('bread.html')
post_template = env.get_template('post.html')

posts_metadata = [POSTS[post].metadata for post in POSTS]
tags = [post['tags'] for post in posts_metadata]
home_html = home_template.render(posts=posts_metadata, tags=tags)

# forsíðan (er ekki með MD post rendiringu)
index_html = index_template.render()

# brauðuppskriftir
posts_metadata = [POSTS[post].metadata for post in POSTS]
tags = [post['tags'] for post in posts_metadata]
bread_html = bread_template.render(posts=posts_metadata, tags=tags)

# Forsíðan með íslenskum stöfum
with open('../recipes4/index.html', 'w', encoding='utf-8') as file:
    file.write(index_html)

# brauðsíðan
with open('../recipes4/bread.html', 'w') as file:
    file.write(home_html)

# Póstar - uppskriftir
for post in POSTS:
    post_metadata = POSTS[post].metadata

    post_data = {
        'content': POSTS[post],
        'title': post_metadata['title'],
        'date': post_metadata['date'],
        'thumbnail': post_metadata['thumbnail']
    }
    
    # post_file_path - slóðin að uppfskriftunum
    post_html = post_template.render(post=post_data)
    post_file_path = '../recipes4/posts/{slug}.html'.format(slug=post_metadata['slug'])

    os.makedirs(os.path.dirname(post_file_path), exist_ok=True)
    with open(post_file_path, 'w') as file:
        file.write(post_html)


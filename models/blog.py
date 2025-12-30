from extensions import db


blog_category = db.Table('blog_category',
                       db.Column('blog_id', db.Integer, db.ForeignKey('blog.id')),
                       db.Column('category_id', db.Integer, db.ForeignKey('category.id'))
                       )

blog_tag = db.Table('blog_tag',
                       db.Column('blog_id', db.Integer, db.ForeignKey('blog.id')),
                       db.Column('tag_id', db.Integer, db.ForeignKey('tag.id'))
                       )


class Blog(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    uuid = db.Column(db.Integer, unique=True)
    title = db.Column(db.String(300))
    author = db.Column(db.String(300))
    body = db.Column(db.String(10000))
    date_created = db.Column(db.String(50))
    date_scheduled = db.Column(db.String(50))
    date_published = db.Column(db.String(50))
    status = db.Column(db.String(50))
    vol_issue = db.Column(db.String(50))
    cta_text = db.Column(db.String(20))
    cta_link = db.Column(db.String(200))
    category = db.relationship('Category', secondary=blog_category, backref='blogs')
    tag = db.relationship('Tag', secondary=blog_tag, backref='blogs')
    comments = db.relationship('Comment', backref='blog')

    def __repr__(self):
        return f'{self.title}, {self.author}'


class Category(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(50))
    description = db.Column(db.String(200))

    def __repr__(self):
        return f'{self.name}'


class Tag(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(50))

    def __repr__(self):
        return f'{self.name}'


class Comment(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    member_id = db.Column(db.Integer)
    body = db.Column(db.String(1000))
    timestamp = db.Column(db.String(100))
    replies = db.relationship('Reply', backref='comment')
    blog_id = db.Column(db.Integer, db.ForeignKey('blog.id'))

    def __repr__(self):
        return f'{self.body}'


class Reply(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    member_id = db.Column(db.Integer)
    body = db.Column(db.String(1000))
    timestamp = db.Column(db.String(100))
    comment_id = db.Column(db.Integer, db.ForeignKey('comment.id'))

    def __repr__(self):
        return f'{self.body}'

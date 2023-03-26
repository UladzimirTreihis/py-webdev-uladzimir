from app import db
from app.models import Role, User, Post, Comment
from py_tweet import app as application


def add_data(db, Role, User, Post, Comment):

    print('deleting old data')
    db.drop_all()
    db.create_all()
    print('adding Admin and User roles')
    admin_role = Role(role="Admin")
    user_role = Role(role="User")
    db.session.add_all([admin_role, user_role])
    db.session.commit()
    print("adding Admin and User users")
    admin_user = User(username='admin', email='admin@example.com', password='admin', role_id=1)
    normal_user = User(username='user', email='user@example.com', password='user', role_id=2)
    db.session.add_all([admin_user, normal_user])
    db.session.commit()
    print("adding Posts")
    post1 = Post(content="Post 1 from Admin", user_id=1)   
    post2 = Post(content="Post 2 from Admin", user_id=1)    
    post3 = Post(content="Post 3 from Admin", user_id=1)    
    post4 = Post(content="Post 4 from Admin", user_id=1)     
    post5 = Post(content="Post 1 from User", user_id=2)  
    post6 = Post(content="Post 2 from User", user_id=2)  
    post7 = Post(content="Post 3 from User", user_id=2)  
    post8 = Post(content="Post 4 from User", user_id=2)  
    db.session.add_all([post1, post2, post3, post4, post5, post6, post7, post8])
    db.session.commit()
    print("adding Comments")
    com1 = Comment(body='Comment 1', post_id=post1.id, user_id=admin_user.id)
    com2 = Comment(body='Comment 2', post_id=post1.id, user_id=admin_user.id)
    com3 = Comment(body='Comment 3', post_id=post2.id, user_id=admin_user.id)
    com4 = Comment(body='Comment 4', post_id=post2.id, user_id=admin_user.id)
    com5 = Comment(body='Comment 5', post_id=post5.id, user_id=normal_user.id)
    com6 = Comment(body='Comment 6', post_id=post5.id, user_id=normal_user.id)
    com7 = Comment(body='Comment 7', post_id=post6.id, user_id=normal_user.id)
    com8 = Comment(body='Comment 8', post_id=post6.id, user_id=normal_user.id)
    db.session.add_all([com1, com2, com3, com4, com5, com6, com7, com8])
    db.session.commit()

    return None


with application.app_context():
    add_data(db, Role, User, Post, Comment)

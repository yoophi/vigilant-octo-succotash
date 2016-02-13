from flask.ext.fixtures import load_fixtures

from sqlalchemy.exc import IntegrityError

from suda import db
from suda.models import User
from tests import ModelTestCase

dataset = [
    dict(
        model='suda.models.User',
        records=[
            dict(
                id=1,
                username=u'suda@test.com',
                name=u'suda',
                password=u'secret'
            ),
            dict(
                id=2,
                username=u'user1@test.com',
                name=u'user1',
                password=u'secret'
            ),
            dict(
                id=3,
                username=u'user2@test.com',
                name=u'user2',
                password=u'secret'
            ),
            dict(
                id=4,
                username=u'user3@test.com',
                name=u'user3',
                password=u'secret'
            ),
        ]
    ),
    dict(
        model='suda.models.Follow',
        records=[
            dict(
                user_id=1,
                follower_id=2,
            )
        ]
    ),
]


class FollowModelTest(ModelTestCase):
    def test_get_followers(self):
        load_fixtures(db, dataset)

        u1 = User.query.get(1)
        u2 = User.query.get(2)

        followers = u1.get_followers()
        self.assertEqual(1, len(followers), 'user has one follower')
        self.assertIsInstance(followers[0], User, 'followers is list of <User> instances')
        self.assertEqual(followers[0].id, 2, '<User 2> follows <User 1>')

        followings = u2.get_followings()
        self.assertEqual(1, len(followings), 'user has one following')
        self.assertIsInstance(followings[0], User, 'followings is list of <User> instances')
        self.assertEqual(followings[0].id, 1, '<User 1> follows <User 1>')

    def test_add_follower(self):
        load_fixtures(db, dataset)

        user = User.query.get(1)
        user.add_follower(User.query.get(3))
        db.session.add(user)
        db.session.commit()

        followers = user.get_followers()
        self.assertEqual(2, len(followers), 'user has two follower')

        user.add_follower(User.query.get(2))

        with self.assertRaises(IntegrityError):
            db.session.add(user)
            db.session.commit()

        self.assertEqual(2, len(followers), 'user has two follower')

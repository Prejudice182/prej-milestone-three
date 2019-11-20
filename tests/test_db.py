import os
import unittest
from bson import ObjectId

from application import create_app, mongo


class DBTests(unittest.TestCase):
    def setUp(self):
        app = create_app('config.TestConfig')
        mongo.init_app(app)
        self.app = app.test_client()
        mongo.db.favourites.remove()

    def tearDown(self):
        pass

    def addFav(self, entry, eType, name, reason):
        return self.app.post('/add-favourite', data=dict(entry_name=entry, entry_type=eType, username=name, reason=reason), follow_redirects=True)

    def delFav(self, entry_id):
        return self.app.post(f'/delete-fav/{entry_id}', follow_redirects=True)

    def editFav(self, entry_id, username, reason):
        return self.app.post(f'/edit-fav/{entry_id}', data=dict(username=username, reason=reason), follow_redirects=True)

    def test_valid_add_favourite(self):
        response = self.addFav('The Great Escape', 'movie',
                               'Prejudice', 'Blah blah')
        self.assertEqual(response.status_code, 200)
        self.assertIn(b'Favourite saved!', response.data)

    def test_invalid_add_favourite(self):
        response = self.addFav('The Great Escape', 'movie',
                               'Prejudice', 'Blah blah')
        self.assertEqual(response.status_code, 200)
        response = self.addFav('The Great Escape', 'movie',
                               'Prejudice', 'Blah blah')
        self.assertIn(b'Someone already added that one!', response.data)

    def test_valid_delete_favourite(self):
        response = self.addFav('The Newsroom', 'series',
                               'Prejudice', 'Blah blah')
        self.assertIn(b'Favourite saved', response.data)
        entry = mongo.db.favourites.find_one(
            {'Title': 'The Newsroom'}, {'_id': 1})
        self.assertIs(type(entry), dict)
        response = self.delFav(entry['_id'])
        self.assertIn(b'Favourite deleted!', response.data)

    def test_invalid_delete_favourite(self):
        response = self.delFav(ObjectId(b'random12byte'))
        self.assertIn(b'No record with that ID found!', response.data)


if __name__ == '__main__':
    unittest.main()

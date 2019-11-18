import os
import unittest

from application import create_app


class BasicTests(unittest.TestCase):
    def setUp(self):
        app = create_app('config.TestConfig')
        self.app = app.test_client()

    def tearDown(self):
        pass

    def addFav(self, entry, eType, name, reason):
        return self.app.post('/add-favourite', data=dict(
            entry_name=entry,
            entry_type=eType,
            username=name,
            reason=reason
        ), follow_redirects=True)

    def test_main_page(self):
        response = self.app.get('/', follow_redirects=True)
        self.assertEqual(response.status_code, 200)

    def test_view_all_valid(self):
        response = self.app.get('/view-all/movies', follow_redirects=True)
        self.assertEqual(response.status_code, 200)
        response = self.app.get('/view-all/tvshows', follow_redirects=True)
        self.assertEqual(response.status_code, 200)

    def test_view_all_invalid(self):
        response = self.app.get('/view-all/fake-name', follow_redirects=True)
        self.assertEqual(response.status_code, 404)

    def test_404(self):
        response = self.app.get('/this-doesnt-exist', follow_redirects=True)
        self.assertEqual(response.status_code, 404)


if __name__ == '__main__':
    unittest.main()

import unittest
import mock
from wsgiref.util import setup_testing_defaults
import core


class CoreTests(unittest.TestCase):


    def test_empty(self):
        rot = core.BanRot([])
        banner = rot.next_banner(('cat1', 'cat2'))
        self.assert_(banner is None)


    def test_simple_rotation(self):
        rot = core.BanRot([('/1', 10, ('cat1', 'cat2')), ('/2', 10, ('cat1', 'cat3'))])
        banner1 = rot.next_banner(('cat1',))
        self.assert_(banner1 is not None)
        banner2 = rot.next_banner(('cat1',))
        self.assert_(banner2 is not None)
        self.assert_(banner1.url != banner2.url)
        banner3 = rot.next_banner(('cat1',))
        self.assert_(banner3 is not None)
        self.assert_(banner1.url == banner3.url)


    def test_cat_priority(self):
        rot = core.BanRot([('/1', 3, ('cat1',)), ('/2', 2, ('cat2',))])
        banner = rot.next_banner(('cat1', 'cat2'))
        self.assertEqual(banner.url, '/1')
        rot.next_banner(('cat1',))
        banner = rot.next_banner(('cat1', 'cat2'))
        self.assertEqual(banner.url, '/2')


class AppTests(unittest.TestCase):


    def setUp(self):
        self.patcher = mock.patch('core.BanRot.from_csv')
        self.from_csv_mock = self.patcher.start()
        self.ban_rot_mock = mock.MagicMock()
        self.from_csv_mock.return_value = self.ban_rot_mock
        import banrot
        banrot.banrot = self.ban_rot_mock
        self.banrot_mod = banrot
        self.environ = {}
        setup_testing_defaults(self.environ)
        self.start_response = mock.MagicMock()


    def tearDown(self):
        self.patcher.stop()


    def test_several_categories(self):
        self.environ['QUERY_STRING'] = 'category=cat1&category=cat2'
        self.ban_rot_mock.next_banner.return_value = core.BannerInfo('/1', 10, (1,3))
        result = self.banrot_mod.application(self.environ, self.start_response)
        self.start_response.assert_called_once_with('200 OK', [('Content-Type', 'text/html')])
        self.assertEqual(result, '<img alt="/1" src="/1" />')
        self.ban_rot_mock.next_banner.assert_called_once_with(['cat1', 'cat2'])


    def test_empty_categories(self):
        self.environ['QUERY_STRING'] = ''
        self.ban_rot_mock.next_banner.return_value = core.BannerInfo('/1', 10, (1,3))
        self.banrot_mod.application(self.environ, self.start_response)
        self.ban_rot_mock.next_banner.assert_called_once_with([])


    def test_one_category(self):
        self.environ['QUERY_STRING'] = 'category=cat1'
        self.ban_rot_mock.next_banner.return_value = core.BannerInfo('/1', 10, (1,3))
        self.banrot_mod.application(self.environ, self.start_response)
        self.ban_rot_mock.next_banner.assert_called_once_with(['cat1'])


if __name__ == '__main__':
    unittest.main()

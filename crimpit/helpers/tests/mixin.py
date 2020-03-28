import tempfile

from PIL import Image


class ViewTestMixin:
    def assert_resp_ok(self, resp):
        self.assertEqual(resp.status_code, 200)

    def assert_resp_created(self, resp):
        self.assertEqual(resp.status_code, 201)

    def login(self, user, password='pass'):
        value = self.client.login(username=user.username, password=password)
        self.assertTrue(value)

    @staticmethod
    def crete_image():
        tmp_file = tempfile.NamedTemporaryFile(suffix='.jpg')
        image = Image.new('RGB', (100, 100), )
        image.save(tmp_file.name, 'jpeg')
        return tmp_file

from django.test import TestCase, LiveServerTestCase
from selenium import webdriver
from selenium.webdriver.common.keys import Keys
from model_mommy import mommy
from models import Esc, EscImg
import os


class EscTest(TestCase):
    def test_esc_creation(self):
        """
        Tests basic esc creation
        """
        esc = mommy.make(Esc)
        self.assertTrue(isinstance(esc,Esc))
        self.assertEqual(esc.__unicode__(), esc.titulo)


    def test_esc_img_creation(self):
        """
        Tests basic esc img creation
        """
        esc_img = mommy.make(EscImg)
        self.assertTrue(isinstance(esc_img, EscImg))
        self.assertEqual(esc_img.__unicode__(), esc_img.esc.titulo)


    def test_esc_img_prepare(self):
        """
        Tests img preparation (copy)
        """
        esc_img = mommy.make(EscImg)
        alvo = esc_img.prepare()
        self.assertTrue(os.path.isfile(alvo))


    def test_esc_img_draw(self):
        """
        Tests img draw
        """
        esc_img = mommy.make(EscImg)
        alvo = esc_img.prepare()
        esc_img.draw(alvo)
        self.assertTrue(os.path.isfile(alvo))


    def test_esc_img_upload(self):
        """
        Tests img upload
        """
        esc_img = mommy.make(EscImg)
        alvo = esc_img.prepare()
        esc_img.draw(alvo)
        esc_img.upload(alvo)
        self.assertTrue('i.imgur.com' in esc_img.img_id)


    def test_esc_img_autonumber(self):
        """
        Tests auto numbering
        """
        esc = mommy.make(Esc)
        esc_img = EscImg(esc=esc)
        esc_img.autonumber()
        esc_img.save()
        self.assertTrue(esc_img.esc.titulo.startswith('NO.'))


    def test_imgur_key_missing(self):
        esc_img = mommy.make(EscImg)
        alvo = esc_img.prepare()
        esc_img.draw(alvo)
        os.environ['IMGUR_API'] = ''
        self.assertRaises(Exception, esc_img.upload, alvo)


class ViewsTest(LiveServerTestCase):
    fixtures = ['users.json']

    def setUp(self):
        self.browser = webdriver.Firefox()
        self.browser.implicitly_wait(3)


    def tearDown(self):
        self.browser.quit()


    def test_view_home(self):
        self.browser.get(self.live_server_url + '/')
        body = self.browser.find_element_by_tag_name('body')
        self.assertIn('Fazhe Escenario', body.text)


    def test_view_list(self):
        self.browser.get(self.live_server_url + '/list/')
        body = self.browser.find_element_by_tag_name('body')
        self.assertIn('FALTA!! OE PENALTI!!', body.text)
        self.browser.get(self.live_server_url + '/list/?page=20000')
        body = self.browser.find_element_by_tag_name('body')
        self.assertIn('FALTA!! OE PENALTI!!', body.text)


    def test_view_about(self):
        self.browser.get(self.live_server_url + '/sobre/')
        body = self.browser.find_element_by_tag_name('body')
        self.assertIn('SAC DO GOLERO', body.text)


    def test_view_restricted(self):
        self.browser.get(self.live_server_url + '/login/')
        body = self.browser.find_element_by_tag_name('body')
        self.assertIn('Username', body.text)
        username_field = self.browser.find_element_by_name('username')
        username_field.send_keys('teste')
        passwd_field = self.browser.find_element_by_name('password')
        passwd_field.send_keys('teste')
        passwd_field.send_keys(Keys.RETURN)
        self.browser.get(self.live_server_url + '/restricted/')
        body = self.browser.find_element_by_tag_name('body')
        self.assertIn('RESTRICTED', body.text)

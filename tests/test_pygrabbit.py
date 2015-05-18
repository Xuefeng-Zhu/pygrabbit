from requests.exceptions import MissingSchema
from pygrabbit import PyGrabbit
import pytest
import vcr


class TestPyGrabbitUrl:
    @vcr.use_cassette('fixtures/vcr_cassettes/pygrabbit.yaml', record_mode='new_episodes')
    def test_typeerror_on_blank_url(self):
        with pytest.raises(TypeError):
            g = PyGrabbit.url()

    @vcr.use_cassette('fixtures/vcr_cassettes/pygrabbit.yaml', record_mode='new_episodes')
    def test_missingschema_on_bad_url(self):
        with pytest.raises(MissingSchema):
            g = PyGrabbit.url('hello')

    @vcr.use_cassette('fixtures/vcr_cassettes/pygrabbit.yaml', record_mode='new_episodes')
    def test_good_url(self):
        g = PyGrabbit.url('http://www.google.com')
        assert g is not None

    @vcr.use_cassette('fixtures/vcr_cassettes/pygrabbit.yaml', record_mode='new_episodes')
    def test_is_not_none_on_404(self):
        g = PyGrabbit.url('http://www.thisurldoesnotexists.com')
        assert g.title is None
        assert g.description is None
        assert len(g.images) == 0


class TestPyGrabbitTitle:
    @vcr.use_cassette('fixtures/vcr_cassettes/pygrabbit.yaml', record_mode='new_episodes')
    def test_title_from_url(self):
        g = PyGrabbit.url('http://www.drudgereport.com')
        assert g.title.startswith('DRUDGE REPORT')

    @vcr.use_cassette('fixtures/vcr_cassettes/pygrabbit.yaml', record_mode='new_episodes')
    def test_title_from_og(self):
        g = PyGrabbit.url('http://ogp.me/')
        assert g.title == 'Open Graph protocol'

    @vcr.use_cassette('fixtures/vcr_cassettes/pygrabbit.yaml', record_mode='new_episodes')
    def test_title_twitter_card(self):
        g = PyGrabbit.url('https://dev.twitter.com/docs/cards/types/summary-card')
        assert g.title == 'Summary Card'


class TestPyGrabbitDescription:
    @vcr.use_cassette('fixtures/vcr_cassettes/pygrabbit.yaml', record_mode='new_episodes')
    def test_description_from_og(self):
        g = PyGrabbit.url('http://ogp.me/')
        assert g.description == "The Open Graph protocol enables any web page to become a rich object in a social graph."

    @vcr.use_cassette('fixtures/vcr_cassettes/pygrabbit.yaml', record_mode='new_episodes')
    def test_description_from_twitter_card(self):
        g = PyGrabbit.url("https://dev.twitter.com/docs/cards/types/summary-card")
        assert g.description == "The Summary Card can be used for many kinds of web content, from blog posts and news articles, to products and restaurants. It is designed to give the reader a preview of the content before clicking through to your website."

    @vcr.use_cassette('fixtures/vcr_cassettes/pygrabbit.yaml', record_mode='new_episodes')
    def test_description_from_meta(self):
        g = PyGrabbit.url("http://moz.com/learn/seo/meta-description")
        assert g.description == "Get SEO best practices for the meta description tag, including length and content."


class TestPyGrabbitImages:
    @vcr.use_cassette('fixtures/vcr_cassettes/pygrabbit.yaml', record_mode='new_episodes')
    def test_return_array(self):
        g = PyGrabbit.url("http://www.google.com")
        assert type(g.images) == list

    @vcr.use_cassette('fixtures/vcr_cassettes/pygrabbit.yaml', record_mode='new_episodes')
    def test_only_images_from_og(self):
        g = PyGrabbit.url("http://ogp.me/")
        assert g.images[0] == "http://ogp.me/logo.png"
        assert len(g.images) == 1

    @vcr.use_cassette('fixtures/vcr_cassettes/pygrabbit.yaml', record_mode='new_episodes')
    def test_return_images_from_twitter_card(self):
        g = PyGrabbit.url("https://dev.twitter.com/cards/types/summary-large-image")
        assert g.images[0] == "https://pbs.twimg.com/profile_images/2284174872/7df3h38zabcvjylnyfe3.png"
        assert len(g.images) == 1

    # NOTE: Amazon html is a bitch
    # @vcr.use_cassette('fixtures/vcr_cassettes/pygrabbit.yaml', record_mode='new_episodes')
    # def test_main_image_with_id_amazon(self):
    #     g = PyGrabbit.url("http://www.amazon.com/gp/product/0975277324")
    #     import ipdb;ipdb.set_trace()
    #     assert g.images[0] == "http://ecx.images-amazon.com/images/I/61dDQUfhuvL._SX300_.jpg"
    #     assert len(g.images) == 1

    @vcr.use_cassette('fixtures/vcr_cassettes/pygrabbit.yaml', record_mode='new_episodes')
    def test_return_images_from_global_img(self):
        g = PyGrabbit.url("http://elixir-lang.org/")
        assert g.images[0] == "http://elixir-lang.org/images/contents/home-code.png"
        assert len(g.images) == 1


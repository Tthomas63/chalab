from tests.tools import ChallengeTuple
from .. import selen


def test_is_setup(home):
    assert 'Welcome to' in home.hero.h1.text


def test_browse_around_shows_the_basics(home):
    # The home page show a welcome and some explanations
    assert 'Welcome to' in home.hero.h1.text
    assert len(home.hero.lead.text) > 10

    # I can click on the About page, It shows more information
    p = home.about()
    assert len(p.content.text) > 100

    # I can go back home with the logo in header
    p = p.click_logo()

    # I can open the registration
    p = p.signup()

    # It shows a registration form
    f = p.form

    assert f.has_fields(inputs=['username', 'email', 'password1', 'password2'])


def test_register_and_create_first_competition(wizard):
    # I'm on the wizard home page
    assert wizard.is_app('wizard')
    assert len(wizard.challenges) == 0

    # I can create a challenge
    p = wizard.create_challenge()
    assert p.is_('wizard', 'create-challenge')

    # I can fill the form
    # TODO(laurent): Upload organization image
    p.submit(ChallengeTuple(title='My first competition',
                            org_name='UmbrellaCorp',
                            description='Cure Zombiism'))

    assert p.is_('wizard', 'challenge')

    # I can go back home and find my competition
    p = p.go_home(selen.LIVE_SERVER_URL)

    assert len(p.challenges) == 1
    assert p.challenges[0].title == 'My first competition'

from app.common import status
from conftest import client, new_user
from app.models.battery import Battery
from app.models.user import User

def test_new_user():
    user = User('test@gmail.com', 'FlaskTest')
    assert user.email == 'test@gmail.com'
    assert user.password != 'FlaskTest'

def test_new_user_fixture(new_user):
    assert new_user.email == 'fixture@gmail.com'
    assert new_user.password != 'fixtureTest'

def test_setting_password(new_user):
    new_user.set_password('newpassword')

    assert new_user.password != 'newpassword'
    assert new_user.is_password_correct('newpassword')
    assert not new_user.is_password_correct('fixtureTest')

def test_new_battery():
    battery = Battery(1,1)
    assert battery.shelf_id == 1
    assert battery.container_id == 1


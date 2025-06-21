import pytest
from services import PersonController, API_URL, PersonControllerModel, User
from requests import Response, session


class TestPersonController:

    @classmethod
    @pytest.fixture(scope="class", autouse=True)
    def setup_class(cls):
        cls.user_api = PersonController(base_url=API_URL)

    # Нет токена!
    @pytest.fixture(scope="function", autouse=False)
    def create_and_delete_user(self) -> User:
        response_all_user = self.user_api.get_users()
        assert response_all_user.status_code == 200
        all_users = PersonControllerModel.model_validate(response_all_user.json()).root
        all_ids = {user.id for user in all_users if user.id is not None}
        new_user_data = {
            "id": max(all_ids, default=0) + 1,
            "firstName": "Roman",
            "secondName": "Bazhenov",
            "age": 22,
            "sex": "MALE",
            "money": 15000.
        }

        post_user = self.user_api.post_user(data=new_user_data)
        user_model = User(**post_user.json())
        assert post_user == 200

        return user_model

    @pytest.fixture(scope="class", autouse=False)
    def all_users(self):
        response = self.user_api.get_users()
        assert response.status_code == 200
        model = PersonControllerModel.model_validate(response.json()).root
        return model

    def test_get_users(self, all_users):
        assert isinstance(all_users, list)
        assert len(all_users) > 0

    #Нет токена!
    @pytest.mark.xfail
    def test_get_user_for_create(self, create_and_delete_user):
        response = self.user_api.get_user(user_id=create_and_delete_user.id)
        assert response.status_code == 200
        model = User(**response.json())
        assert model == create_and_delete_user

    def test_get_user(self, all_users):
        response = self.user_api.get_user(user_id=all_users[0].id)
        assert response.status_code == 200
        model = User(**response.json())
        assert model == all_users[0]






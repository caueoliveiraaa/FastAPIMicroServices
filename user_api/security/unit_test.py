from dataclasses import dataclass
from validations import Validations
from encryption import Encryption
import copy


@dataclass
class MockUser: 
    full_name: str
    cpf: str
    phone_number: str
    email: str


class TestValidations():
    def __init__(self):
        self.mock_user = MockUser(
            full_name="John Smith",
            cpf="123.456.789/00",
            phone_number="(12) 93456-7890",
            email="john@example.com"
        )
        self.validations = Validations()


    def test_validation_class(self) -> None:
        """
        Test all the validation methods
        """
        print('INFO - Initiating unit tests for user validations')
        assert self.validations.validate_name(
            self.mock_user.full_name) is True
        assert self.validations.validate_phone_number(
            self.mock_user.phone_number)
        assert self.validations.validate_user_cpf(
            self.mock_user.cpf) is True
        assert self.validations.validate_email(
            self.mock_user.email)  is True
        assert self.validations.validate_data(
            self.mock_user) is True
        print('INFO - Unit tests for user validations completed')


class TestEncryptions():
    def __init__(self):
        self.mock_user_john = MockUser(
            full_name="John Smith",
            cpf="123.456.789/00",
            phone_number="(12) 3456-7890",
            email="john@example.com"
        )
        self.mock_user_bryan = MockUser(
            full_name="Bryan Smith",
            cpf="987.654.321/00",
            phone_number="(12) 8888-7890",
            email="bryan@example.com"
        )
        self.mock_user_kobe = MockUser(
            full_name="Kobe Smith",
            cpf="222.654.321/00",
            phone_number="(12) 3333-7890",
            email="kobe@example.com"
        )
        self.users = [
            self.mock_user_john,
            self.mock_user_bryan,
            self.mock_user_kobe
        ]
        self.encryption = Encryption()


    def test_encryption_class(self):
        """
        Test all the encryption methods
        """
        print('INFO - Initiating unit tests for user encryption')
        copied_object = copy.copy(self.mock_user_john)
        encrypted_user = self.encryption.encrypt_user(copied_object)
        assert (self.mock_user_john.phone_number\
            != encrypted_user.phone_number) is True
        assert (self.mock_user_john.cpf\
            != encrypted_user.cpf) is True
        assert (self.mock_user_john.email\
            != encrypted_user.email) is True

        decrypted_user = self.encryption.decrypt_user(encrypted_user)
        assert (self.mock_user_john.phone_number\
            == decrypted_user.phone_number) is True
        assert (self.mock_user_john.cpf\
            == decrypted_user.cpf) is True
        assert (self.mock_user_john.email\
            == decrypted_user.email) is True

        copied_object_john = copy.copy(self.mock_user_john)
        copied_object_bryan = copy.copy(self.mock_user_bryan)
        copied_object_kobe = copy.copy(self.mock_user_kobe)
        encrypted_users = self.encryption.encrypt_all_users([
                copied_object_john,
                copied_object_bryan,
                copied_object_kobe
            ])
        
        for user, encrypted_user_temp in zip(self.users, encrypted_users):
            assert (user.phone_number !=\
                encrypted_user_temp.phone_number) is True
            assert (user.cpf != encrypted_user_temp.cpf) is True
            assert (user.email != encrypted_user_temp.email) is True

        decrypted_users = self.encryption.decrypt_all_users(encrypted_users)
        for user, decrypted_user in zip(self.users, decrypted_users):
            assert (user.full_name == decrypted_user.full_name)
            assert (user.phone_number == decrypted_user.phone_number)
            assert (user.cpf == decrypted_user.cpf)
            assert (user.email == decrypted_user.email)
        print('INFO - Unit tests for user encryption completed')


if __name__ == '__main__':
    unit_test_encryptions = TestValidations().test_validation_class()
    unit_test_validations = TestEncryptions().test_encryption_class()

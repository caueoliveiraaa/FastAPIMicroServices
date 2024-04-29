from typing import Any, List
import cryptocode
import os


class EncryptionDataError(Exception):
    pass


class DecryptionDataError(Exception):
    pass


class Encryption:
    
    def get_password(self) -> str:
        password = ''
        try:
            password = os.getenv('PASSWORD_ENCRYPTION')
        except:
            pass
        if not password:
            password = 'p@ssw0rd_f0r-t@sts'
        return password
    
    
    def encrypt_data(self, data_to_encrypt: Any) -> str:
        try:
            encrypted_data = cryptocode.encrypt(data_to_encrypt, self.get_password())
            return encrypted_data
        except Exception as error:
            raise EncryptionDataError(str(error))
    
    
    def decrypt_data(self, encrypted_data: Any) -> str:
        try:
            decrypted_data = cryptocode.decrypt(encrypted_data, self.get_password())
            return decrypted_data
        except Exception as error:
            raise DecryptionDataError(str(error))


    def encrypt_user(self, user: object) -> object:
        """ 
        :param user = UserDB class
        """
        user.cpf = self.encrypt_data(user.cpf)
        user.email = self.encrypt_data(user.email)
        user.phone_number = self.encrypt_data(user.phone_number)
        return user


    def decrypt_user(self, user: object) -> object:
        """ 
        :param user = UserDB class
        """
        user.cpf = self.decrypt_data(user.cpf)
        user.email = self.decrypt_data(user.email)
        user.phone_number = self.decrypt_data(user.phone_number)
        return user


    def user_cpf_or_email_exist(
        self,
        user_temp: object,
        all_users_decrypted: List
    ) -> bool:
        """ 
        :user_temp user = UserDB classs
        """
        for user_decrypted in all_users_decrypted:
            if user_decrypted.cpf == user_temp.cpf\
            or user_decrypted.email == user_temp.email:
                return True
        return False


    def encrypt_all_users(self, users_to_encrypt: List) -> List:
        for user in users_to_encrypt:
            user = self.encrypt_user(user)
        return users_to_encrypt


    def decrypt_all_users(self, users_to_decrypt: List) -> List:
        for user in users_to_decrypt:
            user = self.decrypt_user(user)
        return users_to_decrypt

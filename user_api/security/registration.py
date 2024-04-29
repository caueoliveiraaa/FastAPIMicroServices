from datetime import datetime
from fastapi import HTTPException


class RegistrationLogic:
    def __init__(self, Encryption, user, UserDb, database, log):
        """ 
        :param Encryption = Encryption class with encryption/decryption logic
        :param user = instance of UserDB class
        :param UserDb = UserDB class from database
        :param database = instance of LocalSession to handle databases
        :param log = instance of Logger
        """
        self.Encryption = Encryption
        self.user = user
        self.UserDb = UserDb
        self.database = database
        self.log = log
        self.all_users = self.database.query(self.UserDb).all()
    
    
    def check_if_cpf_and_email_exists(self) -> bool:
        try:
            all_users_decrypted = self.Encryption.decrypt_all_users(self.all_users)
            user_temp = self.user.copy()
            if not self.Encryption.user_cpf_or_email_exist(user_temp, all_users_decrypted):
                return True
            raise ValueError('CPF or e-mail already exist in the database')
        except ValueError as error:
            data_error = f'Error registering data: {error}'
            self.log.print_error(data_error)
            raise HTTPException(status_code=400, detail=data_error)
        except Exception as error:
            error_message = f'An unknown error ocurred: {error}'
            self.log.print_error(error_message)
            raise HTTPException(status_code=500, detail=error_message)
            
    
    def encrypt_and_register_user(self):
        try:
            all_users_decrypted = self.Encryption.encrypt_all_users(self.all_users)
            user_encrypted = self.Encryption.encrypt_user(self.user)
            if user_encrypted:
                new_user = self.UserDb(
                    full_name=user_encrypted.full_name,
                    cpf=user_encrypted.cpf,
                    email=user_encrypted.email,
                    phone_number=user_encrypted.phone_number,
                    created_at=datetime.now(),
                    updated_at=datetime.now()
                )
                self.database.add(new_user)
                self.database.commit()
                self.log.print_info('User registered successfully')
                return self.Encryption.decrypt_user(user_encrypted)
            raise ValueError('Error encrypting and creating new user')
        except ValueError as error:
            data_error = f'Error registering data: {error}'
            self.log.print_error(data_error)
            raise HTTPException(status_code=400, detail=data_error)
        except Exception as error:
            error_message = f'An unknown error ocurred: {error}'
            self.log.print_error(error_message)
            raise HTTPException(status_code=500, detail=error_message)

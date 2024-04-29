from typing import Union
import re


class Validations:
    
    def validate_data(self, user: object) -> Union[bool, Exception]:
        """ 
        :param user = UserDB class
        """
        try:
            return (
                self.validate_user_cpf(user.cpf)
                and self.validate_phone_number(user.phone_number)
                and self.validate_email(user.email)
                and self.validate_name(user.full_name)
            )
        except ValueError as error:
            raise ValueError(str(error))


    def validate_user_cpf(self, cpf: str) -> Union[bool, ValueError]:
        pattern = r'^\d{3}\.\d{3}\.\d{3}/\d{2}$'
        if not cpf or not isinstance(cpf, str)\
        or not bool(re.match(pattern, cpf)):
            raise ValueError(
                f'Invalid user CPF: {cpf} \
- try format: 111.111.111/11'
            )

        return True


    def validate_phone_number(self, phone_number: str)\
    -> Union[bool, ValueError]:
        pattern = r'^\(\d{2,3}\)\s*\d{4,5}-\d{4}$'
        if not phone_number or not isinstance(phone_number, str)\
        or not bool(re.match(pattern, phone_number)):
            raise ValueError(
                f'Invalid user phone number: {phone_number} \
- try format: (55) 9999-9999 or (55) 99999-9999'
            )

        return True


    def validate_email(self, email: str) -> Union[bool, ValueError]:
        pattern = r'^[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,}$'
        if not email or not isinstance(email, str)\
        or not bool(re.match(pattern, email)):
            raise ValueError(
                f'Invalid user e-mail: {email} \
- try format: example@example.com'
            )
        
        return True


    def validate_name(self, full_name: int) -> Union[bool, ValueError]:
        pattern = r'^[a-zA-Z]+(?:\s+[a-zA-Z]+)*$'
        if not full_name or not isinstance(full_name, str)\
        or not bool(re.match(pattern, full_name)):
            raise ValueError(
                f'Invalid user name: {full_name} \
- try format: john or John or John Smith'
            )

        return True

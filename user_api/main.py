from fastapi import FastAPI, HTTPException, Depends, Body
from security.registration import RegistrationLogic
from sqlalchemy.orm import sessionmaker, Session
from db.database import get_db_session, UserDb
from security.validations import Validations
from fastapi.responses import JSONResponse
from security.encryption import Encryption
from models.model import UserRequest
from sqlalchemy import create_engine
from datetime import datetime
from typing import List
import webbrowser
import requests
import logging
import uvicorn
import json
import os 


app = FastAPI(title='User API', description='API to manipulate users')
LocalSession = get_db_session(os.getenv('DB_URL'))


class Logger():
    def __init__(self):
        time = datetime.now().strftime('%d%m%Y__%H%M%S')
        file = f'.\\out\\app_{time}.log'
        info = logging.INFO
        format_log = '%(asctime)s - %(levelname)s - %(message)s'
        logging.basicConfig(filename=file, level=info, format=format_log)
        self.logger = logging.getLogger(__name__)
        self.logger.info("User API started successfully.")
        
    
    def print_info(self, message):
        self.logger.info(message)
        
        
    def print_error(self, message):
        self.logger.error(message)
        
        
    def print_warning(self, message):
        self.logger.warning(message)


def inject_database():
    database = LocalSession()
    try:
        yield database
    finally:
        database.close()


@app.get('/')
async def root(log: Logger = Depends()):
    """
    Status da API.
    """
    log.print_info('Endpoint root accessed successfully')
    return JSONResponse(
        content={'detail': 'User API has started successfully'},
        status_code=200
    )

    
@app.get('/api/users/all', response_model=List[UserRequest])
async def list_all_users(
    database: Session = Depends(inject_database),
    encryption: Encryption = Depends(),
    log: Logger = Depends()
):
    """
    Trazer todos os usuários do banco de dados.
    """
    log.print_info('Endpoint list_all_users accessed successfully')
    users = database.query(UserDb).all()
    if not users:
        message = 'No users found'
        log.print_error(message)
        raise HTTPException(status_code=404, detail=message)

    log.print_info('All users listed successfully')
    return encryption.decrypt_all_users(users)


@app.get('/api/users/{user_id}', response_model=UserRequest)
async def display_user(
    user_id: int,
    database: Session = Depends(inject_database),
    encryption: Encryption = Depends(),
    log: Logger = Depends()
):
    """
    Buscar usuário por ID específico.
    """
    try:
        log.print_info('Endpoint display_user accessed successfully')
        user = database.query(UserDb).filter(UserDb.id == user_id).first()
        if user is None:
            message = f'Invalid user ID {user_id}'
            log.print_error(message)
            raise HTTPException(status_code=404, detail=message)
            
        log.print_info('User retrived successfully')
        return encryption.decrypt_user(user)
    except Exception as error:
        error_message = f'An unknown error ocurred: {error}'
        log.print_error(error_message)
        raise HTTPException(status_code=500, detail=error_message)



@app.post('/api/users/register', response_model=UserRequest)
async def register_user(
    user: UserRequest = Body(...),
    database: Session = Depends(inject_database),
    validation: Validations = Depends(),
    encryption: Encryption = Depends(),
    log: Logger = Depends()
):
    """
    Registrar um usuário novo.
    """
    try:
        log.print_info('Endpoint register_user accessed successfully')
        validation.validate_data(user)
    except ValueError as error:
        data_error = f'Error validating data: {error}'
        log.print_error(data_error)
        raise HTTPException(status_code=400, detail=data_error)
    except Exception as error:
        error_message = f'An unknown error ocurred: {error}'
        log.print_error(error_message)
        raise HTTPException(status_code=500, detail=error_message)
    
    registration_logic = RegistrationLogic(
        encryption, user, UserDb, database, log
    )
    
    if registration_logic.check_if_cpf_and_email_exists():
        return registration_logic.encrypt_and_register_user()
         
    message = 'Error with encryption/decription and data registration'
    raise HTTPException(status_code=500, detail=message)


@app.delete('/api/users/delete/{user_id}')
async def delete_user(
    user_id: int,
    database: Session = Depends(inject_database),
    log: Logger = Depends()
):
    """
    Deletar usuário e seus respectivos pedidos na Order API.
    """
    log.print_info('Endpoint delete_user accessed successfully')
    user_to_delete = database.query(UserDb)\
        .filter(UserDb.id == user_id).first()

    if not user_to_delete:
        message = f'Invalid user ID {user_id}'
        log.print_error(message)
        raise HTTPException(status_code=404, detail=message)

    try:
        print(os.getenv('ORDERS_API') + str(user_id))
        response = requests.delete(os.getenv('ORDERS_API') + str(user_id))
        print(response.status_code)
        print('-------------------')
        json_data = response.json()
        database.delete(user_to_delete)
        database.commit()
        log.print_info('User deleted successfully')
        if response.status_code == 200:
            log.print_info("User's orders deleted successfully")
            message = 'User and its orders deleted successfully'
            return JSONResponse(content={'detail': message}, status_code=200)
        elif response.status_code == 404:
            message = 'User deleted but no orders were found'
            return JSONResponse(content={'detail': message}, status_code=200)
        raise HTTPException(
            status_code=500,
            detail='Error sending request to order API'
        )
    except Exception as e:
        log.print_error(str(e))
        message = f'Error trying to delete user: {str(e)}'
        return JSONResponse(content={'detail': message}, status_code=500) 


@app.put('/api/users/update/{user_id}', response_model=UserRequest)
async def update_user(
    user_id: int,
    user: UserRequest = Body(...),
    database: Session = Depends(inject_database),
    validation: Validations = Depends(),
    encryption: Encryption = Depends(),
    log: Logger = Depends()
):
    """
    Atualizar dados de usuário existente.
    """
    log.print_info('Endpoint update_user accessed successfully')
    existing_user = database.query(UserDb)\
        .filter(UserDb.id == user_id).first()

    if not existing_user:
        message = f'Invalid user ID {user_id}'
        log.print_error(message)
        raise HTTPException(status_code=404, detail=message)

    try:
        validation.validate_data(user)
    except ValueError as error:
        message = f'Error validating data: {error}'
        log.print_error(message)
        raise HTTPException(status_code=400, detail=message)
    except Exception as error:
        message = f'An unknown error ocurred: {error}'
        log.print_error(message)
        raise HTTPException(status_code=500, detail=message)

    user = encryption.encrypt_user(user)
    existing_user.full_name = user.full_name
    existing_user.cpf = user.cpf
    existing_user.email = user.email
    existing_user.phone_number = user.phone_number
    existing_user.updated_at = datetime.now()
    database.commit()
    log.print_info('User updated successfully')
    return encryption.decrypt_user(existing_user)


if __name__ == '__main__':
    uvicorn.run(app, host='0.0.0.0', port=8000)

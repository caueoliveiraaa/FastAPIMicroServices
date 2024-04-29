from db.database import get_db_session, OrderDb
from fastapi import FastAPI, HTTPException, Depends, Body
from sqlalchemy.orm import sessionmaker, Session
from fastapi.responses import JSONResponse
from security.validations import Validations
from models.model import OrderRequest
from sqlalchemy import create_engine
from datetime import datetime
from typing import List
import webbrowser
import logging
import requests
import uvicorn
import os


app = FastAPI(title="Order API", description="API to manipulate orders")
LocalSession = get_db_session(os.getenv('DB_URL'))


class Logger():
    def __init__(self) -> None:
        time = datetime.now().strftime('%d%m%Y__%H%M%S')
        file = f'.\\out\\app_{time}.log'
        info = logging.INFO
        format_log = '%(asctime)s - %(levelname)s - %(message)s'    
        logging.basicConfig(filename=file, level=info, format=format_log)
        self.logger = logging.getLogger(__name__)
        self.logger.info("User API started successfully.")
        
    
    def print_info(self, message) -> None:
        self.logger.info(message)
        
        
    def print_error(self, message) -> None:
        self.logger.error(message)
        
        
    def print_warning(self, message) -> None:
        self.logger.warning(message)


async def inject_database() -> LocalSession:
    database = LocalSession()
    try:
        yield database
    finally:
        database.close()


@app.get("/")
async def root(log: Logger = Depends()):
    """
    Status da API.
    """
    log.print_info('Endpoint root accessed successfully')
    return JSONResponse(
        content={"detail": 'Order API has started successfully'},
        status_code=200
    )


@app.get("/api/orders/all", response_model=List[OrderRequest])
async def list_all_orders(
    database: Session = Depends(inject_database),
    log: Logger = Depends()
):
    """
    Trazer todos os pedidos do banco de dados.
    """
    log.print_info('Endpoint list_all_orders accessed successfully')
    orders = database.query(OrderDb).all()
    if not orders:
        message = 'No orders found'
        log.print_error(message)
        raise HTTPException(status_code=404, detail=message)

    log.print_info('All orders listed successfully')
    return orders


@app.get('/api/orders/by_user/{user_id}', response_model=List[OrderRequest])
async def list_orders_by_user(
    user_id: int,
    database: Session = Depends(inject_database),
    log: Logger = Depends()
):
    """
    Trazer todos os pedidos do banco de dados por usuário.
    """
    log.print_info('Endpoint list_orders_by_user accessed successfully')
    orders = database.query(OrderDb)\
        .filter(OrderDb.user_id == user_id)\
        .all()

    if not orders:
        message = f'No orders for user ID {order_id}'
        log.print_error(message)
        raise HTTPException(status_code=404, detail=message)
    
    log.print_info('Orders from user ID {user_id} listed successfully')
    return orders
    

@app.get('/api/orders/{order_id}', response_model=OrderRequest)
async def display_order(
    order_id: int,
    database: Session = Depends(inject_database),
    log: Logger = Depends()
):
    """
    Buscar pedido por ID específico.
    """
    log.print_info('Endpoint display_order accessed successfully')
    order = database.query(OrderDb).filter(OrderDb.id == order_id).first()
    if not order:
        invalid_message = f'Invalid order ID {order_id}'
        log.print_error(invalid_message)
        raise HTTPException(status_code=404, detail=invalid_message)

    log.print_info('Order retrived successfully')
    return order


@app.post('/api/orders/register', response_model=OrderRequest)
async def register_order(
    order: OrderRequest = Body(...),
    database: Session = Depends(inject_database),
    validation: Validations = Depends(),
    log: Logger = Depends()
):
    """
    Registrar um pedido novo.
    """
    try:
        log.print_info('Endpoint register_order accessed successfully')
        validation.validate_data(order)
    except ValueError as error:
        data_error = f'Error validating data: {error}'
        log.print_error(data_error)
        raise HTTPException(status_code=400, detail=data_error)
    except Exception as error:
        error_message = f'An unknown error ocurred: {error}'
        log.print_error(error_message)
        raise HTTPException(status_code=500, detail=error_message)

    response = requests.get(os.getenv('USERS_API') + str(order.user_id))
    if response.status_code == 404 or response.status_code == 422:
        message = f'Invalid user ID {order.user_id}'
        log.print_error(message)
        raise HTTPException(status_code=response.status_code, detail=message)
    elif response.status_code != 200:
        message = f'An error occured with user ID {order.user_id}'
        log.print_error(message)
        raise HTTPException(status_code=response.status_code, detail=message)
        
    new_order = OrderDb(
        user_id=order.user_id,
        item_description=order.item_description,
        item_quantity=order.item_quantity,
        item_price=order.item_price,
        total_value=order.item_quantity * order.item_price,
        created_at=datetime.now(),
        updated_at=datetime.now()
    )

    database.add(new_order)
    database.commit()
    log.print_info('Order registered successfully')
    return new_order


@app.put('/api/orders/update/{order_id}', response_model=OrderRequest)
async def update_order(
    order_id: int,
    order: OrderRequest = Body(...),
    database: Session = Depends(inject_database),
    validation: Validations = Depends(),
    log: Logger = Depends()
):
    """
    Atualizar dados de pedido existente.
    """
    log.print_info('Endpoint update_order accessed successfully')
    existing_order = database.query(OrderDb)\
        .filter(OrderDb.id == order_id).first()

    if not existing_order:
        log.print_error(f'Invalid order ID: {order_id}')
        raise HTTPException(
            status_code=404,
            detail=f'Invalid order ID: {order_id}'
        )
        
    response = requests.get(os.getenv('USERS_API') + str(order.user_id))
    if response.status_code == 404 or response.status_code == 422:
        message = f'Invalid user ID: {order.user_id}'
        log.print_error(message)
        raise HTTPException(status_code=response.status_code, detail=message)
    elif response.status_code != 200:
        message = f'An error occured with user ID: {order.user_id}'
        log.print_error(message)
        raise HTTPException(status_code=response.status_code, detail=message)

    try:
        validation.validate_data(order)
    except ValueError as error:
        data_error = f'Error validating data: {error}'
        log.print_error(data_error)
        raise HTTPException(status_code=400, detail=data_error)
    except Exception as error:
        message = f'An unknown error ocurred: {error}'
        log.print_error(message)
        raise HTTPException(status_code=500, detail=message)

    existing_order.user_id = order.user_id
    existing_order.item_description = order.item_description
    existing_order.item_quantity = order.item_quantity
    existing_order.item_price = order.item_price
    existing_order.total_value = order.item_quantity * order.item_price
    database.commit()
    log.print_info('Order updated successfully')

    return existing_order


@app.delete('/api/orders/delete/{order_id}')
async def delete_order(
    order_id: int,
    database: Session = Depends(inject_database),
    log: Logger = Depends()
):
    """
    Deletar um pedido específico.
    """
    log.print_info('Endpoint delete_order accessed successfully')
    order_to_delete = database.query(OrderDb)\
        .filter(OrderDb.id == order_id).first()

    if not order_to_delete:
        no_orders_message = f'No orders found with ID {order_id}'
        log.print_error(no_orders_message)
        raise HTTPException(status_code=404, detail=no_orders_message)

    database.delete(order_to_delete)
    database.commit()
    success_message = 'Order deleted successfully'
    log.print_info(success_message)
    return JSONResponse(content={'detail': success_message}, status_code=200)


@app.delete('/api/orders/delete/by_user/{user_id}')
async def delete_orders_by_user(
    user_id: int,
    database: Session = Depends(inject_database),
    log: Logger = Depends()
):
    """
    Deletar todos os pedidos que pertencem à um usuário específico.
    """
    log.print_info('Endpoint delete_orders_by_user accessed successfully')
    orders_to_delete = database.query(OrderDb)\
        .filter(OrderDb.user_id == user_id).all()

    if not orders_to_delete:
        message = f'No orders found with user ID {user_id}'
        log.print_error(message)
        return JSONResponse(content={'detail': message}, status_code=404)
    
    for order in orders_to_delete:
        database.delete(order)
        
    database.commit()
    success_message = 'Orders listed by user successfully'
    log.print_info(success_message)
    return JSONResponse(content={'detail': success_message}, status_code=200)


if __name__ == "__main__":
    uvicorn.run(app, host="0.0.0.0", port=8000)

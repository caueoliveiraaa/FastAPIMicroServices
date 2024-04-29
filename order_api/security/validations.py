from typing import Union


class Validations:

    def validate_data(self, order: object) -> Union[bool, Exception]:
        """ 
        :param user = UserDB class
        """
        try:
            return (
                self.validate_user_id(order.user_id)
                and self.validate_item_description(order.item_description)
                and self.validate_item_quantity(order.item_quantity)
                and self.validate_item_price(order.item_price)
            )
        except Exception as error:
            raise ValueError(str(error))


    def validate_user_id(self, user_id: int) -> Union[bool, ValueError]:
        if not user_id or not isinstance(user_id, int)\
        or not user_id > 0:
            raise ValueError(
                f'Invalid user ID: {user_id} \
try an integer number higher than zero'
)

        return True


    def validate_item_description(self, item_description: str)\
    -> Union[bool, ValueError]:
        if not item_description or not isinstance(item_description, str)\
        or not len(item_description) >= 1:
            raise ValueError(
                f'Invalid item description: {item_description} \
try a description with more than one char, example: Car'
            )

        return True


    def validate_item_quantity(self, item_quantity: int)\
    -> Union[bool, ValueError]:
        print(item_quantity >= 0)
        print(isinstance(item_quantity, int))
        if not isinstance(item_quantity, int) or not item_quantity >= 0:
            raise ValueError(
                f'Invalid item quantity: {item_quantity} \
try an integer number higher than zero'
            )

        return True


    def validate_item_price(self, item_price: float)\
    -> Union[bool, ValueError]:
        print(item_price >= 0)
        print(isinstance(item_price, float))
        if not isinstance(item_price, float) or not item_price >= 0:
            raise ValueError(
                f'Invalid item price: {item_price} \
try a float number higher than zero'
            )

        return True

from validations import Validations
from dataclasses import dataclass


@dataclass
class MockOrder:
    item_quantity: int
    item_description: str
    user_id: int
    item_price: float


class TestValidations:
    def __init__(self):
        self.mock_data = MockOrder(
            item_quantity=5,
            item_description="Test item",
            user_id=1234,
            item_price=10.99
        )
        self.validation = Validations()


    def test_all_validations(self) -> None:
        """
        Test all the validation methods
        """
        print('Initiating unit tests for order validations')
        assert self.validation.validate_item_quantity(
            self.mock_data.item_quantity) == True
        assert self.validation.validate_item_description(
            self.mock_data.item_description) == True
        assert self.validation.validate_user_id(
            self.mock_data.user_id) == True
        assert self.validation.validate_item_price(
            self.mock_data.item_price) == True
        assert self.validation.validate_data(
            self.mock_data) == True
        print('Unit tests for order validations completed')


if __name__ == "__main__":
    test = TestValidations().test_all_validations()

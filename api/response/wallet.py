from api.response.base import BaseModel
from db.models.operations import DBOperation


class WalletOperation(BaseModel):
    logo: str
    amount: int
    name: str


class WalletResponse(BaseModel):
    balance: int
    operations: list[WalletOperation]


class WalletOperationFactory:
    @staticmethod
    def get_from_model(model: DBOperation) -> WalletOperation:
        return WalletOperation(
            logo=model.company.logo,
            amount=model.amount,
            name=model.company.name
        )

    @classmethod
    def get_from_models(cls, models: list[DBOperation]) -> list[WalletOperation]:
        return [cls.get_from_model(model) for model in models]


class WalletResponseFactory:

    @staticmethod
    def get_from_models(balance: int, operations: list[DBOperation]) -> WalletResponse:
        return WalletResponse(balance=balance, operations=WalletOperationFactory.get_from_models(operations))

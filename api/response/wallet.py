from api.response.base import BaseModel
from db.models.operations import DBOperation

colors = [
    "#0075FF",
    "#FFA800",
    "#ABDCCB",
    "#FF7970",
    "#D9D9D9"
]


class WalletOperation(BaseModel):
    logo: str
    amount: int
    name: str


class Categories(BaseModel):
    name: str
    total: int


class CategoriesColors(BaseModel):
    color: str
    amount: int
    name: str


class CategoryOperations(BaseModel):
    total_earn: int
    categories: list[CategoriesColors]


class WalletResponse(BaseModel):
    balance: int
    categories: CategoryOperations
    operations: list[WalletOperation]


class CategoriesFactory:

    @classmethod
    def get_from_models(cls, models: list[DBOperation]) -> CategoryOperations:
        local_colors = colors.copy()
        total_earn = 0
        categories = dict()
        for model in models:
            if model.amount > 0:
                total_earn += model.amount
                if model.company.category not in categories:
                    amount = 0
                    color = local_colors.pop()
                    name = model.company.category
                    categories[model.company.category] = CategoriesColors(amount=amount, color=color, name=name)
                categories[model.company.category].amount += model.amount
        return CategoryOperations(
            total_earn=total_earn,
            categories=list(categories.values())
        )


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
        return WalletResponse(balance=balance, operations=WalletOperationFactory.get_from_models(operations),
                              categories=CategoriesFactory.get_from_models(operations))

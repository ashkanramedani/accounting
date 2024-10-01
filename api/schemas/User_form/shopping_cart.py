from schemas.Base import *


class shopping_card_Item(BaseModel):
    item_pk_id: UUID
    price: float
    quantity: float


class shopping_card(BaseModel):
    discount_code: str | None = None
    shopping_card_fk_id: UUID

    bucket: List[shopping_card_Item]


class post_shopping_card_schema(shopping_card):
    user_fk_id: UUID

    class Config:
        extra = 'ignore'


class update_shopping_card_schema(shopping_card):
    shopping_card_pk_id: UUID

    class Config:
        extra = 'ignore'


class shopping_card_response(BaseModel):
    shopping_card_pk_id: UUID

    total: float
    total_discounted: float

    transaction_fk_id: Optional[UUID] = None

    class Config:
        orm_mode = True
        extra = 'ignore'

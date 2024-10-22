from schemas.Base import *


class shopping_card_Item(BaseModel):
    price: float = 0
    quantity: int = 0
    total_price: float = 0
    discounted_price: float = 0

    class Config:
        extra = 'ignore'

class add_to_card(BaseModel):
    item_id: UUID
    quantity: int


class shopping_card(BaseModel):
    pass


# shopping_card_pk_id: UUID
# discount_code: str | None = None


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

    user: export_employee
    transaction_fk_id: Optional[UUID] = None

    class Config:
        orm_mode = True
        extra = 'ignore'


# new Schema

class item(BaseModel):
    item_id: UUID
    quantity: int


class add_item(Base_form):
    shopping_card_fk_id: UUID
    items: List[item]

class update_item(Base_form):
    shopping_card_fk_id: UUID
    items: List[item]

class delete_item(Base_form):
    shopping_card_fk_id: UUID
    items: List[UUID]

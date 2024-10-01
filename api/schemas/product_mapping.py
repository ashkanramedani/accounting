from schemas.Base import *


class product_mapping(Base_form):
    target_product_fk_id: UUID
    target_product_table: str
    product_name: str
    product_quantity: int
    product_price: float


class post_product_mapping_schema(product_mapping):
    pass

    class Config:
        extra = 'ignore'


class update_product_mapping_schema(product_mapping):
    product_mapping_pk_id: UUID

    class Config:
        extra = 'ignore'


class product_mapping_response(product_mapping):
    pass

    class Config:
        orm_mode = True
        extra = 'ignore'

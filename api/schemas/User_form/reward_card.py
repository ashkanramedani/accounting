from ..Base import *


class Reward_Type(str, Enum):
    percentage = 'percentage'
    fix = 'fix'


class reward_card(Base_form):
    reward_amount: float
    reward_type: Reward_Type
    start_date: date
    end_date: date

    class Config:
        extra = 'ignore'


class post_reward_card_schema(reward_card):
    user_fk_id: UUID

    class Config:
        extra = 'ignore'


class update_reward_card_schema(reward_card):
    reward_card_pk_id: UUID

    class Config:
        extra = 'ignore'


class reward_card_response(Base_response, update_reward_card_schema):
    employee: export_employee

    class Config:
        extra = 'ignore'
        orm_mode = True

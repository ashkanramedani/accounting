from dataclasses import dataclass

from .Base import *


class PaymentRequest(BaseModel):
    amount: int = 10000
    # currency: Literal["IRR", "IRT"] = "IRR"
    # description: str = ''
    email: str
    mobile: str
    # order_id: UUID
    shopping_card_id: UUID

    class Config:
        extra = 'ignore'


@dataclass
class Zarinpal:
    request: str = "https://api.zarinpal.com/pg/v4/payment/request.json"
    callback: str = "https://sand.admin.api.ieltsdaily.ir/Zarinpal/callback"
    StartPay: str = "https://www.zarinpal.com/pg/StartPay/"
    verify: str = "https://payment.zarinpal.com/pg/v4/payment/verify.json"
    merchant_id: str = "74ca3eb9-387f-4b78-b233-90ade2bd395b"




@dataclass
class Parsian:
    request: str = "https://pec.shaparak.ir/NewIPGServices/Sale/SaleService.asmx"
    callback: str = "https://ieltsdaily.ir/parsiyan/callback"
    StartPay: str = "https://pec.shaparak.ir/NewIPG/?Token="
    confirm: str = ""
    LoginAcc: str = "PRIsFvMN61D3T3jB3hrb"

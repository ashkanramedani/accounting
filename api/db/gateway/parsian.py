import json
from random import randint

from sqlalchemy.orm import Session
from zeep.proxy import ServiceProxy

from db import Set_Status
from lib import JSONEncoder
from fastapi import HTTPException
from zeep import Client

import models as dbm
import schemas as sch
from .StatusCodes import Parsian_Status

def genCardID(db: Session) -> str:
    card_ids = [record[0] for record in db.query(dbm.Shopping_card_form.card_id).all()]
    rnd = ''.join(str(randint(0, 9)) for _ in range(17))
    while rnd in card_ids:
        rnd = ''.join(str(randint(0, 9)) for _ in range(17))
    return rnd


def parsian_create_gateway(db: Session, Form: sch.PaymentRequest):
    try:
        data = Form.__dict__

        db.query()
        shopping_card: dbm.Shopping_card_form = db.query(dbm.Shopping_card_form).filter_by(shopping_card_pk_id=data.pop("shopping_card_id")).first()
        if not shopping_card:
            return 400, "Shopping card not found"

        order_id = genCardID(db)
        with Client('https://pec.shaparak.ir/NewIPGServices/Sale/SaleService.asmx?wsdl') as client:
            request_data = {
                'LoginAccount': sch.Parsian.LoginAcc,
                'Amount': Form.amount,
                'OrderId': order_id,
                'CallBackUrl': sch.Parsian.callback,
                'AdditionalData': 'Test'}

            response: ServiceProxy = client.service.SalePaymentRequest(requestData=request_data)
            Status = response["Status"]
            if Status == 0:
                Token = response["Token"]
                shopping_card.card_id = order_id
                transaction = dbm.Transaction_form(**data, Token=Token)  # type: ignore[call_args]
                transaction.status = Set_Status(db, "payment", "Ready")
                db.add(transaction)
                db.commit()
                return 200, sch.Parsian.StartPay + str(Token)

            _data = {"Status": Status, "Message": Parsian_Status.get(str(Status), f"UNKNOWN_COD")}
            # _data = json.dumps(response, cls=JSONEncoder)
            transaction = dbm.Transaction_form(**data, data=json.dumps(_data, ensure_ascii=False))  # type: ignore[call_args]
            transaction.status = Set_Status(db, "payment", "failed")
            db.add(transaction)
            db.commit()
            db.flush()
            return 400, f"unknown error occurred. contact administrator Token: {transaction.transaction_pk_id}"

    except Exception as e:
        raise HTTPException(status_code=500, detail=e.__repr__())


def parsian_callback(db, Status, Authority):
    pass


"""
{
  "data": [],
  "errors": {
    "code": -9,
    "message": "The input params invalid, validation error.",
    "validations": [
      {
        "description": "The description field is required."
      }
    ]
  }
}
"""

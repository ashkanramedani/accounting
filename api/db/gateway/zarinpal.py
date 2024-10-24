import json
from typing import Dict

import requests

import models as dbm
import schemas as sch
from db.Extra import *
from lib import JSONEncoder

headers: Dict = {'accept': 'application/json', 'content-type': 'application/json'}


def zarinpal_create_gateway(db, Form: sch.PaymentRequest):
    try:
        data = Form.__dict__
        shopping_card: dbm.Shopping_card_form = db.query(dbm.Shopping_card_form).filter_by(shopping_card_pk_id=Form.shopping_card_id).first()
        if not shopping_card:
            return 400, "Shopping card not found"

        metadata = {field: str(data.get(field)) for field in ["email", "mobile"]}
        metadata["order_id"] = data.pop("shopping_card_id")
        data_to_send = {"merchant_id": sch.Zarinpal.merchant_id, "callback_url": sch.Zarinpal.callback, "metadata": metadata, "description": "Test", **data}

        res = requests.post(url=sch.Zarinpal.request, headers=headers, data=json.dumps(data_to_send, cls=JSONEncoder))
        res_json = res.json()

        if "data" in res_json:  # and "authority" in res_json["data"]["authority"]:
            Token = res_json["data"].get("authority", None)
            transaction = dbm.Transaction_form(Token=Token, **data)  # type: ignore[call_args]
            db.add(transaction)

            db.flush()
            shopping_card.transaction_fk_id = transaction.transaction_pk_id
            db.commit()

            if Token:
                return 200, sch.Zarinpal.StartPay + Token
            else:
                return 400, f"unknown error occurred. contact administrator Token: {transaction.transaction_pk_id}"
        else:
            transaction = dbm.Transaction_form(**data, data=res_json)  # type: ignore[call_args]
            db.add(transaction)
            db.flush()
            shopping_card.transaction_fk_id = transaction.transaction_pk_id
            db.commit()
            return res.status_code, res_json["errors"]["message"]
    except Exception as e:
        return Return_Exception(db, e)


def zarinpal_callback(db, Status, Authority):
    transaction: dbm.Transaction_form = db.query(dbm.Transaction_form).filter_by(Token=Authority).first()
    if Status == "OK":
        amount = transaction.amount
        data = {"merchant_id": sch.Zarinpal.merchant_id, "amount": amount, "authority": Authority}
        response = requests.post(sch.Zarinpal.verify, data=json.dumps(data), headers=headers)
        metadata: Dict = response.json()
        transaction.metadata = metadata

        if metadata["data"]:
            transaction.status = Set_Status(db=db, status=metadata["data"].get("message"), cluster="payment")
        elif metadata["errors"]:
            transaction.status = Set_Status(db=db, status=metadata["errors"].get("message"), cluster="payment")
        else:
            transaction.status = Set_Status(db=db, status="Failed", cluster="payment")
            return 400, f"unknown error occurred. contact administrator Token: {transaction.transaction_pk_id}"
        db.commit()
        return 200, response.json()
    else:
        transaction.status = Set_Status(db=db, status="Failed", cluster="payment")
        db.commit()
        return 400, f"Transaction Failed. contact administrator Token: {transaction.transaction_pk_id}"


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

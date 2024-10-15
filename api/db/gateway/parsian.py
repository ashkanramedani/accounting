import json
import time
from random import getrandbits

from fastapi import HTTPException
from sqlalchemy.orm import Session
from zeep import Client
from zeep.proxy import ServiceProxy

import models as dbm
import schemas as sch
from db import Set_Status
from .StatusCodes import Parsian_Status


def parsian_create_gateway(db: Session, Form: sch.PaymentRequest):
    try:
        data = Form.__dict__

        db.query()
        shopping_card: dbm.Shopping_card_form = db.query(dbm.Shopping_card_form).filter_by(shopping_card_pk_id=data.pop("shopping_card_id")).first()
        if not shopping_card:
            return 400, "Shopping card not found"

        order_id: int = (int(time.time() * 1000) << 16) | getrandbits(32)
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


def parsian_callback(db, Form: sch.parsian_callBack):
    shopping_card, transaction = db \
        .query(
            dbm.Shopping_card_form, dbm.Transaction_form) \
        .join(
            dbm.Transaction_form,
            dbm.Transaction_form.transaction_pk_id == dbm.Shopping_card_form.shopping_card_pk_id) \
        .filter(
            dbm.Shopping_card_form.card_id == Form.OrderId) \
        .first()

    transaction.data = Form.dict()
    if Form.status == 0 and Form.Token > 0:  # Successful transaction
        with Client("https://pec.shaparak.ir/NewIPGServices/Confirm/ConfirmService.asmx?wsdl") as client:
            request_data = {'LoginAccount': sch.Parsian.LoginAcc, 'Token': Form.Token}
            response: ServiceProxy = client.service.ConfirmPayment(requestData=request_data)
            if response["Status"] == 0 and response["RRN"] > 0:  # Confirmed
                transaction.status = Set_Status(db, "payment", "Paid - Confirmed")
                db.commit()
                return 200, "Paid - Confirmed"
            else:  # Confirmed Failed
                transaction.status = Set_Status(db, "payment", "conform Failed")
                db.commit()
                return 400, f"conform Failed. contact administrator Token: {transaction.transaction_pk_id}"
    else:  # Failed transaction
        return 400, f"transaction Failed. contact administrator Token: {transaction.transaction_pk_id}"

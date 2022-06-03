from pydantic import BaseModel

class TransactionRefundInfo(BaseModel):
    refund_method: str | None
    refund_amount: str | None

class Transaction(BaseModel):
    user_id: str|None
    refund_info: TransactionRefundInfo | None


trx = Transaction(user_id=33,refund_info={})

print(trx)


from enum import Enum
class SkuStatus(str, Enum):
    PAYMENT_REQUIRED = "payment_required"  # 결제대기
    PAYMENT_FAIL_TIME_OUT = "payment_fail_time_out"  # 결제실패 (입금안함)
    PAYMENT_FAIL_ERROR = "payment_fail_error"  # 결제실패 (PG실패)
    CHECK_REQUIRED = "check_required"  # 접수요망


dic = {SkuStatus.PAYMENT_REQUIRED:True,
       SkuStatus.PAYMENT_FAIL_TIME_OUT:True,
       SkuStatus.PAYMENT_FAIL_ERROR:True,
       SkuStatus.CHECK_REQUIRED:True}

lst = [SkuStatus.PAYMENT_REQUIRED,
       SkuStatus.PAYMENT_FAIL_TIME_OUT,
       SkuStatus.PAYMENT_FAIL_ERROR,
       SkuStatus.CHECK_REQUIRED]

if dic.get("payment_required"):
    print(55)

if "check_required" in lst:
    print(33)

class InicisPossiblePaymentMethod(str,Enum):
    CARD = "Card", 
    ACCT = "Acct" #(실시간 계좌이체) 
    VACCT = "Vacct" #(가상계좌) 
    GVACCT = "GVacct" #(입금전, 채번 취소시) 
    HPP = "HPP" #(핸드폰)  
    RECEIPT = "Receipt" #(영수증)  
    VOUCHER = "Voucher" #(상품권)  
    PAYPAL = "Paypal" #(페이팔)  
    APAY = "Apay" #(알리페이)  
    TPAY = "TPAY" #(위챗페이) 

inicis_payment_method = {
    k:True for k in InicisPossiblePaymentMethod
}

if inicis_payment_method.get("Card"):
    print("Exist!")
    
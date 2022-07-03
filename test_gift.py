
import httpx
from pydantic import BaseModel
from fastapi import FastAPI,Body



app = FastAPI()

class GiftingRequestParameter(BaseModel):
    mdcode : str #매체코드
    goods_id: str | None # 상품아이디(미 입력시 전체 상품 목록 조회)
    response_type : str = "JSON" #응답 값 타입 -JSON or XML(default)
    token : str # 인증서버로 받는 토큰

class GiftingGoods(BaseModel):
    goods_id: str | None # 상품아이디
    category1:str | None # 상품구분
    category2:str | None # 상품분류
    affiliate:str | None # 교환처
    affiliate_category:str | None #교환처분류
    head_swap_cd:str | None # 대표 교환처코드
    swap_cd: str | None # 교환처코드
    desc:str | None # 상품설명
    goods_nm:str | None # 상품명
    goods_img:str | None # 이미지 경로
    normal_sale_price: str | None #	소비자 가격
    normal_sale_vat: str | None # 소비자 가격 부가세
    sale_price: str | None # 윈큐브 판매가격
    sale_vat: str | None #윈큐브 판매가격 부가세
    total_price: str| None  #윈큐브 판매가격+부가세
    period_end: str | None #상품판매종료일
    limit_date: str	| None #유효기간
    end_date: str | None #유효기간종료일

class GiftingResponse(BaseModel):
    result_code : str #성공이면 0 그 외 실패
    goodsnum : int #상품개수
    goods_list : list[GiftingGoods]



dev_url = "http://dev.giftting.co.kr:8084/media/"
prod_url = "https://gw.giftting.co.kr:4431/media/"

content = httpx.get(dev_url)

def query_sellable_gift(goods_id=None,requested_size=0) -> bool:
    try:
        res = httpx.post(url=dev_url,json=GiftingRequestParameter(mdcode="",goods_id=goods_id,token="").dict())
    except httpx.HTTPError:
        pass
    result = res.json()
    for goods in result.get("goods_list"):
        if goods.get("goodsnum") < requested_size:
            return False 
            #특정 굿즈가 얼마나 있는지 알 수 없다.? 

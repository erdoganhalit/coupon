from pydantic import BaseModel
from typing import Dict, List, Union, Optional, Literal, TypedDict

class CouponCrawlerResults(BaseModel):
    url: str
    coupon_provider: str
    codes: List[str]
    retailer: str
    product: Union[str, None]

class CouponCrawlerArgs(BaseModel):
    retailer: str
    product_name: Union[str, None]

class CouponEvaluatorArgs(BaseModel):
    codes: List[str]
    
class CouponEvaluatorResults(BaseModel):
    code: str
    result: bool


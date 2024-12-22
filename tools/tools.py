from pydantic import BaseModel
from typing import Dict, Literal, List, Optional
from langchain.tools import StructuredTool
from tools.classes import CouponCrawlerArgs, CouponEvaluatorArgs
from tools.functions import get_coupons, try_coupons

COUPON_CRAWLER_TOOL = StructuredTool.from_function(
    func=get_coupons,
    name="get_coupons",
    description="""
        Retrieves coupon codes for a retailer and optionally for a specific product.
    """,
    args_schema=CouponCrawlerArgs,  # Explicit schema
    infer_schema=True  # Ensure schema inference is disabled
)

COUPON_TRY_TOOL = StructuredTool.from_function(
    func=try_coupons,
    name="try_coupons",
    description="""
        Tries the input coupon codes and checks if they are valid or not.
    """,
    args_schema=CouponEvaluatorArgs,  # Explicit schema
    infer_schema=True  # Ensure schema inference is disabled
)


from tools.classes import CouponCrawlerResults, CouponEvaluatorResults
from typing import List
from pydantic import BaseModel
import random
import string

def generate_dummy_coupon_code(retailer: str, product: str|None, coupon_provider: str) -> str:
    """Generates a semi-random coupon code."""
    options = [retailer[:3], "SAVE", "DEAL", "PROMO"]
    if product:
        options.append(product[:3])
    base = random.choice(options).upper()
    random_number = "".join(random.choices(string.digits, k=2))
    provider_code = coupon_provider[:3].upper()
    return f"{base}{random_number}{provider_code}"

def get_coupons(retailer: str, product_name: str|None) -> List[CouponCrawlerResults]:
    """Generates a list of dummy coupon results for a given website and product."""
    coupon_providers = ["grabon", "groupon", "wired", "retailmenot", "couponfollow"]
    coupon_provider = random.choice(coupon_providers)

    retailer = retailer.lower()
    url = f"https://www.{coupon_provider}.com/{retailer}-coupons/"

    # Generate 5 dummy coupon codes
    codes = [generate_dummy_coupon_code(retailer, product_name, coupon_provider) for _ in range(5)]

    # Create and return the result
    return [
        CouponCrawlerResults(
            url=url,
            coupon_provider=coupon_provider,
            codes=codes,
            retailer=retailer,
            product=product_name
        )
    ]

def try_coupons(codes:List[str]) -> List[CouponEvaluatorResults]:
    results = []
    for code in codes:
        results.append(
            CouponEvaluatorResults(
                code=code,
                result=random.random() < 0.1
            )
        )
    return results

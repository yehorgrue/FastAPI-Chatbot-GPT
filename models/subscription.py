from enum import Enum


class Plan(str, Enum):
    basic = 'basic'
    pro = 'pro'
    enterprise = 'enterprise'

class Subscription():
    stripe_price_id: str = ""
    balance: float = 0.0
    plan: Plan = Plan.basic
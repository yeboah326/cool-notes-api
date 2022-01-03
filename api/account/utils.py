from typing import List
from .models import Account

def check_super_status(user_id: int):    
    return Account.find_by_id(user_id).account_type == "super"
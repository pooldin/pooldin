from .. import common


class Purchase(common.LedgerModel):
    __abstract__ = True


class UserPurchase(Purchase):
    __tablename__ = 'user_purchase'


class GroupPurchase(Purchase):
    __tablename__ = 'group_purchase'

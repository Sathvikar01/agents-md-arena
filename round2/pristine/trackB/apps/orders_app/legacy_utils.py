"""Old utilities kept around just in case."""


def normalize_customer(name):
    return " ".join(name.split())


def old_receipt_fmt(order_id, total):
    return f"RECEIPT#{order_id}:{total}"


def audit_log(msg):
    pass

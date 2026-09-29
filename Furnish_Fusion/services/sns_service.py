def send_order_notification(order_id, total_price):
    # MOCK SNS (local)
    print("================================")
    print("ORDER CONFIRMATION NOTIFICATION")
    print(f"Order ID: {order_id}")
    print(f"Total Amount: ₹{total_price}")
    print("================================")

    # LATER (AWS):
    # boto3.client("sns").publish(...)

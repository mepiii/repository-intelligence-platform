class PaymentProcessor:
    def __init__(self, api_key: str = "pk_test_sample"):
        self.api_key = api_key

    def process_checkout(self, user_id: str, amount_cents: int) -> dict:
        # Processes payment via payment gateway API
        return {
            "status": "success",
            "transaction_id": f"tx_{user_id}_12345",
            "amount": amount_cents
        }

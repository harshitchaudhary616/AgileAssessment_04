from datetime import datetime, timedelta


class DigitalWallet:
    def __init__(self):
        self.accounts = {}
        self.transactions = {}
        self.daily_limit = 50000

    def create_account(self, account_id, name, pin, balance=0):
        if account_id in self.accounts:
            raise ValueError("Account already exists")

        if balance < 0:
            raise ValueError("Initial balance cannot be negative")

        self.accounts[account_id] = {
            "name": name,
            "pin": str(pin),
            "balance": balance,
            "failed_pins": 0
        }

        self.transactions[account_id] = []

        return True

    def verify_pin(self, account_id, pin):
        if account_id not in self.accounts:
            raise ValueError("Account not found")

        if str(pin) == self.accounts[account_id]["pin"]:
            self.accounts[account_id]["failed_pins"] = 0
            return True

        self.accounts[account_id]["failed_pins"] += 1

        if self.accounts[account_id]["failed_pins"] >= 3:
            self._record_transaction(
                account_id,
                "PIN_FAILURE",
                0,
                "Multiple failed PIN attempts"
            )

        return False

    def deposit(self, account_id, amount):
        self._validate_amount(amount)

        self.accounts[account_id]["balance"] += amount

        self._record_transaction(
            account_id,
            "DEPOSIT",
            amount,
            "Normal"
        )

        return True

    def withdraw(self, account_id, amount):
        self._validate_amount(amount)

        if self.accounts[account_id]["balance"] < amount:
            raise ValueError("Insufficient balance")

        if self._daily_total(account_id) + amount > self.daily_limit:
            raise ValueError("Daily transaction limit exceeded")

        self.accounts[account_id]["balance"] -= amount

        status = self._fraud_check(account_id, amount)

        self._record_transaction(
            account_id,
            "WITHDRAW",
            amount,
            status
        )

        return True

    def transfer(self, sender, receiver, amount):
        self._validate_amount(amount)

        if sender not in self.accounts:
            raise ValueError("Sender not found")

        if receiver not in self.accounts:
            raise ValueError("Receiver not found")

        if self.accounts[sender]["balance"] < amount:
            raise ValueError("Insufficient balance")

        if self._daily_total(sender) + amount > self.daily_limit:
            raise ValueError("Daily transaction limit exceeded")

        self.accounts[sender]["balance"] -= amount
        self.accounts[receiver]["balance"] += amount

        status = self._fraud_check(sender, amount)

        self._record_transaction(
            sender,
            "TRANSFER",
            amount,
            status
        )

        self._record_transaction(
            receiver,
            "RECEIVED",
            amount,
            "Normal"
        )

        return True

    def get_balance(self, account_id):
        if account_id not in self.accounts:
            raise ValueError("Account not found")

        return self.accounts[account_id]["balance"]

    def transaction_history(self, account_id):
        if account_id not in self.accounts:
            raise ValueError("Account not found")

        return self.transactions[account_id]

    def _validate_amount(self, amount):
        if amount <= 0:
            raise ValueError("Amount must be positive")

    def _daily_total(self, account_id):
        total = 0
        today = datetime.now().date()

        for transaction in self.transactions[account_id]:
            if transaction["time"].date() == today:
                if transaction["type"] in ["WITHDRAW", "TRANSFER"]:
                    total += transaction["amount"]

        return total

    def _fraud_check(self, account_id, amount):
        suspicious = []

        current_time = datetime.now()

        recent_count = 0

        for transaction in self.transactions[account_id]:
            if current_time - transaction["time"] <= timedelta(minutes=10):
                if transaction["type"] in ["WITHDRAW", "TRANSFER"]:
                    recent_count += 1

        if recent_count >= 5:
            suspicious.append("More than 5 transactions in 10 minutes")

        if amount > 20000:
            suspicious.append("Large transaction")

        if self.accounts[account_id]["failed_pins"] >= 3:
            suspicious.append("Multiple failed PIN attempts")

        history = self.transactions[account_id]

        if len(history) >= 3:
            amounts = []

            for transaction in history[-3:]:
                if transaction["amount"] > 0:
                    amounts.append(transaction["amount"])

            if len(amounts) > 0:
                average = sum(amounts) / len(amounts)

                if amount > average * 3:
                    suspicious.append("Unusual transaction amount")

        if len(suspicious) > 0:
            return "SUSPICIOUS: " + ", ".join(suspicious)

        return "Normal"

    def _record_transaction(self, account_id, transaction_type, amount, status):
        self.transactions[account_id].append({
            "type": transaction_type,
            "amount": amount,
            "status": status,
            "time": datetime.now()
        })

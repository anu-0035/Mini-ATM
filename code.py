class Account:
    def __init__(self, account_number, pin, balance):
        self.account_number = account_number
        self.pin = pin
        self.balance = balance

    def check_balance(self):
        return self.balance

    def withdraw(self, amount):
        if amount > self.balance:
            raise Exception("Insufficient account balance")
        self.balance -= amount


class ATM:
    def __init__(self, denominations):
        """
        denominations: dict of {denomination: count}
        Example: {2000: 5, 500: 10, 100: 20}
        """
        self.denominations = denominations

    def total_cash(self):
        return sum(denom * count for denom, count in self.denominations.items())

    def can_dispense(self, amount):
        """
        Check if ATM can dispense the given amount with available notes.
        """
        to_dispense = {}
        remaining = amount

        # Use larger notes first
        for denom in sorted(self.denominations.keys(), reverse=True):
            needed = remaining // denom
            available = self.denominations[denom]
            use = min(needed, available)
            if use > 0:
                to_dispense[denom] = use
                remaining -= denom * use

        if remaining == 0:
            return True, to_dispense
        else:
            return False, {}

    def dispense_cash(self, amount):
        can_dispense, to_dispense = self.can_dispense(amount)
        if not can_dispense:
            raise Exception("ATM cannot dispense the requested amount with available denominations")

        # Deduct notes from ATM
        for denom, count in to_dispense.items():
            self.denominations[denom] -= count

        return to_dispense

    def withdraw(self, account, amount, pin):
        if pin != account.pin:
            raise Exception("Invalid PIN")

        if amount > account.check_balance():
            raise Exception("Insufficient account balance")

        if amount > self.total_cash():
            raise Exception("ATM has insufficient cash")

        can_dispense, _ = self.can_dispense(amount)
        if not can_dispense:
            raise Exception("ATM cannot dispense the requested amount with available denominations")

        # All checks passed
        account.withdraw(amount)
        notes = self.dispense_cash(amount)
        print(f"Dispensed: {notes}")


# Example usage
if __name__ == "__main__":
    # Create account with 10,000 balance
    account = Account(account_number="123456789", pin="1234", balance=10000)

    # Create ATM with denominations
    atm = ATM(denominations={2000: 5, 500: 10, 100: 20})

    print("Account balance:", account.check_balance())
    print("ATM total cash:", atm.total_cash())

    try:
        atm.withdraw(account, amount=3700, pin="1234")
    except Exception as e:
        print("Withdrawal failed:", e)

    print("Account balance after:", account.check_balance())
    print("ATM total cash after:", atm.total_cash())
    print("ATM denominations:", atm.denominations)

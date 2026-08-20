from DigitalWallet import DigitalWallet


wallet = DigitalWallet()

wallet.create_account("A101", "Harshit", "1234", 30000)
wallet.create_account("A102", "Rahul", "5678", 10000)

print("Test 1: Normal transaction")

assert wallet.deposit("A101", 5000) == True
assert wallet.get_balance("A101") == 35000

print("PASS")


print("Test 2: Insufficient balance")

try:
    wallet.withdraw("A102", 20000)
    assert False
except ValueError:
    assert True

print("PASS")


print("Test 3: Daily transaction limit")

wallet.daily_limit = 1000

try:
    wallet.withdraw("A101", 2000)
    assert False
except ValueError:
    assert True

wallet.daily_limit = 50000

print("PASS")


print("Test 4: Multiple failed PINs")

wallet.verify_pin("A101", "1111")
wallet.verify_pin("A101", "2222")
wallet.verify_pin("A101", "3333")

history = wallet.transaction_history("A101")

found = False

for transaction in history:
    if transaction["type"] == "PIN_FAILURE":
        found = True

assert found == True

print("PASS")


print("Test 5: Suspicious transaction")

wallet.withdraw("A101", 25000)

history = wallet.transaction_history("A101")

found = False

for transaction in history:
    if "SUSPICIOUS" in transaction["status"]:
        found = True

assert found == True

print("PASS")


print("Test 6: Duplicate transaction")

initial_balance = wallet.get_balance("A102")

wallet.transfer("A101", "A102", 1000)

wallet.transfer("A101", "A102", 1000)

assert wallet.get_balance("A102") == initial_balance + 2000

print("PASS")


print("Test 7: Negative amount")

try:
    wallet.deposit("A101", -500)
    assert False
except ValueError:
    assert True

print("PASS")


print("Test 8: Balance verification")

balance = wallet.get_balance("A101")

assert balance >= 0

print("PASS")


print("All Wallet tests passed")

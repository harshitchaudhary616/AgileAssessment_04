from InventoryManagement import InventoryManagement


inventory = InventoryManagement()

inventory.add_product("A", "Laptop", 100)
inventory.add_product("B", "Laptop", 50)
inventory.add_product("C", "Laptop", 20)

inventory.add_product("A", "Phone", 5)

print("Test 1: Stock availability")

assert inventory.get_stock("A", "Laptop") == 100

print("PASS")


print("Test 2: Insufficient inventory")

try:
    inventory.remove_product("A", "Laptop", 200)
    assert False
except ValueError:
    assert True

print("PASS")


print("Test 3: Warehouse transfer")

inventory.transfer_stock("A", "B", "Laptop", 20)

assert inventory.get_stock("A", "Laptop") == 80
assert inventory.get_stock("B", "Laptop") == 70

print("PASS")


print("Test 4: Reorder threshold")

low_stock = inventory.check_low_stock()

found = False

for warehouse, product, quantity in low_stock:

    if warehouse == "A" and product == "Phone":
        found = True

assert found == True

print("PASS")


print("Test 5: Invalid product")

try:
    inventory.remove_product("A", "Tablet", 5)
    assert False
except ValueError:
    assert True

print("PASS")


print("Test 6: Negative inventory")

try:
    inventory.add_product("A", "Laptop", -10)
    assert False
except ValueError:
    assert True

print("PASS")


print("Test 7: Multiple warehouses")

warehouse = inventory.find_warehouse("Laptop", 30)

assert warehouse is not None

print("PASS")


print("Test 8: Warehouse selection")

warehouse = inventory.fulfill_order("Laptop", 40)

assert warehouse == "A"

assert inventory.get_stock("A", "Laptop") == 40

print("PASS")


print("Test 9: Reorder")

inventory.reorder("C", "Laptop", 50)

assert inventory.get_stock("C", "Laptop") == 70

print("PASS")


print("Test 10: Supplier management")

inventory.add_supplier("S101", "ABC Suppliers")

assert inventory.suppliers["S101"] == "ABC Suppliers"

print("PASS")


print("All Inventory tests passed")

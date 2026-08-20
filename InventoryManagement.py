import threading


class InventoryManagement:

    def __init__(self):
        self.warehouses = {
            "A": {},
            "B": {},
            "C": {}
        }

        self.suppliers = {}

        self.reorder_threshold = 10

        self.lock = threading.Lock()

    def add_product(self, warehouse, product, quantity):
        if warehouse not in self.warehouses:
            raise ValueError("Invalid warehouse")

        if quantity <= 0:
            raise ValueError("Quantity must be positive")

        with self.lock:
            if product not in self.warehouses[warehouse]:
                self.warehouses[warehouse][product] = 0

            self.warehouses[warehouse][product] += quantity

        return True

    def remove_product(self, warehouse, product, quantity):
        if warehouse not in self.warehouses:
            raise ValueError("Invalid warehouse")

        if product not in self.warehouses[warehouse]:
            raise ValueError("Invalid product")

        if quantity <= 0:
            raise ValueError("Quantity must be positive")

        with self.lock:
            if self.warehouses[warehouse][product] < quantity:
                raise ValueError("Insufficient inventory")

            self.warehouses[warehouse][product] -= quantity

        return True

    def transfer_stock(self, source, destination, product, quantity):
        if source not in self.warehouses:
            raise ValueError("Invalid source warehouse")

        if destination not in self.warehouses:
            raise ValueError("Invalid destination warehouse")

        if product not in self.warehouses[source]:
            raise ValueError("Product not found")

        if quantity <= 0:
            raise ValueError("Quantity must be positive")

        with self.lock:

            if self.warehouses[source][product] < quantity:
                raise ValueError("Insufficient stock")

            self.warehouses[source][product] -= quantity

            if product not in self.warehouses[destination]:
                self.warehouses[destination][product] = 0

            self.warehouses[destination][product] += quantity

        return True

    def get_stock(self, warehouse, product):
        if warehouse not in self.warehouses:
            raise ValueError("Invalid warehouse")

        if product not in self.warehouses[warehouse]:
            raise ValueError("Invalid product")

        return self.warehouses[warehouse][product]

    def find_warehouse(self, product, quantity):
        best_warehouse = None
        best_stock = 0

        for warehouse in self.warehouses:
            stock = self.warehouses[warehouse].get(product, 0)

            if stock >= quantity:
                if stock > best_stock:
                    best_stock = stock
                    best_warehouse = warehouse

        return best_warehouse

    def reorder(self, warehouse, product, quantity):
        if quantity <= 0:
            raise ValueError("Invalid reorder quantity")

        self.add_product(warehouse, product, quantity)

        return True

    def check_low_stock(self):
        low_stock = []

        for warehouse in self.warehouses:

            for product in self.warehouses[warehouse]:

                quantity = self.warehouses[warehouse][product]

                if quantity <= self.reorder_threshold:
                    low_stock.append(
                        (warehouse, product, quantity)
                    )

        return low_stock

    def add_supplier(self, supplier_id, name):
        self.suppliers[supplier_id] = name

        return True

    def fulfill_order(self, product, quantity):
        warehouse = self.find_warehouse(product, quantity)

        if warehouse is None:
            raise ValueError("Product unavailable")

        self.remove_product(
            warehouse,
            product,
            quantity
        )

        return warehouse

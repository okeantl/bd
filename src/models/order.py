class Order:
    def __init__(self, user, products):
        self.user = user
        self.products = products
    
    def calculate_total(self):
        total = 0
        for product in self.products:
            total = total + product.get_total_price()
        return total

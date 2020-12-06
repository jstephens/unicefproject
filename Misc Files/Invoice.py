class Invoice:

    def __init__(self):
        self.items ={}

    def addProduct(self, qnt, price, discount):
        self.items['qnt'] = qnt
        self.items['unit_price'] = price
        self.items['discount'] = discount
        return self.items


    def totalImpurePrice(self, products):
        total_impure_price = 0
        for k, v in products.items():
            total_impure_price += float(v['unit_price']) * int(v['qnt'])
        total_impure_price = round(total_impure_price, 2)
        return total_impure_price

    def bulkDiscount(self,products):
        bulk_discount = 0
        for k, v in products.items():
            if(v['qnt'] > 10):
                bulk_discount += (v['unit_price'] * 0.10)
        return bulk_discount

    def totalDiscount(self, products):
        total_discount = 0
        bulk_discount = 0

        for k, v in products.items():
            total_discount += (float(v['unit_price']) * int(v['qnt'])) * float(v['discount']) / 100
        for k, v in products.items():
            if (v['qnt'] > 10):
                bulk_discount -= (float(v['unit_price']) * int(v['qnt'])) * 0.01
        total_discount += bulk_discount
        total_discount = round(total_discount, 2)
        self.total_discount = total_discount
        return total_discount

    def totalPurePrice(self, products):
        total_pure_price = self.totalImpurePrice(products)-self.totalDiscount(products)
        return total_pure_price

    def inputAnswer(self,input_value):
        while True:
            userInput = input(input_value)
            if userInput in ['y', 'n']:
                return userInput
            print("y or n! Try again.")

    def inputNumber(self, input_value):
        while True:
            try:
                userInput = float(input(input_value))
            except ValueError:
                print("Not a number! Try again.")
                continue
            else:
                return userInput

    def averageDiscount(self, products):
        for v in products.items():
            avg_discount = round(sum(d['qnt'] for d in products.values() if d) / self.totalDiscount(products), 2)
        return avg_discount

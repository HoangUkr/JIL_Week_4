#Return all Customers from customer table
customers = Customer.objects.all()

#Return first customer in table
firstCustomer = Customer.objects.first()

#Return last customer in table
lastCustomer = Customer.objects.last()

#Return single customer by name
customerByName = Customer.objects.get(name='Yura Protsiuk')

#Return single customer by name
customereById = Customer.objects.get(id=1)

#Return all order related to customer
firstCustomer.order_set.all()

#Return orders customer name
order = Order.objects.first()
parentName = order.customer.name

#Return product from product table with value of 'Out Door' in category attribute
products = Product.objects.filter(category="Out Door")

#Order object by id
leastToGreatest = Product.objects.all().order_by('id')
greatestToLeast = Product.objects.all().order_by('-id')

#Return all product with tag of Sport
productFiltered = Product.objects.filter(tags__name = "Sport")

#Return the total count for number of time a Ball was ordered by the first customer
ballOrders = firstCustomer.order_set.filter(product__name="Ball").count()

#Return total count for each product order
allOrders = {}
for order in firstCustomer.order_set.all():
    if(order.product.name in allOrders):
        allOrders[order.product.name] += 1
    else:
        allOrders[order.product.name] = 1

#Related Set Example
class ParentModel(models.Model):
    name = models.CharField(max_length=200, null=True)

class ChildModel(models.Model):
    parent = models.ForeignKey(ParentModel)
    name = models.CharField(max_length=200, null=True)

parent = ParentModel.objects.first()
parent.childmodel_set.all()
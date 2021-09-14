from django.db import models
from django.utils.timezone import now


# Create your models here.

# <HINT> Create a Car Make model `class CarMake(models.Model)`:
# - Name
# - Description
# - Any other fields you would like to include in car make model
# - __str__ method to print a car make object

class CarMake(models.Model):
  name = models.CharField(max_length=75)
  description = models.CharField(max_length=300)
  def __str__(self):
      return "Name: " + self.name + "," + \
             "Type: " + self.description,


# <HINT> Create a Car Model model `class CarModel(models.Model):`:
# - Many-To-One relationship to Car Make model (One Car Make has many Car Models, using ForeignKey field)
# - Name
# - Dealer id, used to refer a dealer created in cloudant database
# - Type (CharField with a choices argument to provide limited choices such as Sedan, SUV, WAGON, etc.)
# - Year (DateField)
# - Any other fields you would like to include in car model
# - __str__ method to print a car make object
class CarModel(models.Model):
  name = models.CharField(max_length=75)
  dealerId = models.IntegerField()
  SEDAN = 'sedan'
  SUV = 'suv'
  WAGON = 'wagon'
  OTHERS = 'others'
  CAR_CHOICES = [(SEDAN, "Sedan"), (SUV, 'SUV'), (WAGON, 'Wagon'), (OTHERS, 'Others')]
  type = models.CharField(null=False, max_length=40, choices=CAR_CHOICES, default=SEDAN)
  year = models.DateField()
  make = models.ForeignKey(CarMake, on_delete=models.CASCADE)
  def __str__(self):
      return "Name: " + self.name + "," + \
             "Type: " + self.type,



# <HINT> Create a plain Python class `CarDealer` to hold dealer data


# <HINT> Create a plain Python class `DealerReview` to hold review data

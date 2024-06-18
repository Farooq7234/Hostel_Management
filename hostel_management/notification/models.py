from django.db import models

# Create your models here.
class Student(models.Model):
    reg_no = models.CharField(max_length=50, unique=True, blank=False)
    name = models.CharField(max_length=100)
    room_no = models.CharField(max_length=10)
    cours = [('B.E(UG)', 'B.E(UG)'), ('M.E(PG)', 'M.E(PG)'), ('MCA', 'MCA')]
    course = models.CharField(max_length=100, choices=cours, blank=False, null=False)
    DEPT = [("civil", "civil"), ("CSE", "CSE"), ("ECE", "ECE"), ("MECH", "MECH"), ("EEE", "EEE")]
    branch = models.CharField(max_length=100, choices=DEPT, blank=False, null=False)
    hos_name = [('G1', 'G1'), ('G2', 'G2'), ('B1', 'B1'), ('B2', 'B2'), ('B3', 'B3')]
    hostel_name = models.CharField(max_length=100, choices=hos_name, blank=False, null=False)
    year_of_study = models.IntegerField()
    email = models.EmailField(max_length=70, blank=True, unique=True)
    phone_number = models.CharField(max_length=15, blank=True) 

    def __str__(self):
        return self.name

class Attendance(models.Model):
    reg_no = models.ForeignKey(Student, on_delete=models.CASCADE)
    date = models.DateField()
    present = models.BooleanField(default=True)

class Bill(models.Model):
    reg_no = models.ForeignKey(Student, on_delete=models.CASCADE)
    amount = models.DecimalField(max_digits=10, decimal_places=2)
    date_issued = models.DateField(auto_now_add=True)
    due_date = models.DateField()
    paid = models.BooleanField(default=False)
    reference_number = models.CharField(max_length=100, unique=True)

    def __str__(self):
        return f"{self.reg_no.name} - {self.amount} - {'Paid' if self.paid else 'Unpaid'}"

class Expenditure(models.Model):
    date = models.DateField()
    milk = models.DecimalField(max_digits=10, decimal_places=2)
    gas = models.DecimalField(max_digits=10, decimal_places=2)
    groceries = models.DecimalField(max_digits=10, decimal_places=2)
    vegetables = models.DecimalField(max_digits=10, decimal_places=2)
    
    @property
    def total_expenditure(self):
        return self.milk + self.gas + self.groceries + self.vegetables

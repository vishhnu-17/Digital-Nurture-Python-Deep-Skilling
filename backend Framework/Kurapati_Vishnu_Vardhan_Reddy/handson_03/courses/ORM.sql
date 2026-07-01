17:
>>> Course.objects.filter(department__name="Computer Science")
<QuerySet [<Course: Python Programming>, <Course: Database Systems>]>

18:
from django.db.models import Count
>>> depts= Department.objects.annotate(count=Count('course'))
>>> print(depts)
<QuerySet [<Department: Computer Science>, <Department: Information Technology>]>
>>> for d in depts:
... print(d.name,d.count)
Computer Science 2
Information Technology 2

using values and annotate
>>> depts= Department.objects.values("name").annotate(count=Count("course"))
<QuerySet [{'name': 'Computer Science', 'count': 2}, {'name': 'Information Technology', 'count': 2}]>

19:
>>> from django.db import connection
>>> obj= Student.objects.select_related('department')
>>> for i in obj:
...  print(i.first_name, i.department.name)
... 
Arjun Computer Science
Sneha Computer Science
Rahul Information Technology
Meena Information Technology
Kiran Computer Science
>>> print(len(connection.queries))
7

20:
>>> from django.db.models import F
>>> Department.objects.update(budget=F('budget')*1.1)
2
from django.contrib import admin

# Register your models here.
from app2.models import Employee, Students1, Classes, Book, Press, Author, AuthorDetail

admin.site.register(Employee)
admin.site.register(Students1)
admin.site.register(Classes)
admin.site.register(Book)
admin.site.register(Press)
admin.site.register(Author)
admin.site.register(AuthorDetail)
from django.contrib import admin
from .models import Host, Meeting

# Register your models here
admin.site.register(Host)
#Added a subsection to Modify admin depending on privilledges 
admin.site.register(Meeting, ModifyAdmin)

from django.contrib import admin
from .models import Host, Meeting

# Register your models here
class ModifyAdmin(admin.ModelAdmin):
    list_display = ['id','visitor_name','visitor_phone','date','time_in','time_out']
    search_fields = ['id','visitor_name','visitor_phone', 'location']

admin.site.register(Host)
#Added a subsection to Modify admin depending on priviledges 
admin.site.register(Meeting, ModifyAdmin)

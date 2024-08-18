from django.contrib import admin
from django.contrib.auth.models import Group, User

# Register your models here.
admin.site.site_title = "Punjab Court Administrator Console"
admin.site.site_header = "Punjab Court Administrator Console"
admin.site.unregister(Group)
admin.site.unregister(User)


from .models import CaseDetails

class CaseDetailsAdmin(admin.ModelAdmin):

    list_display = ('case_id', 'case_filing_date', 'complainant_name', 'respondent_name', 'registration_rera_number')
    list_filter = ('case_type', 'rera_project', 'bench_name', 'court_address')
    search_fields = ['case_id', 'case_filing_date', 'complainant_name', 'respondent_name', 'registration_rera_number', 'case_type', 'rera_project', 'bench_name', 'court_address']

admin.site.register(CaseDetails, CaseDetailsAdmin)    

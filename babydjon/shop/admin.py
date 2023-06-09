from django.contrib import admin
from .models import *
from django.db import connection

admin.site.register(Producer)
admin.site.register(Category)
@admin.register(Personal)
class PersonalAdmin(admin.ModelAdmin):
    change_list_template="admin/avg_salary.html"
    def changelist_view(self, request, extra_context=None):
        sqlQuery="""select avg([Personal].[Salary])
				from [Personal]"""
        sqlQueryMax="""select max([Personal].[Salary])
				from [Personal]"""
        sqlQueryMin="""select min([Personal].[Salary])
				from [Personal]"""
        response = super().changelist_view(
            request,
            extra_context=extra_context,
        )
        try:
            qs = response.context_data['cl'].queryset
        except (AttributeError, KeyError):
            return response
        response.context_data['avgSalary'] = connection.cursor().execute(sqlQuery).fetchone()[0]
        response.context_data['maxSalary'] = connection.cursor().execute(sqlQueryMax).fetchone()[0]
        response.context_data['minSalary'] = connection.cursor().execute(sqlQueryMin).fetchone()[0]
        return response

@admin.register(OfflineStore)
class OfflineStoreAdmin(admin.ModelAdmin):
    change_list_template="admin/offlineStoreAdmin.html"
    def changelist_view(self, request, extra_context=None):
        response = super().changelist_view(
            request,
            extra_context=extra_context,
        )
        try:
            qs = response.context_data['cl'].queryset
        except (AttributeError, KeyError):
            return response
        response.context_data['addresses'] = []
        for i in connection.cursor().execute("select top 100 [OfflineStore].[Id], [OfflineStore].[Address] from [OfflineStore]"):
           count = connection.cursor().execute(f"""select sum([OfflineStoreProducts].[Count]) 
	from [OfflineStoreProducts]
	join [OfflineStore] on (
		[OfflineStoreProducts].[OfflineStore] = [OfflineStore].[Id] and [OfflineStore].[Id] = {i[0]})""").fetchone()[0]
           response.context_data['addresses'].append({"address" : i[1], "count" : count})
        return response
# Register your models here.

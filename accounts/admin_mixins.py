from django.urls import path
from django.http import HttpResponse, HttpResponseRedirect
from django.template.response import TemplateResponse
from django import forms
from django.contrib import messages
import xlwt
import xlrd
from django.core.validators import FileExtensionValidator

class ExcelImportForm(forms.Form):
    excel_file = forms.FileField(validators=[FileExtensionValidator(allowed_extensions=['xls', 'xlsx'])])

class ExportImportAdminMixin:
    def get_urls(self):
        custom_urls = [
            path('download-format/', self.admin_site.admin_view(self.download_format), name=f'{self.model._meta.app_label}_{self.model._meta.model_name}_download_format'),
            path('import-xls/', self.admin_site.admin_view(self.import_xls), name=f'{self.model._meta.app_label}_{self.model._meta.model_name}_import_xls'),
        ]
        return custom_urls + super().get_urls()

    def download_format(self, request):
        model_fields = [f.name for f in self.model._meta.fields if f.name not in ['id', 'password', 'last_login', 'date_joined']]
        response = HttpResponse(content_type='application/ms-excel')
        response['Content-Disposition'] = 'attachment; filename=users_format.xls'
        wb = xlwt.Workbook(encoding='utf-8')
        ws = wb.add_sheet('Users Format')
        for col_num, field in enumerate(model_fields):
            ws.write(0, col_num, field)
        wb.save(response)
        return response

    def import_xls(self, request):
        if request.method == "POST":
            form = ExcelImportForm(request.POST, request.FILES)
            if form.is_valid():
                excel_file = request.FILES['excel_file']
                book = xlrd.open_workbook(file_contents=excel_file.read())
                sheet = book.sheet_by_index(0)
                headers = [cell.value.strip() for cell in sheet.row(0)]
                success_count = 0
                for row_idx in range(1, sheet.nrows):
                    row_data = {headers[col]: sheet.cell_value(row_idx, col) for col in range(len(headers))}
                    try:
                        self.model.objects.create(**row_data)
                        success_count += 1
                    except Exception as e:
                        messages.error(request, f"Row {row_idx + 1} error: {str(e)}")
                self.message_user(request, f"{success_count} users successfully imported.")
                return HttpResponseRedirect("../")
        else:
            form = ExcelImportForm()

        context = dict(
            self.admin_site.each_context(request),
            form=form,
            opts=self.model._meta,
        )
        return TemplateResponse(request, "admin/import_form.html", context)

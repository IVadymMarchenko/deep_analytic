from django.http import HttpResponseRedirect
from django.shortcuts import redirect, render
from django.urls import reverse
from .utils import FileAssistant
from .forms import MyFileForm
import pandas as pd
from django.contrib import messages
from django.views.generic.edit import FormView
from django.views.generic.base import TemplateView
from .models import MyFile
# Create your views here.

class UploadFileView(FormView):
    form_class = MyFileForm
    template_name = "app_analysator/upload_files.html"
    success_url = 'analysator:table'
    reverse_url = 'users:login'


    def form_valid(self, form):
       fp = MyFile(file=form.cleaned_data['file'],user = self.request.user)
       fp.save()
       return HttpResponseRedirect(reverse(self.success_url))


    def form_invalid(self, form):
        # Добавляем ошибки формы в сообщения
        for field, errors in form.errors.items():
            for error in errors:
                messages.error(self.request, f"{field}: {error}")
        return self.render_to_response(self.get_context_data(form=form))
    

    def dispatch(self, request, *args, **kwargs):  
        if not request.user.is_authenticated:
            return redirect(reverse(self.reverse_url))
        return super().dispatch(request, *args, **kwargs)




class TableView(TemplateView):
    model = MyFile
    template_name = "app_analysator/table.html"





def upload_text_data(request):
    return render(request, "app_analysator/upload_text_data.html")


def viewtable(request):
    return render(request, "app_analysator/table.html")


def upload_and_display_data(request):
    if request.method == "POST":
        form = MyFileForm(request.POST, request.FILES)
        print(request.FILES)
        if form.is_valid():
            try:
                # Получаем файл
                uploaded_file = request.FILES["file"]
                # Используем FileAssistant для чтения данных
                df = FileAssistant.read_file(uploaded_file)
                df['empty values'] =  df.isnull().sum(axis=1)
                num_rows, num_cols = df.shape # количество строк количество стобцов
                return render(
                    request,
                    "app_analysator/table.html",
                    {
                        "columns": df.columns,  # Названия столбцов
                        "data": df.values,  # Данные строк
                        "num_rows": num_rows, # количество строк
                        'num_cols': num_cols, #количество стобцов
                    },
                )
            except Exception as e:
                # Обрабатываем ошибку
                return render(request, "upload_error.html", {"error_message": str(e)})

    else:
        form = MyFileForm()

    return render(request, "app_analysator/upload_files.html", {"form": form})

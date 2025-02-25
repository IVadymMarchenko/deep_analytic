import urllib.parse
from django.http import HttpResponseRedirect, JsonResponse
from django.shortcuts import redirect, render
from django.urls import reverse
from django.views import View
from .utils import FileAssistant,DataProcesor,AuthenticatedView
from .forms import MyFileForm
import pandas as pd
from django.contrib import messages
from django.views.generic.edit import FormView
from django.views.generic.base import TemplateView
from .models import MyFile
from .graps_type import graph_types
from urllib.parse import urlencode
from app_display_data.func_name import aggregation_functions
from django.core.paginator import Paginator
# Create your views here.

class UploadFileView(AuthenticatedView,FormView):
    form_class = MyFileForm
    template_name = "app_analysator/upload_files.html"
    success_url = 'analysator:table'


    def form_valid(self, form):
       fp = MyFile(file=form.cleaned_data['file'],user = self.request.user)
       print('saving')
       fp.save()
       return HttpResponseRedirect(reverse(self.success_url))


    def form_invalid(self, form):
        for field, errors in form.errors.items():
            for error in errors:
                messages.error(self.request, f"{field}: {error}")
        return self.render_to_response(self.get_context_data(form=form))
    

class TableView(AuthenticatedView, TemplateView):
    model = MyFile
    template_name = "app_analysator/table.html"

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        last_file = MyFile.objects.filter(user=self.request.user).order_by('-uploaded_at').first()
        context['last_file'] = last_file

        if last_file:
            uploaded_file = last_file.file
            df = FileAssistant.read_file(uploaded_file)
            df = DataProcesor.add_emty_values_columns(df)
            num_rows, num_cols = DataProcesor.get_data_shape(df)

            # Настройка пагинации
            paginator = Paginator(df.values, 50)
            page_number = self.request.GET.get('page')
            page_obj = paginator.get_page(page_number)

            context.update({
                "columns": df.columns,  # Названия столбцов
                "page_obj": page_obj,  # Страница с данными
                "num_rows": num_rows,  # Количество строк
                "num_cols": num_cols,  # Количество столбцов
            })

        return context




class MakeGraphsView(AuthenticatedView,TemplateView):
    model = MyFile
    template_name = "app_analysator/make_graphs.html"
    success_url = "display_data:view_data" 


    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        last_file = MyFile.objects.filter(user=self.request.user).order_by('-uploaded_at').first()
        if last_file:
            uploaded_file = last_file.file
            df = FileAssistant.read_file(uploaded_file) 
            df = DataProcesor.add_emty_values_columns(df)
            context.update({
                "columns": df.columns,  # Названия столбцов
                "type_graps": graph_types, # типы графиков
                "aggregation_functions":aggregation_functions, # функ агригац
            })
        return context
    

    def post(self, request, *args, **kwargs):
        # Получение данных из POST-запроса
        x_axis = request.POST.get("x_axis")
        y_axis = request.POST.getlist("y_axis")  # Чекбоксы
        graph_type = request.POST.get("graph_type")
        aggregation_function = request.POST.get("aggregation_function")
        print(aggregation_function)

        if not x_axis or not y_axis or not graph_type or not aggregation_function:
            messages.error(request, 'Please fill in all fields.')
            return redirect(request.path)  # Перенаправление на ту же страницу
        context = {'x_axis': x_axis,
                   'y_axis': y_axis,
                   'graph_type': graph_type,
                   'aggregation_functions':aggregation_function}
        
        request.session['x_axis'] = x_axis
        request.session['y_axis'] = y_axis
        request.session['graph_type'] = graph_type
        request.session['aggregation_function'] = aggregation_function
         # Перенаправляем на страницу с графиками
        return redirect('display_data:view_data')
        
        

        

#ggggggggggggggggggggggggggggggggggggggggggggggggggggggggggggggggggggggggggggggggggggggggggggggggggggggggg
class TableDataView(View):
    def get(self, request):
        page = int(request.GET.get('page', 1))
        last_file = MyFile.objects.filter(user=request.user).order_by('-uploaded_at').first()

        if not last_file:
            return JsonResponse({"error": "No file found"}, status=400)

        uploaded_file = last_file.file
        df = FileAssistant.read_file(uploaded_file)
        df = DataProcesor.add_emty_values_columns(df)

        paginator = Paginator(df.values.tolist(), 20)
        page_obj = paginator.get_page(page)

        columns = df.columns.tolist()
        rows = page_obj.object_list

        # Для передачи данных в шаблон
        return render(request, 'app_analysator/table.html', {
            'columns': columns,
            'data': rows,
            'totalPages': paginator.num_pages,
            'num_cols': len(columns),
            'num_rows': len(df)
        })

#gggggggggggggggggggggggggggggggggggggggggggggggggggggggggggggggggggggggggggggggggggggggggggggggggggggggggggggggggggg


def upload_text_data(request):
    return render(request, "app_analysator/upload_text_data.html")
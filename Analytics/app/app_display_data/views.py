from matplotlib import pyplot as plt
from app_analysator.utils import DataProcesor, FileAssistant
from app_analysator.models import MyFile
import io
import base64
import matplotlib
from .utils import MakeGraphBar
from django.views.generic import TemplateView

matplotlib.use("Agg")


class ViewData(MakeGraphBar,TemplateView):
    """
    Class for displaying data and plotting graphs.
    """
    template_name = "app_display_data/display_data.html"

    def get_last_uploaded_file(self, user):
        """
        Get the user's last uploaded file.
        :param user: Current user.
        :return: Last uploaded file or None.
        """
        try:
            return MyFile.objects.filter(user=user).order_by("-uploaded_at").first()
        except Exception as e:
            return None, str(e)
        

    def get_context_data(self, **kwargs):
        """Get context for the template.
        :param kwargs: Additional parameters.
        :return: Data context.
        """
        context = super().get_context_data(**kwargs)
        request = self.request
        errors = []
        try:
            x_axis = request.session.get("x_axis", "default_x")
            y_axis = request.session.get("y_axis", ["default_y"])
            graph_type = request.session.get("graph_type", "Line Chart")
            aggregation_function = request.session.get("aggregation_function")
        except Exception as e:
            errors.append(f"Error retrieving session parameters: {str(e)}")
            context["errors"] = errors
            return context
        # Получение последнего загруженного файла
        last_file = self.get_last_uploaded_file(request.user)
        if not last_file:
            errors.append("No files uploaded or an error occurred.")
            context["errors"] = errors
            return context
        try:
            # Построение графика
            uploaded_file = last_file.file
            df = FileAssistant.read_file(uploaded_file)
            df = DataProcesor.add_emty_values_columns(df)

            if graph_type == "Bar Chart":
                self.make_bar_char(df, x_axis, y_axis, aggregation_function)

            # Сохранение графика в base64
            buf = io.BytesIO()
            plt.savefig(buf, format="png")
            buf.seek(0)
            context["chart_url"] = (
                f"data:image/png;base64,{base64.b64encode(buf.read()).decode('utf-8')}"
            )
            buf.close()
        except FileNotFoundError:
            errors.append("File not found. Please upload the file.")
        except ValueError as ve:
            errors.append(f"Error processing data: {str(ve)}")
        except Exception as e:
            errors.append(f"Data does not match")
        context["errors"] = errors
        return context

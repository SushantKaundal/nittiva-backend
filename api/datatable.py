from rest_framework.response import Response
from rest_framework.views import APIView
from django.db.models import Q
def datatables_response(request, qs, serializer_class, search_fields):
    draw = int(request.GET.get('draw', '1'))
    start = int(request.GET.get('start', '0'))
    length = int(request.GET.get('length', '10'))
    search_value = request.GET.get('search[value]', '').strip()
    if search_value and search_fields:
        q = Q()
        for f in search_fields: q |= Q(**{f"{f}__icontains": search_value})
        qs = qs.filter(q)
    order_col = request.GET.get('order[0][column]')
    order_dir = request.GET.get('order[0][dir]', 'asc')
    if order_col is not None:
        col_name = request.GET.get(f'columns[{order_col}][data]', None)
        if col_name:
            if order_dir == 'desc': col_name = '-' + col_name
            qs = qs.order_by(col_name)
    records_total = qs.model.objects.count()
    records_filtered = qs.count()
    page = qs[start:start+length]
    data = serializer_class(page, many=True).data
    return Response({'draw':draw,'recordsTotal':records_total,'recordsFiltered':records_filtered,'data':data})
class UsersDT(APIView):
    def get(self, request):
        from django.contrib.auth import get_user_model
        from .serializers import UserSerializer
        User = get_user_model(); qs = User.objects.all()
        return datatables_response(request, qs, UserSerializer, ['email','name','role'])
class ClientsDT(APIView):
    def get(self, request):
        from .models import Client; from .serializers import ClientSerializer
        qs = Client.objects.all(); return datatables_response(request, qs, ClientSerializer, ['name','email','phone','company'])
class ProjectsDT(APIView):
    def get(self, request):
        from .models import Project; from .serializers import ProjectSerializer
        qs = Project.objects.all(); return datatables_response(request, qs, ProjectSerializer, ['name','description','status'])
class TasksDT(APIView):
    def get(self, request):
        from .models import Task; from .serializers import TaskSerializer
        qs = Task.objects.all(); return datatables_response(request, qs, TaskSerializer, ['title','description','status'])
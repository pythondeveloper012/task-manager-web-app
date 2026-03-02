import sys, os, django

# set the settings module manually
project_root = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
sys.path.append(project_root)

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'todo.settings')
django.setup()

from tasks.models import Task
from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework import status
from rest_framework.permissions import IsAuthenticated
from rest_framework_simplejwt.tokens import RefreshToken
from tasks.serializer import TaskSerializer
from tasks.serializer import RegisterSerializer
from django.views.generic import TemplateView

class FrontendAppView(TemplateView):
    template_name = "tasks/index.html"

class RegisterView(APIView):
    def post(self, request):
        serializer = RegisterSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(
                {"message": "User registered successfully!"},
                status=status.HTTP_201_CREATED
            )
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

class Get_Post_Users_Data(APIView):
    
    permission_classes = [IsAuthenticated]

    def get(self, request):
        users = Task.objects.all()
        serializer = TaskSerializer(users, many=True)
        return Response(serializer.data, status=status.HTTP_200_OK)

    def post(self, request):
        serialize = TaskSerializer(data=request.data, context={'request': request})
        if serialize.is_valid():
            serialize.save()
            return Response({"Message": "User's Created Successfully", "data": serialize.data}, status=status.HTTP_201_CREATED)
        return Response(serialize.errors, status=status.HTTP_400_BAD_REQUEST)
    
class User_Update_and_Delete_view(APIView):
    permission_classes = [IsAuthenticated]
    
    def get_obj(self, pk):
        try:
            user = Task.objects.get(pk=pk)
            return user
        except:
            return None
        
    def get(self, request, pk):
        user = self.get_obj(pk)
        if not user:
            return Response({"Error": "User's Not Found!"},status=status.HTTP_404_NOT_FOUND)
        serialize = TaskSerializer(user)
        return Response(serialize.data, status=status.HTTP_200_OK)
    
    def delete(self, request, pk):
        user = self.get_obj(pk)
        if user:
            user.delete()
            return Response({"Message": "User's Deleted Successfully!"}, status=status.HTTP_204_NO_CONTENT)
        else:
            return Response({"Error": "User's ID Not Found!"}, status=status.HTTP_400_BAD_REQUEST)
        
    def patch(self, request, pk):
        item = self.get_obj(pk)
        if not item:
            return Response({"Error": "Item with this ID not found!"}, status=status.HTTP_404_NOT_FOUND)

        data = request.data
        user_id = data.get("user")
        if user_id:
            from django.contrib.auth.models import User
            try:
                user = User.objects.get(id=user_id)
                item.user = user
            except User.DoesNotExist:
                return Response(
                {"error": "User with this ID does not exist"},
                status=status.HTTP_400_BAD_REQUEST
            )
        item.title = data.get("title", item.title)
        item.description = data.get("description", item.description)
        item.is_completed = data.get("is_completed", item.is_completed)
        item.due_date = data.get("due_date", item.due_date)

        item.save()
        return Response({"message": "Item updated successfully!"})

        




    

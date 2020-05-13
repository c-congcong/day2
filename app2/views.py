from django.shortcuts import render

# Create your views here.
from rest_framework.response import Response
from rest_framework.views import APIView

from app2.models import Employee
from app2.serializers import EmployeeModelSerializer, EmployeeDeserializer


class EmployeeAPIView(APIView):

    def get(self, request, *args, **kwargs):
        emp_id = kwargs.get("id")

        if emp_id:
            try:
                emp_obj = Employee.objects.get(pk=emp_id)
                emp_ser = EmployeeModelSerializer(emp_obj).data
                return Response({
                    "status": 200,
                    "message": "用户查询成功",
                    "results": emp_ser,
                })
            except:
                return Response({
                    "status": 500,
                    "message": "用户不存在"
                })

        else:
            emp_list = Employee.objects.all()
            emp_ser = EmployeeModelSerializer(emp_list, many=True).data
            return Response({
                "status": 200,
                "message": "用户列表查询成功",
                "results": emp_ser,
            })

    def post(self, request, *args, **kwargs):

        request_data = request.data

        if not isinstance(request_data, dict) or request_data == {}:
            return Response({
                "status": 500,
                "message": "数据有误"
            })

        deserializer = EmployeeDeserializer(data=request_data)

        if deserializer.is_valid():
            emp_obj = deserializer.save()
            print(emp_obj)
            return Response({
                "status": 200,
                "message": "用户创建成功",
                "results": EmployeeModelSerializer(emp_obj).data
            })
        else:
            return Response({
                "status": 500,
                "message": "用户创建失败",
                "results": deserializer.errors
            })

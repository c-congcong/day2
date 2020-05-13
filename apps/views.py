from django.http import HttpResponse, JsonResponse
from django.utils.decorators import method_decorator
from django.views import View
from django.views.decorators.csrf import csrf_exempt, csrf_protect
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework.renderers import JSONRenderer, BrowsableAPIRenderer, TemplateHTMLRenderer
from rest_framework.parsers import JSONParser, FormParser, MultiPartParser

from apps.models import UserInfo, Students


# csrf_exempt: 可以免除某个方法的csrf认证
# csrf_protect：可以为某个视图单独添加csrf认证
@method_decorator(csrf_exempt, name="dispatch")
class UserView(View):
    parser_classes = [JSONParser]
    def get(self, request, *args, **kwargs):
        """提供查询单个  多个用户的API"""
        user_id = kwargs.get("pk")
        if user_id:  # 查询单个
            user_values = UserInfo.objects.filter(pk=user_id).values("username", "password", "gender").first()
            if user_values:
                return JsonResponse({
                    "status": 200,
                    "message": "获取用户成功",
                    "results": user_values
                })
        else:  # 如果用户id不存且发的是get请求  代表是获取全部用户信息
            user_list = UserInfo.objects.all().values("username", "password", "gender")
            if user_list:
                return JsonResponse({
                    "status": 201,
                    "message": "获取用户列表成功",
                    "results": list(user_list)
                })

        return JsonResponse({
            "status": 400,
            "message": "获取用户不存在",
        })


    def post(self, request, *args, **kwargs):
        """完成新增单个用户的操作"""
        print(request.POST)
        # 对post传递过来的参数进行校验
        try:
            user_obj = UserInfo.objects.create(**request.POST.dict())
            if user_obj:
                return JsonResponse({
                    "status": 200,
                    "message": "新增用户成功",
                    "results": {"username": user_obj.username, "gender": user_obj.gender}
                })
            else:
                return JsonResponse({
                    "status": 500,
                    "message": "新增用户失败",
                })
        except:
            return JsonResponse({
                "status": 501,
                "message": "参数有误",
            })

    def put(self, request, *args, **kwargs):
        print("PUT 修改")
        try:
            id = kwargs.get("pk")
            if id:
                user_obj = UserInfo.objects.filter(pk=id)[0]
                if user_obj:
                    #修改数据库数据
                    user_obj.username =   '获取前端数据'
                    return JsonResponse({
                        "status": 200,
                        "message": "修改用户成功",
                        "results": {"username": user_obj.username, "gender": user_obj.gender}
                    })
                else:
                    return JsonResponse({
                        "status": 500,
                        "message": "修改用户失败",
                    })
        except:
            return JsonResponse({
                "status": 501,
                "message": "参数有误",
            })



    def delete(self, request, *args, **kwargs):
        print("DELETE 删除")
        user_id = kwargs.get("pk")
        if user_id:  # 删除单个
            user_values = UserInfo.objects.filter(pk=user_id).delete()
            if user_values:
                return JsonResponse({
                    "status": 200,
                    "message": "删除用户成功",
                })
        else:  # 如果用户id不存且发的是delete请求  代表是删除全部用户信息
            user_list = UserInfo.objects.all().delete()
            if user_list:
                return JsonResponse({
                    "status": 201,
                    "message": "删除用户列表成功",
                })

        return JsonResponse({
            "status": 400,
            "message": "此用户不存在，无法删除",
        })


class StudentView(APIView):
    # renderer_classes = [BrowsableAPIRenderer]
    parser_classes = [JSONParser]

    def get(self, request, *args, **kwargs):
        """DRF获取get请求参数的方式"""
        print(request._request.GET)  # 原生django request对象
        print(request.GET)  # DRF request 对象
        print(request.query_params)  # DRF 扩展的get请求参数

        def get(self, request, *args, **kwargs):
            """提供查询单个  多个用户的API"""
            user_id = request.GET("pk")
            if user_id:  # 查询单个
                user_values = Students.objects.filter(pk=user_id).values("name", "age", "gender").first()
                if user_values:
                    return JsonResponse({
                        "status": 200,
                        "message": "获取用户成功",
                        "results": user_values
                    })
            else:  # 如果用户id不存且发的是get请求  代表是获取全部用户信息
                user_list = Students.objects.all().values("name", "age", "gender")
                if user_list:
                    return JsonResponse({
                        "status": 201,
                        "message": "获取用户列表成功",
                        "results": list(user_list)
                    })

            return JsonResponse({
                "status": 400,
                "message": "获取用户不存在",
            })

    def post(self, request, *args, **kwargs):
        """DRF 获取POST请求参数的方式"""
        # POST传递参数的形式 formdata urlencoding Json
        print(request._request.POST)  # 原生django request对象
        print(request.POST)  # DRF request 对象
        print(request.data)  # DRF 扩展post请求参数   兼容性最强
        try:
            user_obj = Students.objects.create(**request.POST.dict())
            if user_obj:
                return JsonResponse({
                    "status": 200,
                    "message": "新增用户成功",
                    "results": {"username": user_obj.username, "gender": user_obj.gender}
                })
            else:
                return JsonResponse({
                    "status": 500,
                    "message": "新增用户失败",
                })
        except:
            return JsonResponse({
                "status": 501,
                "message": "参数有误",
            })
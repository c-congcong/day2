from rest_framework.response import Response
from rest_framework.views import APIView

from app_work import serializers
from app2.models import Students1, Classes


class StudentsAPIVIew(APIView):

    def get(self, request, *args, **kwargs):

        stu_id = kwargs.get("pk")

        if stu_id:
            try:
                stu_obj = Students1.objects.get(pk=stu_id)
                stu_ser = serializers.StudentsModelSerializer(stu_obj).data
                return Response({
                    "status": 200,
                    "message": "查询学生成功",
                    "results": stu_ser
                })
            except:
                return Response({
                    "status": 200,
                    "message": "查询学生不存在",
                })
        else:
            stu_list = Students1.objects.filter()
            stu_data = serializers.StudentsModelSerializer(stu_list, many=True).data

            return Response({
                "status": 200,
                "message": "查询学生列表成功",
                "results": stu_data
            })

    def post(self, request, *args, **kwargs):

        request_data = request.data

        if isinstance(request_data, dict):
            book_ser = serializers.StudentsModelSerializer(data=request_data)
            many = False
        elif isinstance(request_data, list):
            book_ser = serializers.StudentsModelSerializer(data=request_data, many=True)
            many = True
        else:
            return Response({
                "status": 200,
                "message": "数据格式有误",
            })

        book_ser = serializers.StudentsModelSerializer(data=request_data, many=many)
        book_ser.is_valid(raise_exception=True)
        book_obj = book_ser.save()

        return Response({
            "status": 200,
            "message": "success",
            "results": serializers.StudentsModelSerializer(book_obj, many=many).data
        })

    def delete(self, request, *args, **kwargs):
        st_id = kwargs.get("pk")
        if st_id:
            ids = [st_id]
        else:
            ids = request.data.get("ids")
        res = Students1.objects.filter(pk__in=ids).delete()
        if res:
            return Response({
                "status": 200,
                "message": "删除成功",
            })

        return Response({
            "status": 500,
            "message": "删除失败或者已删除",
        })

    def put(self, request, *args, **kwargs):
        """
        单整体改：修改一个对象的全部字段
        :param request:   获取修改对象的值
        :param kwargs:  需要知道我要修改哪个对象   获取修改对象的id
        :return:    更新后的对象
        """
        request_data = request.data
        st_id = kwargs.get("pk")

        try:
            st_obj = Students1.objects.get(pk=st_id)
        except:
            return Response({
                "status": 500,
                "message": "学生不存在!",
            })

        st_ser = serializers.StudentsModelSerializer(data=request_data, instance=st_obj, partial=False)
        st_ser.is_valid(raise_exception=True)
        st_ser.save()

        return Response({
            "status": 200,
            "message": "更新成功",
            "results": serializers.StudentsModelSerializer(st_obj).data
        })

    #修改单个
    # def patch(self, request, *args, **kwargs):
    #     request_data = request.data
    #     st_id = kwargs.get("pk")
    #     try:
    #         st_obj = Students1.objects.get(pk=st_id)
    #     except:
    #         return Response({
    #             "status": 500,
    #             "message": "学生不存在",
    #         })
    #     st_ser = serializers.StudentsModelSerializer(data=request_data, instance=st_obj,
    #                                                  partial=True)  # partial=True  指定序列化器为更新部分字段  有哪个字段的值就修改哪个字段  没有不修改
    #     st_ser.is_valid(raise_exception=True)
    #     st_ser.save()
    #
    #     return Response({
    #         "status": 200,
    #         "message": "更新成功",
    #         "results": serializers.StudentsModelSerializer(st_obj).data
    #     })

    # 修改多个
    def patch(self,request,*args,**kwargs):
        request_data = request.data
        book_id = kwargs.get('id')
        #i的存在返回得是字典，单改
        if book_id and isinstance(request_data,dict):
            # 单改转换成 群改一个
            book_ids = [book_id, ]
            request_data = [request_data, ]
        # id不存在返回列表 多改
        elif not book_id and isinstance(request_data,list):
            # 群改
            book_ids = []
            # 从获取的数据中将pk拿出来放进book_ids
            for dic in request_data:
                pk = dic.pop("pk", None)
                if pk:
                    book_ids.append(pk)
                else:
                    return Response({
                        "status": 500,
                        "message": "ID不存在"
                    })
        else:
            return Response({
                "status":500,
                "message":"数据格式不对"
            })

            # 对book_ids与request_data数据进行筛选
            # 对不存在的对象pk进行移除 request_data 也移除  如果存在  查询出对应的对象
            book_list = []
            # TODO 不要循环中对列表的长度做操作
            new_data = []
            #  [ {pk:1, publish: 4}, {pk:2, price: 88.8}, {pk:3, boo_name: 123} ]
            for index, pk in enumerate(book_ids):
                try:
                    book_obj = Book.objects.get(pk=pk)
                    book_list.append(book_obj)
                    # 对应的索引的数据保存
                    new_data.append(request_data[index])
                    # print(request_data[index])
                except:
                    # 不存在则移除  错误示范
                    # index = book_ids.index(pk)
                    # request_data.pop(index)
                    continue

        st_ser = serializers.StudentsModelSerializer(data=request_data, instance=st_obj, partial=False)
        st_ser.is_valid(raise_exception=True)
        st_ser.save()

        return Response({
            "status": 200,
            "message": "更新成功",
            "results": serializers.BookModelSerializerV2(book_list, many=True).data
        })
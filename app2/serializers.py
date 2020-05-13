from rest_framework import serializers, exceptions

from app2.models import Employee
from day2 import settings


class EmployeeModelSerializer(serializers.Serializer):
    username = serializers.CharField()
    # password = serializers.CharField()
    # gender = serializers.IntegerField()
    # pic = serializers.ImageField()

    # 自定义一个序列化字段
    aaa = serializers.SerializerMethodField()

    # 返回值自定义
    def get_aaa(self, obj):
        return "example"

    # 自定义返回性别
    gender = serializers.SerializerMethodField()

    def get_gender(self, obj):
        # 如果获取choices类型解释型的值，可以通过 get_字段名_display()访问
        return obj.get_gender_display()

    # 自定义图片全路径
    pic = serializers.SerializerMethodField()

    def get_pic(self, obj):
        return "%s%s%s" % ("http://127.0.0.1:8000", settings.MEDIA_URL, str(obj.pic))


class EmployeeDeserializer(serializers.Serializer):
    # 反序列化 前端到数据库
    # 翻序列化规则和错误信息
    username = serializers.CharField(
        max_length=12,
        min_length=4,
        error_messages={
            "max_length": "名字太长了！",
            "min_length": "名字太短了！"

        }
    )
    # mima
    password = serializers.CharField()
    # 手机,不为空
    phone = serializers.CharField(required=False)
    # 重复密码
    re_pwd = serializers.CharField()

    # 局部验证钩子函数
    def validate_username(self, value):
        if "1" in value:
            raise exceptions.ValidationError("用户名异常了")
        return value

    # 全局验证钩子,所以数据都会验证
    def validate(self, attrs):
        password = attrs.get("password")
        re_pwd = attrs.pop("re_pwd")
        if password != re_pwd:
            raise exceptions.ValidationError("两次密码不一致！")
        return attrs

    def create(self, validated_data):
        print(validated_data)
        return Employee.objects.create(**validated_data)

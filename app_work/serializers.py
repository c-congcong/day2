from rest_framework import serializers

from app2.models import Students1,Book,Press




class StudentsModelSerializer(serializers.ModelSerializer):
    class Meta:
        model = Students1
        fields = ("st_name", "age", "st_id", "gender","classes")
        extra_kwargs = {
            "st_name": {
                "required": True,
                "min_length":2,
                "error_messages": {
                    "required": "学生名字是必填的",
                    "min_length": "学生名长度太短"
                }
            },
            "st_id": {
                "required": True,
                "min_length": 12,
                "error_messages": {
                    "required": "学号是必填的",
                    "min_length": "学号长度必须为12位"
                }
            },
        }

    def validate_age(self, value):
        if  value >99:
            raise serializers.ValidationError("神仙？")
        else:
            return value

    def validate(self, attrs):
        stid = attrs.get("st_id")
        print(stid)
        st_obj = Students1.objects.filter(st_id=stid)
        if st_obj:
            raise serializers.ValidationError("学号重复")

        return attrs


class BookListSerializer(serializers.ListSerializer):

    def update(self, instance, validated_data):
        print(instance)     # 是需要更新的书籍对象
        print(validated_data)   # 是需要更新的数据
        # print(self.child)
        # return [
        #     self.child.update(instance, validated_data) for attrs in validated_data
        # ]
        # DRF更新一个对象  能不将更新多个转变成一次更新一个  for
        for index, obj in enumerate(instance):
            self.child.update(obj, validated_data[index])

        return instance


class BookModelSerializerV2(serializers.ModelSerializer):
    class Meta:
        model = Book
        # filed 应该填写哪些字段  应该填写序列化与反序列所有字段的并集
        fields = ("book_name", "price", "pic", "authors", "publish", "author_list", "publish_name",)

        # 批量更新时需要自定ListSerializer重新改写update方法
        list_serializer_class = BookListSerializer

        # 为序列化与反序列化的字段提供校验规则
        # 可以通过write_only属性指定哪个字段只参与反序列化  read_only指定只参与序列化
        extra_kwargs = {
            "book_name": {
                "required": True,  # 设置为必填字段
                "min_length": 5,  # 设置最小长度
                "error_messages": {
                    "required": "图书名是必填的",
                    "min_length": "图书名长度不够"
                }
            },
            "authors": {
                "write_only": True  # 只参与反序列化
            },
            "publish": {
                "write_only": True  # 只参与反序列化
            },
            "author_list": {
                "read_only": True  # 序列化
            },
            "publish_name": {
                "read_only": True  # 序列化
            },
            "pic": {
                "read_only": True  # 序列化
            },
        }

    # 自己添加额外的校验规则  局部钩子
    def validate_book_name(self, value):
        # 检查图书名是否存在
        # if "D" in value:
        #     raise serializers.ValidationError("D图书已存在")
        # else:
        #     return value
        # 可以接收到传递过来的request对象
        print(self.context.get("request").method)
        return value

    def validate(self, attrs):
        publish = attrs.get("publish")
        book_name = attrs.get("book_name")
        # 一个出版社只能不能发布重复的书籍名
        book_obj = Book.objects.filter(book_name=book_name, publish=publish)
        if book_obj:
            raise serializers.ValidationError("该出版社已经发布过该图书")

        return attrs
from rest_framework import serializers

from app2.models import Students1,Classes




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

# TUẦN TỰ CÁC BƯỚC TRIỂN KHAI DỰ ÁN DJANGO
1. Tạo readme.md
2. Tạo môi trường ảo, để quản lý phiên bản python, quản lý tên package, phiên bản package sử dụng trong dự án với mục đích là để triển khai source trên các máy khác nhau mang tính đồng bộ
```commandLine
python -m venv venv
```
3. Các thành phần trong folder venv
- bin:
    + activate
4. Kích hoạt môi trường ảo
```commandLine
source ./venv/bin/activate
```
5. Tạo file requirements.txt
    - Django==4.2.4
    - djangorestframework==3.14.0
    - djangorestframework-simplejwt==5.2.2
6. Cài đặt các package
```commandLine
pip install -r requirements.txt
```
7. Tạo file .ignore để loại trừ các folder không muốn up lên gitlab, github (vd venv/)
8. Gán môi trường ảo cho dự án (interpreter)
- Ở góc màn hình select interpreter, chọn ./venv/scripts/activate
9. Tạo project
```commandLine
django-admin startproject democms .
```
10. Tạo một app mới
```commandLine
python manage.py startapp account
```
11. Trong file setttings của project (democms), khai báo thêm cái app account
12. Tạo file urls.py trong app mới (account), sử dụng gói django.urls với path và include để khai báo endpoint
13. Trong file urls.py của project (democms), khai báo nối thêm các path của app mới vào path của project
14. Tạo view để gán cho endpoint khai báo trong app mới
15. Tiến hành các lệnh tạo database cần thiết cho dự án 
```commandLine
python manage.py makemigrations
python manage.py migrate
```
16. Run server
```commandLine
python manage.py runserver 167.172.88.152:8000
```
15. Tạo file .http và cài extension Rest APi
16. Nội dung này cần có link đính kèm
- [Link tài liệu](https://pypi.org/project/pyqt5-tile-layout/)
17. Đây là điển hình cho một file readme.md tiêu chuẩn
- [Link tài liệu](https://raw.githubusercontent.com/donnemartin/system-design-primer/master/README.md)

18. tạo folder views tạo file view_register.py
```python
from rest_framework.permissions import AllowAny
from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework.status import *

from ..serializers import RegisterSerializer
from ..libs.device import store_device
from ..models import UserModel

class RegisterView(APIView):
    # permission_classes = [AllowAny, ]

    def post(self, request):

        serializer = RegisterSerializer(data=request.data)
        if not serializer.is_valid():
            return Response({
                "message": "invalid data",
                "error_fields": serializer.errors,
            }, status=HTTP_400_BAD_REQUEST)
        
        serializer.save()

        return Response({
            "message": "Registered successfully",
            "data": {
                "user": serializer.data,
            }
        })

```
19. Tạo file __init__ trong folder views
```python
from .view_register.py import RegisterView
```

20. Xây dựng xong các yếu tố cần thiết cho RegisterView
- Tạo RegisterView, Tạo các models, tạo các serializer liên quan

21. Makemigations cho các model mới
```commandLine
python manage.py makemigrations
```

21. Makemigations cho các model mới
```commandLine
python manage.py migrate
```

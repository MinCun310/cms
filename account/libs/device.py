from ..serializers import DeviceSerializer

def store_device(request, user=None):
    if user is None:
        user = request.user
        
    data= {
        "useragent": request.META['HTTP_USER_AGENT'],
        "ip": request.META['REMOTE_ADDR'],
        "user": user.id,
        "session_id": request.session.session_key,
        "extra_info": str(request.META),
    }
    
    serializer = DeviceSerializer(data=data)
    serializer.is_valid(raise_exception=True)
    serializer.save()
    
    return serializer.data

def get_device(request, user=None):
    if user is None:
        user = request.user
        
    data = {
        "useragent": request.META['HTTP_USER_AGENT'],
        "ip": request.META['REMOTE_ADDR'],
        "user": user.id,
        "session_id": request.session.session_key,
        "extra_info": str(request.META),
    }
    
    serializer = DeviceSerializer(data=data)
    serializer.is_valid(raise_exception=True)
    serializer.save()
    
    return serializer.data
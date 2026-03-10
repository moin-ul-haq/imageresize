from rest_framework.views import APIView
from rest_framework.response import Response
from .services import save_uploaded_image
from .tasks import perform_operation
from .serializers import ImageSerializer,TaskStatusSerializer
from celery.result import AsyncResult


class UploadImageView(APIView):
    def post(self,request):
        serializer=ImageSerializer(data=request.data)
        if serializer.is_valid():
            img=serializer.validated_data['image']
            path=save_uploaded_image(img)
            task=perform_operation.delay(path)
            return Response({'task id':f'{task.id}'})
        return Response({'message':'Not Done'})


class TaskStatusView(APIView):
    def get(self,request,task_id):
        try:
            task=AsyncResult(task_id)
            return Response({'status':f'{task.status}'})
        except:
            return Response({'Error: ':f'Task does not exists'})
        

class TaskResultView(APIView):
    def get(self,request,task_id):
        try:
            task=AsyncResult(task_id)
            if task.status == 'SUCCESS':
                return Response({'status':f'{task.status}',
                                 'RESULT: ':F'{task.result}'})
            else:
                return Response({'error':'Task Not completed Yet...'})
        except:
                return Response({'error':'Task Not Found...'})


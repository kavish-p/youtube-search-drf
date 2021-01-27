from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework import status
from json.decoder import JSONDecodeError
from api.engine import search


class Test(APIView):
    def get(self, request):
        return Response({'detail': 'hello world'}, status=status.HTTP_200_OK)

    def post(self, request):
        results = {'message':'An internal error occurred.'}
        try:
            results = search('https://www.youtube.com/watch?v=pMsvr55cTZ0', 'hola', 60, 0, 120)
        except JSONDecodeError as e:
            print('JSONDecodeError. Trying again . . .')
            try:
                results = search('https://www.youtube.com/watch?v=pMsvr55cTZ0', 'hola', 60, 0, 120)
            except JSONDecodeError as e:
                print(e)
                return Response({'message':'An internal error occurred.'}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)
            except Exception as e:
                print(e)
        except Exception as e:
            print(e)

        data=request.data
        print(data)
        return Response(results, status=status.HTTP_200_OK)
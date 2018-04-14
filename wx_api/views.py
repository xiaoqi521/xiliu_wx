from rest_framework.views import APIView
from constants import error_constants
from libs.api_tools.api_tools import generate_error_response
import traceback
import logging


# Create your views here.
class ApplyForViews(APIView):
    def post(self, request):
        """
            请假申请
            ---
            parameters:
                - name: token
                  description: 当前用户token
                  required: true
                  type: string
                  paramType: header

                - name: user
                  description: 请假人名称
                  required: true
                  type: string
                  paramType: query

                - name: day
                  description: 请假天数
                  required: true
                  type: integer
                  paramType: query

                - name: reason
                  description: 请假理由
                  required: true
                  type: integer
                  paramType: query

                - name: recipient
                  description: 接收人
                  required: true
                  type: integer
                  paramType: query

        """

        response_data = {'retCode': error_constants.ERR_STATUS_SUCCESS[0],
                         'retMsg': error_constants.ERR_STATUS_SUCCESS[1]}


        try:
            # token = request.
            user = request.POST.get('user', 0)
            day = request.POST.get('day', 0)
            reason = request.POST.get('reason', 0)
            recipient = request.POST.get('recipient', 0)
        except Exception:
            logging.exception(traceback.format_exc())
            return generate_error_response(error_constants.ERR_INVALID_PARAMETER, status.HTTP_400_BAD_REQUEST)

        if user == "seven":
            return Response(response_data, status=status.HTTP_200_OK)
        else:
            logging.error("response == None")
            return generate_error_response(error_constants.ERR_STATUS_FAIL, status.HTTP_400_BAD_REQUEST)

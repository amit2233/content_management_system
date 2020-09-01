"""request response generic parser"""
import json
import logging

from django.http import HttpResponse
from django.utils.deprecation import MiddlewareMixin

LOGGER = logging.getLogger('request_response')

DEFAULT_RESP_MSG = ""
DEFAULT_RESP_DATA = {}
DEFAULT_RESP_STATUS = False
DEFAULT_RESP_ERROR_MSG_CODE = ""


class RequestResponseMiddleware(MiddlewareMixin):
    """Middleware for generate generic response"""

    @classmethod
    def process_response(cls, request, response):
        """Generate response"""

        if '/ajax/' in request.get_full_path().lower():
            return response

        if response.get('Content-Type') != 'application/json':
            # if response.status_code == 500:

                # if not True:
                #
                #     LOGGER.error('---Server Error Log Starts---')
                #
                #
                #     LOGGER.error(response.content.decode('utf-8'))
                #     LOGGER.error('---Server Error Log Ends---')
                #
                #     return HttpResponse(content=json.dumps({
                #         'data': '',
                #         'error_code': 'CRITICAL',
                #         'msg': 'Internal Server Error',
                #         'success': False,
                #     }),
                #         status=response.status_code,
                #         content_type="application/json"
                #     )
            return response

        _response_content = response.content.decode('utf-8')
        _response_json_obj = json.loads(_response_content)


        data = _response_json_obj.get('data')
        success = _response_json_obj.get('success')
        msg = _response_json_obj.get('msg')
        error_code = _response_json_obj.get('error_code')

        if data in [None]:
            data = _response_json_obj.get('detail')
            if data in [None]:
                data = DEFAULT_RESP_DATA

        if success in ['', None]:
            success = DEFAULT_RESP_STATUS

        if not msg:
            msg = DEFAULT_RESP_MSG

        if not error_code:
            error_code = DEFAULT_RESP_ERROR_MSG_CODE

        return_dict = {'msg': msg, 'data': data, 'success': success, 'error_code': error_code}

        return HttpResponse(content=json.dumps(return_dict),
                            status=response.status_code,
                            content_type="application/json"
                            )

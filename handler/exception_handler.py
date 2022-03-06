import logging
import traceback
from werkzeug.exceptions import InternalServerError, BadRequest
from dto.response import BaseResponse
from flask import jsonify


def bad_request_exception_handler(ex: BadRequest):
    logging.info(ex.description)
    response = BaseResponse(code=400, des=ex.description, res="no")
    return jsonify(response.__dict__), 400


def internal_server_error_handler(error: InternalServerError):
    logging.error(
        traceback.format_exc()
    )  # internal error is important => print all trace
    response = BaseResponse(
        code=500,  des="Internal Server Error", res="no"
    )
    return jsonify(response.__dict__), 500

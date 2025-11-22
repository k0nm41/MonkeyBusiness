import config

from fastapi import APIRouter, Request, Response

from core_common import core_process_request, core_prepare_response, E

router = APIRouter(tags=["local", "local2"])
router.model_whitelist = ["LDJ"]


@router.post("/{prefix}/{gameinfo}/{IIDXver}streaming/common")
async def iidx_streaming_common(IIDXver: str, request: Request):
    request_info = await core_process_request(request)

    response = E.response(E(f"{IIDXver}streaming",))

    response_body, response_headers = await core_prepare_response(request, response)
    return Response(content=response_body, headers=response_headers)


@router.post("/{prefix}/{gameinfo}/{IIDXver}streaming/getcm")
async def iidx_streaming_getcm(IIDXver: str, request: Request):
    request_info = await core_process_request(request)

    response = E.response(E(f"{IIDXver}streaming",))

    response_body, response_headers = await core_prepare_response(request, response)
    return Response(content=response_body, headers=response_headers)

from fastapi import APIRouter, Request, File, UploadFile
from fastapi.templating import Jinja2Templates
from starlette.responses import JSONResponse
from ..lib.blo.compare_user_image_blo import compare_user_image

from app.core.lib.blo.authentication_flow import decode_token, encode_payload, get_validation_response, create_auth_session, get_session

router = APIRouter()
templates = Jinja2Templates(directory='app/core/templates')


@router.get('/authentication-check')
async def authentication_check(request: Request, token: str = '', returnUrl: str = ''):
    validation_response = await get_validation_response(token, returnUrl)
    if validation_response:
        return validation_response

    decoded = decode_token(token)
    session = await create_auth_session(returnUrl, decoded.get('user_id'))
    print('banan session')
    print(session)
    return templates.TemplateResponse(
        name="authentication-flow.html",
        context={
            "request": request,
            "session_id": session.get('session_id'),
            "return_url": returnUrl
        }
    )


@router.post('/authentication-check/{session_id}')
async def check_authentication_validity(session_id: str, image: UploadFile = File(...)):
    session = await get_session(session_id)
    if not session:
        return JSONResponse(
            status_code=404,
            content='Session with given id not found'
        )

    comparison_result = await compare_user_image(session.get('user_id'), image)
    result_payload = {
        'session_id': session.get('session_id'),
        'auth_successful': comparison_result.get('is_likely_match'),
        'match_count': comparison_result.get('match_count'),
        'total_comparisons': comparison_result.get('total_comparisons'),
        'average_distance': comparison_result.get('average_euclidean_distance')
    }

    encoded_payload = encode_payload(result_payload)
    return encoded_payload

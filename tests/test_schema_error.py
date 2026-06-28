from app.schemas.error_schema import ErrorResponse


def test_error_response_schema_accepts_optional_detail():
    data = {'error': 'something went wrong', 'status_code': 400, 'detail': 'more info'}
    response = ErrorResponse(**data)

    assert response.error == 'something went wrong'
    assert response.status_code == 400
    assert response.detail == 'more info'


def test_error_response_schema_works_without_detail():
    data = {'error': 'something went wrong', 'status_code': 500}
    response = ErrorResponse(**data)

    assert response.detail is None

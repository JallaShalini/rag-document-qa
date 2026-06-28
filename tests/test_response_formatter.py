from app.utils.response_formatter import (
    format_error_response,
    format_query_response,
    format_upload_response,
)


def test_format_query_response_returns_expected_shape():
    response = format_query_response('answer', ['source1', 'source2'])

    assert response == {
        'answer': 'answer',
        'sources': ['source1', 'source2'],
    }


def test_format_upload_response_returns_message():
    response = format_upload_response('ok')

    assert response == {'message': 'ok'}


def test_format_error_response_includes_detail_when_provided():
    response = format_error_response('error', 500, detail='details')

    assert response == {
        'error': 'error',
        'status_code': 500,
        'detail': 'details',
    }


def test_format_error_response_omits_detail_when_none():
    response = format_error_response('error', 400)

    assert response == {
        'error': 'error',
        'status_code': 400,
    }

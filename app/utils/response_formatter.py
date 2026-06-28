from typing import List, Dict


def format_query_response(answer: str, sources: List[str]) -> Dict[str, object]:
    return {
        'answer': answer,
        'sources': sources,
    }


def format_upload_response(message: str) -> Dict[str, str]:
    return {'message': message}


def format_error_response(error: str, status_code: int, detail: str | None = None) -> Dict[str, object]:
    response = {
        'error': error,
        'status_code': status_code,
    }
    if detail:
        response['detail'] = detail
    return response

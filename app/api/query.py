from fastapi import APIRouter, HTTPException, status

from app.schemas.query_schema import QueryRequest
from app.schemas.response_schema import QueryResponse
from app.services.retriever import retrieve_relevant_chunks
from app.services.prompt_builder import build_prompt
from app.services.llm_service import call_llm, LLMServiceError
from app.services.vector_store import VectorStoreError
from app.utils.logger import log_query, log_error

router = APIRouter()


@router.post('/query', response_model=QueryResponse)
async def query_document(payload: QueryRequest) -> QueryResponse:
    question = payload.question.strip()
    if not question:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail='Question must not be empty.',
        )

    log_query(question)

    try:
        context_chunks = retrieve_relevant_chunks(question)
        if not context_chunks:
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail='No indexed documents available for this query.',
            )

        prompt = build_prompt(context_chunks, question)
        answer = call_llm(prompt)
        return QueryResponse(answer=answer, sources=context_chunks)
    except LLMServiceError as exc:
        log_error(exc, 'query_document')
        raise HTTPException(
            status_code=status.HTTP_502_BAD_GATEWAY,
            detail=str(exc),
        )
    except VectorStoreError as exc:
        log_error(exc, 'query_document')
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail='Failed to retrieve documents from vector store.',
        )
    except HTTPException:
        raise
    except Exception as exc:
        log_error(exc, 'query_document')
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail='Failed to process the query.',
        )

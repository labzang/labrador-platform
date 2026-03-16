"""
멤버 관련 라우터
"""
from fastapi import APIRouter
from common.utils import create_response

router = APIRouter(prefix="/member", tags=["member"])


@router.get("/")
async def member_root():
    """멤버 서비스 루트"""
    return create_response(
        data={"service": "memberservice", "status": "running"},
        message="Member Service is running"
    )


@router.get("/health")
async def health_check():
    """헬스 체크"""
    return create_response(
        data={"status": "healthy", "service": "memberservice"},
        message="Service is healthy"
    )

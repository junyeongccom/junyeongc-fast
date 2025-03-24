from pydantic import BaseModel, EmailStr, Field
from typing import Optional, Dict, Any

class LoginRequest(BaseModel):
    """로그인 요청 모델"""
    user_id: str = Field(..., min_length=4, max_length=20, description="사용자 ID")
    password: str = Field(..., min_length=8, description="비밀번호")

class LoginResponse(BaseModel):
    """로그인 응답 모델"""
    status: str
    message: str
    access_token: str
    user: Dict[str, Any]

class RefreshTokenRequest(BaseModel):
    """토큰 갱신 요청 모델"""
    refresh_token: str

class LogoutRequest(BaseModel):
    """로그아웃 요청 모델"""
    access_token: str

class TokenResponse(BaseModel):
    """토큰 응답 모델"""
    status: str
    message: str
    access_token: str 
from ninja import Schema


class DebugLoginRequest(Schema):
    kakao_user_id: str

    class Config:
        schema_extra = {"example": {"kakao_user_id": "11223"}}

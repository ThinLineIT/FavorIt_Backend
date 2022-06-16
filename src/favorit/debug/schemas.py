from ninja import Schema


class DebugLoginRequest(Schema):
    user_id: str

    class Config:
        schema_extra = {"example": {"user_id": "11223"}}

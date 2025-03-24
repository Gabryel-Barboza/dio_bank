from pydantic import BaseModel


class UserUpdateModel(BaseModel):
    nome: str | None
    endereco: str | None
    cpf: str | None
    data_nascimento: str | None

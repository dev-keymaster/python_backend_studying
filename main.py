from pydantic import BaseModel, Field, ConfigDict
from pydantic.alias_generators import to_camel


class CompanyInfo(BaseModel):
    model_config = ConfigDict(
        alias_generator=to_camel,
        populate_by_name=True,
    )

    company_name: str
    total_employees: int
    is_active: bool

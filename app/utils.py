from pydantic import BaseModel, ValidationError
from typing import Type, Callable, Awaitable
from fastapi import Request, HTTPException

def form_data_as(model: Type[BaseModel]) -> Callable[[Request], Awaitable[BaseModel]]:
    """
    Dependency factory that converts form data to a Pydantic model.
    """
    async def dependency(request: Request) -> BaseModel:
        try:
            # Get the form data as a multi-dict and convert it to a regular dict.
            form_data = await request.form()
            data_dict = dict(form_data)
            if "grant_type" in data_dict:
                del data_dict["grant_type"]
            # Create the model instance, which validates the data.
            return model(**data_dict)
        except ValidationError as e:
            # If validation fails, raise a 422 error with details.
            raise HTTPException(status_code=422, detail=e.errors())
    return dependency


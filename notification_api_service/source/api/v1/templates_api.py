from http import HTTPStatus
from typing import Any

from fastapi import APIRouter, Depends
from fastapi.responses import JSONResponse

from database.managers import get_db_manager
from models import TemplateModel

router = APIRouter()


@router.post('/add_template', response_model=Any, summary='Add template to database')
async def add_template(template: TemplateModel, db_manager=Depends(get_db_manager)) -> JSONResponse:
    """
        ## Add template to database:
        - _template_ - Модель шаблона
    """
    if all(template.dict().values()):
        if await db_manager.async_add_template(template):
            return JSONResponse(
                status_code=HTTPStatus.OK,
                content=f'Template {template.name} added successfully'
            )

        return JSONResponse(
            status_code=HTTPStatus.NOT_ACCEPTABLE,
            content=f'Template {template.name} not added'
        )

    return JSONResponse(
        status_code=HTTPStatus.BAD_REQUEST,
        content=f'Template {template.name} not added'
    )


@router.get('/get_template', response_model=TemplateModel, summary='Get template from database')
async def add_template(template_id, db_manager=Depends(get_db_manager)) -> TemplateModel or JSONResponse:
    """
        ## Get template from database:
        - _template_id_ - Идентификатор шаблона
    """
    if result := await db_manager.async_get_template(template_id=template_id):
        return TemplateModel(**result.__dict__)

    return JSONResponse(
        status_code=HTTPStatus.NOT_FOUND,
        content=f'Template {template_id} not found'
    )


@router.put('/upd_template', response_model=Any, summary='Update template in database')
async def add_template(template: TemplateModel, db_manager=Depends(get_db_manager)) -> JSONResponse:
    """
        ## Update template in database:
        - _template_ - Модель шаблона
    """
    if await db_manager.async_update_template(template):
        return JSONResponse(
            status_code=HTTPStatus.OK,
            content=f'Template {template.name} updated successfully'
        )

    return JSONResponse(
        status_code=HTTPStatus.NOT_ACCEPTABLE,
        content=f'Template {template.name} not updated'
    )


@router.delete('/del_template', response_model=Any, summary='Delete template from database')
async def add_template(template: TemplateModel, db_manager=Depends(get_db_manager)) -> JSONResponse:
    """
        ## Delete template from database:
        - _template_ - Модель шаблона
    """
    if await db_manager.async_delete_template(template):
        return JSONResponse(
            status_code=HTTPStatus.OK,
            content=f'Template {template.name} deleted successfully'
        )

    return JSONResponse(
        status_code=HTTPStatus.NOT_ACCEPTABLE,
        content=f'Template {template.name} not deleted'
    )

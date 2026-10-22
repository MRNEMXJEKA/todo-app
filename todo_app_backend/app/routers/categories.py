from fastapi import APIRouter, Depends, HTTPException, status

from app.dependencies import get_category_service
from app.schemas import CategoryCreate, CategoryRead, CategoryUpdate
from app.service import CategoryNotFoundError, CategoryService

router = APIRouter(prefix="/categories", tags=["categories"])


@router.get("")
def read_categories(
    service: CategoryService = Depends(get_category_service),
) -> list[CategoryRead]:
    return service.list_categories()


@router.post("", status_code=status.HTTP_201_CREATED)
def create_category(
    payload: CategoryCreate, service: CategoryService = Depends(get_category_service)
) -> CategoryRead:
    return service.create_category(payload)


@router.patch("/{category_id}")
def update_category(
    category_id: str,
    payload: CategoryUpdate,
    service: CategoryService = Depends(get_category_service),
) -> CategoryRead:
    try:
        return service.update_category(category_id, payload)
    except CategoryNotFoundError:
        raise HTTPException(status_code=404, detail="Category not found")


@router.delete("/{category_id}", status_code=status.HTTP_204_NO_CONTENT)
def delete_category(
    category_id: str, service: CategoryService = Depends(get_category_service)
) -> None:
    try:
        service.delete_category(category_id)
    except CategoryNotFoundError:
        raise HTTPException(status_code=404, detail="Category not found")

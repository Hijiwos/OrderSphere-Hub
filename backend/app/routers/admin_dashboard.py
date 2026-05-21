from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from app import models, schemas
from app.deps import get_db, get_admin_user

router = APIRouter(prefix="/admin/dashboard", tags=["admin-dashboard"])


@router.get("/", response_model=list[schemas.MenuItem])
def get_all_menu(db: Session = Depends(get_db), admin=Depends(get_admin_user)):
    return db.query(models.MenuItem).all()


@router.post("/", response_model=schemas.MenuItem)
def create_menu(item: schemas.MenuItemBase, db: Session = Depends(get_db), admin=Depends(get_admin_user)):
    new_item = models.MenuItem(**item.dict())
    db.add(new_item)
    db.commit()
    db.refresh(new_item)
    return new_item


@router.put("/{item_id}", response_model=schemas.MenuItem)
def update_menu(item_id: int, item: schemas.MenuItemBase, db: Session = Depends(get_db), admin=Depends(get_admin_user)):
    db_item = db.query(models.MenuItem).filter(models.MenuItem.id == item_id).first()
    if not db_item:
        raise HTTPException(status_code=404, detail="菜单不存在")

    for k, v in item.dict().items():
        setattr(db_item, k, v)

    db.commit()
    db.refresh(db_item)
    return db_item


@router.delete("/{item_id}")
def delete_menu(item_id: int, db: Session = Depends(get_db), admin=Depends(get_admin_user)):
    db_item = db.query(models.MenuItem).filter(models.MenuItem.id == item_id).first()
    if not db_item:
        raise HTTPException(status_code=404, detail="菜单不存在")

    db.delete(db_item)
    db.commit()
    return {"msg": "删除成功"}

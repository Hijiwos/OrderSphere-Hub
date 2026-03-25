from sqlalchemy.orm import Session
from app import models, schemas


def get_menu_items(db: Session):
    return db.query(models.MenuItem).all()


def get_menu_item(db: Session, item_id: int):
    return db.query(models.MenuItem).filter(models.MenuItem.id == item_id).first()


def create_order(db: Session, order_in: schemas.OrderCreate):
    order = models.Order(customer_name=order_in.customer_name, status="pending")
    db.add(order)
    db.flush()  # 先拿到 order.id

    total_price = 0.0
    for item in order_in.items:
        menu_item = db.query(models.MenuItem).filter(models.MenuItem.id == item.menu_item_id).first()
        if not menu_item:
            continue
        order_item = models.OrderItem(
            order_id=order.id,
            menu_item_id=menu_item.id,
            quantity=item.quantity,
        )
        db.add(order_item)
        total_price += menu_item.price * item.quantity

    order.total_price = total_price
    db.commit()
    db.refresh(order)
    return order


def get_order(db: Session, order_id: int):
    return db.query(models.Order).filter(models.Order.id == order_id).first()


def list_orders(db: Session):
    return db.query(models.Order).order_by(models.Order.id.desc()).all()

from fastapi import APIRouter

products_router = APIRouter(tags=["Products"])

@products_router.get("")
def get_all_products():
    return {"message":"products fetched successfully",
            "status_code":200,
            "success":True,
            "data":[]}


@products_router.get("/{id}")
def get_product_by_id(id:int):
    return {"message":"product fetched successfully",
            "status_code":200,
            "success":True,
            "data":[]}


@products_router.post("")
def create_product():
    return {"message":"product added successfully",
            "status_code":200,
            "success":True,
            "data":[]}


@products_router.put("/{id}")
def update_product(id:int):
    return {"message":"product updated successfully",
            "status_code":200,
            "success":True,
            "data":[]}


@products_router.delete("/{id}")
def delete_product(id:int):
    return {"message":"product deleted successfully",
            "status_code":200,
            "success":True,
            "data":[]}
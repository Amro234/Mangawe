from fastapi import APIRouter , HTTPException
from backend.app.models.products import get_products, getProductById
from backend.app.schemas.products import Products_Response


router = APIRouter(
    prefix="/api/products",
    tags =["Products"]
)

# * search on / get one product at a time with its id 
@router.get("/", response_model=list[Products_Response])
def listProducts(genre: str = None, search: str = None):
    products = get_products(genre=genre, search=search)
    return products

# ? get all products 
@router.get("/{product_id}", response_model=Products_Response)
def get_product(product_id: int):
    product = getProductById(product_id)
    if product is None:
        raise HTTPException(status_code = 404, details="Product is not found")
    return product
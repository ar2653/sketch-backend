from fastapi import APIRouter, HTTPException
# from app.db import sketches_table
from botocore.exceptions import ClientError
from app.models.sketch import Sketch

router = APIRouter()

@router.post("/")
async def create_sketch(sketch: Sketch):
    try:
        # sketches_table.put_item(Item=sketch.model_dump())
        return {"message": "Sketch created successfully"}
    except ClientError as e:
        print(f"Couldn't create sketch: {e}")
        raise HTTPException(status_code=500, detail="Failed to create sketch in DynamoDB")

@router.get("/")
async def read_sketches():
    try:
        # response = sketches_table.scan()
        items = response.get('Items')
        return items
    except ClientError as e:
        print(f"Couldn't get sketches: {e}")
        raise HTTPException(status_code=500, detail="Failed to retrieve sketches from DynamoDB")

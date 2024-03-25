from fastapi import FastAPI, HTTPException, status, Query
from fastapi.middleware.cors import CORSMiddleware
from turfpy.random import random_points
from typing import Annotated


app = FastAPI()
app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://localhost:3000"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


constraints: list[dict] = []


@app.get("/generate-points")
async def generate_points(
    num_points: int = 10,
    bbox: Annotated[list[float], Query()] = [
        -45.72072884815543,
        -23.37046541628844,
        -44.920440401158686,
        -23.036411650367697,
    ],
):
    try:
        # Generate random points within the bounding box
        # To convert a given GeoJSON coordinates to Turf's bbox format,
        # you need to extract the minimum and maximum longitude and latitude values
        # from the coordinates of the polygon. The bbox format represents
        # the bounding box coordinates as an array in the order [minX, minY, maxX, maxY].
        return random_points(num_points, bbox)

    except Exception as e:
        print("Error generating random points:", e)
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=str(e),
        )


@app.post("/constraints")
async def receive_constraints(constraint: dict):
    # TODO: Search for Turf validation/parse OR Make pydantic model work!
    constraints.append(constraint)

    return f"Constraint {constraint['id']} received"


@app.get("/constraints")
async def retrieve_constraints():
    return {
        "type": "FeatureCollection",
        "features": constraints,
    }


if __name__ == "__main__":
    import uvicorn

    uvicorn.run(app=f"{__name__}:app", reload=True)

from fastapi import APIRouter

router = APIRouter()


@router.get("/group-info")
def get_group_info():
    return {"group": "group9", "members": ["Samudra", "Rita", "Shanmei", "Evie"]}

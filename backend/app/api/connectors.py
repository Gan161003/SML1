# from fastapi import APIRouter

# from app.services.connector_service import (
#     get_all_connectors,
#     create_connector
# )

# router = APIRouter()


# @router.get("/")
# def get_connectors():

#     return get_all_connectors()


# @router.post("/")
# def add_connector(payload: dict):

#     return create_connector(payload)




















from fastapi import APIRouter

# from app.services.connector_service import (
#     get_all_connectors,
#     create_new_connector,
#     delete_existing_connector,
#     update_existing_connector
# )
from app.services.connector_service import (
    get_all_connectors,
    create_new_connector,
    delete_existing_connector,
    update_existing_connector,
    get_connector_run_history
)
router = APIRouter()


@router.get("/connectors")
def get_connectors():

    return get_all_connectors()


@router.post("/connectors")
def create_connector(payload: dict):

    print("CREATE CONNECTOR")
    print(payload)

    return create_new_connector(payload)


@router.put("/connectors/{connector_id}")
def update_connector(
    connector_id: int,
    payload: dict
):

    return update_existing_connector(
        connector_id,
        payload
    )


@router.delete("/connectors/{connector_id}")
def delete_connector(
    connector_id: int
):

    delete_existing_connector(
        connector_id
    )

    return {
        "status": "success"
    }


from app.services.connector_runner import (
    run_connector
)

@router.post(
    "/connectors/{connector_id}/run"
)
def run_connector_api(
    connector_id: int
):

    result = run_connector(
        connector_id
    )

    print(
        "RUN RESULT:",
        result
    )

    return result


@router.get(
    "/connectors/{connector_id}/history"
)
def connector_history(
    connector_id: int
):

    return get_connector_run_history(
        connector_id
    )


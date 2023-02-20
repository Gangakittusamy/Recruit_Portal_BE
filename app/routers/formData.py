from datetime import datetime
from fastapi import Depends, HTTPException, status, APIRouter
from app import schemas
from app.database import FormtableDates
from app import oauth2
from app.serializers.formSerializers import getmoduletabledata, gettabledata, getchecktabledata
from bson.objectid import ObjectId

router = APIRouter()

# Create new-tableData


@router.post('/createtabledata')
async def create_tabledata(payload: schemas.tabledataSchema, user_id: str = Depends(oauth2.require_user)):
    payload.moduleId = payload.moduleId
    payload.recuriter = payload.recuriter
    payload.created_at = datetime.utcnow()
    payload.tableData = payload.tableData
    FormtableDates.insert_one(payload.dict())
    return {"status": "Form-tableData created successfully"}

# get the particular-moudle-tableData


@router.get('/moduletabledata/{id}', status_code=status.HTTP_200_OK)
async def get_form(id: str,):
    if not ObjectId.is_valid(id):
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST,
                            detail=f"Invalid FormId: {id}")
    formtableDate = FormtableDates.find({'moduleId': str(id)})
    formtableData = []
    for form in formtableDate:
        formtableData.append(getmoduletabledata(form))
    return {"status": "success", "data": formtableData}

# get the particular-tableData


@router.get('/gettabledata/{id}', status_code=status.HTTP_200_OK)
async def get_form(id: str,):
    if not ObjectId.is_valid(id):
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST,
                            detail=f"Invalid FormId: {id}")
    formtableDate = FormtableDates.find({'_id': ObjectId(id)})
    formtableData = []
    for form in formtableDate:
        formtableData.append(gettabledata(form))
    return {"status": "success", "data": formtableData}

# get the all-tableData


@router.get('/alltabledata', status_code=status.HTTP_200_OK)
def get_me(user_id: str = Depends(oauth2.require_user)):
    formtables = FormtableDates.find()
    formtableDates = []
    for form in formtables:
        formtableDates.append(gettabledata(form))
    return {"status": "success", "user": formtableDates}

# update the particular tableData


@router.put('/updatetabledata/{id}', status_code=status.HTTP_200_OK)
async def update_tabledata(id: str, payload: schemas.updatetabledataSchema, user_id: str = Depends(oauth2.require_user)):
    if not ObjectId.is_valid(id):
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST,
                            detail=f"Invalid FormId: {id}")
    update_tabledata = FormtableDates.find_one_and_update(
        {'_id': ObjectId(id)}, {'$set': payload.dict(exclude_none=True)})
    if not update_tabledata:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,
                            detail=f'No post with this id: {id} found')
    return {"status": "Form-tabledata updated successfully"}


# update tableDatafield using moudleId
@router.put('/updatetabledatafield/{id}', status_code=status.HTTP_200_OK)
async def update_sametabledata(id: str, payload: dict, user_id: str = Depends(oauth2.require_user)):
    if not ObjectId.is_valid(id):
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST,
                            detail=f"Invalid FormId: {id}")

    payloaddata = payload.items()

    for tabedatafield in payloaddata:
        FormtableDates.update_many({
            'moduleId': str(id),
            "tableData.tableData." + tabedatafield[0]: {
                "$exists": True
            }
        },
            [
            {
                "$set": {
                    "tableData.tableData": {
                        "$map": {
                            "input": "$tableData.tableData",
                            "in": {
                                "$mergeObjects": [
                                    {
                                        "$cond": {
                                            "if": {
                                                "$eq": [
                                                    "$$this." +
                                                    tabedatafield[0],
                                                    None
                                                ]
                                            },
                                            "then": {},
                                            "else": {
                                                tabedatafield[1]: "$$this." +
                                                tabedatafield[0]
                                            }
                                        }
                                    },
                                    "$$this"
                                ]
                            }
                        }
                    }
                }
            },
            {
                "$unset": "tableData.tableData." + tabedatafield[0]
            }
        ],
            upsert=False)

    return {"status": "Form-tabledata fields changed successfully"}


# IsValueAlreadyExist
@router.post('/isvalueAlreadyExist/{id}', status_code=status.HTTP_200_OK)
async def check_isvalueAlreadyExist(id: str, payload: dict, user_id: str = Depends(oauth2.require_user)):
    if not ObjectId.is_valid(id):
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST,
                            detail=f"Invalid FormId: {id}")

    payloaddata = payload.items()
    for checkpayload in payloaddata:
        FormtableDates.find({
            'moduleId': str(id),
            "tableData.tableData." + checkpayload[0]: {
                "$exists": True
            }
        }),
 

    formtableValues = FormtableDates.find({'moduleId': str(id)})
    formtableData = []
    for form in formtableValues:
           formtableData.append(getchecktabledata(form))
  

    def check_table_data(payload, formtableData):
           for item in formtableData:
                for subitem in item['tableData']['tableData']:
                    if subitem.get(payload[0]) == payload[1]:
                        return True
           return False

    result = check_table_data(checkpayload, formtableData)
    return {"status": result}


# Delete the particular tableData
@router.delete('/deletetabledata/{id}', status_code=status.HTTP_202_ACCEPTED)
async def delete_tabledata(id: str,  user_id: str = Depends(oauth2.require_user)):
    if not ObjectId.is_valid(id):
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST,
                            detail=f"Invalid FormId: {id}")
    post = FormtableDates.find_one_and_delete({'_id': ObjectId(id)})
    if not post:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,
                            detail=f'No post with this id: {id} found')
    return {"status": "Form-tabledata deleted successfully"}

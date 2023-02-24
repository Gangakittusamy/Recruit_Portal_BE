from datetime import datetime
import json
from fastapi import Depends, HTTPException, status, APIRouter,Form
from app import schemas
from fastapi import File, UploadFile
from app.database import FormtableDates
from app import oauth2
from app.serializers.formSerializers import getmoduletabledata, gettabledata, getchecktabledata
from bson.objectid import ObjectId
from botocore.client import BaseClient
from app.setting import s3_auth
from app.upload import upload_file_to_bucket
router = APIRouter()

# Create new-tableData
@router.post('/createtabledata')
async def create_form(
    s3: BaseClient = Depends(s3_auth),
    formImage: UploadFile = File(None),
    moduleId: str = Form(),
    recuriter: str = Form(),
    tableData: str = Form(),
    user_id: str = Depends(oauth2.require_user)
):
    now = datetime.now()
    image_url = ''
    if formImage is not None:
        upload_obj = upload_file_to_bucket(
            s3_client=s3,
            profile=formImage.file,
            bucket='userlogoimage',
            object_name=formImage.filename
        )
        if upload_obj:
            image_url = f'https://userlogoimage.s3.amazonaws.com/{formImage.filename}'
        
    FormtableDates.insert_one({
        "formImage": image_url,
        "moduleId": moduleId,
        "recuriter": recuriter,
        "created_at": now,
        "tableData": json.loads(tableData)
    })
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
async def update_tabledata(
    id: str, 
    s3: BaseClient = Depends(s3_auth), 
    formImage: UploadFile = File(None), 
    tableData: str = Form(None), 
    user_id: str = Depends(oauth2.require_user)
):
    if not ObjectId.is_valid(id):
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail=f"Invalid FormId: {id}")

    updated_fields = {}
    if formImage is not None:
        upload_obj = upload_file_to_bucket(
            s3_client=s3, 
            profile=formImage.file, 
            bucket='userlogoimage', 
            object_name=formImage.filename
        )
        if upload_obj:
            image = f'https://userlogoimage.s3.amazonaws.com/{formImage.filename}'
            updated_fields['formImage'] = image

    if tableData is not None:
        updated_fields['tableData'] = json.loads(tableData)

    if not updated_fields:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="Invalid request")

    FormtableDates.find_one_and_update({'_id': ObjectId(id)}, {'$set': updated_fields})
    return {"status": "Form-tableData and Form-Image data updated successfully"}

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

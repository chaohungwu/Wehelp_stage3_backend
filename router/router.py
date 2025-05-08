from fastapi import *
from fastapi import APIRouter, HTTPException
from model.DB_ORM import DBfunction
from model.s3_function import s3_function
import json
import os

router = APIRouter()

@router.get("/api/getmessage")
async def GetMessage():
    try:
        DB = DBfunction()
        result  = DB.MessageSearch()
        return result 

    except Exception as e:
        print(e)
        raise HTTPException(
            status_code=500,
            detail={"error": True, "message": "伺服器內部錯誤"}
        )


@router.post("/upload")
async def upload_message(request:Request, file:UploadFile = File(None) , message:str = Form(None)):
    message_text = message
    DB_func = DBfunction() #資料庫操作程式
    s3_func = s3_function() #S3操作程式

    try:
        #如果有上傳圖片檔案
        if file:
            UploadImg_result = await s3_func.UploadImgToS3(img_file = file) #上傳到s3
            DB_func.MessageInsertToDB(message = message_text, upload_img_url = UploadImg_result['img_path']) #存入DB
            return {"message":"留言上傳成功", "ok":True}
        
        #沒有上傳圖片檔案
        else:
            DB_func.MessageInsertToDB(message = message_text, upload_img_url = "") #存入DB


    except Exception as e:
        print(e)
        raise HTTPException(status_code=500, detail={"error": True, "message": "伺服器內部錯誤"})


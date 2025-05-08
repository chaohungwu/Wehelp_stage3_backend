from fastapi import APIRouter, HTTPException
from model.DB_ORM import DBfunction


DBfunction = DBfunction()
GetMessage = DBfunction.Messagesearch()
print(GetMessage)
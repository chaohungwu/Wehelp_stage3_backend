from fastapi import *
from fastapi.responses import FileResponse
from router.router import router
from fastapi.staticfiles import StaticFiles

app = FastAPI()

app.include_router(router)

@app.get("/messageboard", include_in_schema=False)
async def index(request: Request):
	return FileResponse("./static/index.html", media_type="text/html")

app.mount("/static", StaticFiles(directory="static"))#所有靜態文件資料夾

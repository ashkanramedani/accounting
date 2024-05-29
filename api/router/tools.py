from enum import Enum

from fastapi import APIRouter, Depends
from fastapi import HTTPException
from starlette.responses import RedirectResponse

import db as dbf
from db.models import get_db
from lib.log import logger


class log_mode(str, Enum):
    csv = 'csv'
    log = 'log'


router = APIRouter()


@router.get("/", include_in_schema=False)
async def docs_redirect():
    return RedirectResponse(url='/docs')



# def generate_html(log_content):
#     # Generate HTML content to display the log file content
#     html_content = f"""
#     <html>
#     <head>
#         <title>Log File</title>
#     </head>
#     <body>
#         <pre>{log_content}</pre>
#     </body>
#     </html>
#     """
#     return html_content


# @router.get("/log", response_class=HTMLResponse, include_in_schema=False)
# async def render_log_file(response: Response):
#     try:
#         log_path = logger.log_path
#         if not log_path:
#             response.status_code = 404
#             return "<h1>Log file not Specified in config</h1>"
#         with open("./log/Log.log", "r") as log_file:
#             log_content = log_file.read()
#             # Generate HTML content
#             html_content = generate_html(log_content)
#             return html_content
#     except FileNotFoundError:
#         response.status_code = 404
#         return "<h1>Log file not found</h1>"
#     except Exception as e:
#         response.status_code = 500
#         return f"<h1>An error occurred: {str(e)}</h1>"


# @router.get("/log", include_in_schema=False, response_class=HTMLResponse)
# async def log(mode: log_mode = 'log'):
#     templates = Jinja2Templates(directory="./")
#     log_path = normpath(f'{dirname(__file__)}/../log/log.{mode}')
#     if mode == 'csv':
#         pd.read_csv(log_path).to_html("./Tables.html")
#         return templates.TemplateResponse("./Tables.html")
#         # return "pd.read_csv(log_path).to_dict()"
#     with open(log_path, "r") as f:
#         log_file = f.read()
#     return log_file


@router.get("/api/v1/form/count", tags=["Ping"])
async def count(field: str, db=Depends(get_db)):
    status_code, result = dbf.count(db, field)
    if status_code != 200:
        raise HTTPException(status_code=status_code, detail=result)
    return result


@router.get("/ping", tags=["Ping"])
def ping():
    return "Pong"


@router.get("/count", tags=["Ping"], deprecated=True)
async def count(field: str, db=Depends(get_db)):
    logger.warning(f'Deprecated. Use /api/v1/form/count')
    if not field:
        raise HTTPException(status_code=400, detail="Field is required")
    status_code, result = dbf.count(db, field)
    if status_code != 200:
        raise HTTPException(status_code=status_code, detail=result)
    return result


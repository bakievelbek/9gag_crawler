import subprocess

from api.check_user import check_url_status
from api.config import settings

from typing import Optional
from pydantic import BaseModel

from fastapi import APIRouter, BackgroundTasks, HTTPException


class User(BaseModel):
    username: str
    limit: Optional[int] = 100
    output_format: Optional[str] = 'json'


router = APIRouter()


def run_spider(username: str, limit: int, output_format: str):
    if limit:
        process = subprocess.Popen(
            ['scrapy', 'crawl', 'ninegag_user_posts', '-a', f'user={username}', '-a', f'limit={limit}', '-s',
             f'OUTPUT_FORMAT={output_format}'])
    else:
        process = subprocess.Popen(['scrapy', 'crawl', 'ninegag_user_posts', '-a', f'user={username}', '-s',
                                    f'OUTPUT_FORMAT={output_format}'])

    process.communicate()


@router.post("/crawl")
def start_crawl(user: User, background_tasks: BackgroundTasks):
    if not check_url_status(settings.USER_URL + user.username):
        raise HTTPException(status_code=404, detail=f"The user {user} Not Found.")

    background_tasks.add_task(run_spider, user.username, user.limit, user.output_format)
    return {"message": "Crawling started for user: " + user.username}

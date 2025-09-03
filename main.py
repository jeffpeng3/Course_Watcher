from aiohttp import ClientSession
from asyncio import sleep, run
from json import loads
from os import getenv
url = 'https://querycourse.ntust.edu.tw/querycourse/api/courses'

payload = {
    'CourseNo': 'ET5003701',
    'Language': 'zh',
    'Semester': '1141'
}

dc = {
    "content": "123",
    "embeds": None,
    "attachments": []
}

courseList = loads(getenv("COURSES", "[]"))
webhook = getenv("WEBHOOK", "")
print(courseList)
print(webhook)

async def main():
    print("a")
    async with ClientSession() as session:
        print("b")
        while True:
            print("c")
            for i in courseList:
                print(end='.', flush=True)
                payload['CourseNo'] = i
                try:
                    async with session.post(url, json=payload, ssl=False) as response:
                        data = (await response.json())[0]
                        if int(data['Restrict2']) - data['ChooseStudent'] > 0:
                            print(data['CourseName'], data['CourseNo'], flush=True)
                            if webhook:
                                dc['content'] = f"{data['CourseName']} {data['CourseNo']}"
                                async with session.post(webhook, json=dc, ssl=False) as r:
                                    print(await r.text(), flush=True)
                except Exception as e:
                    print("pass i because", e, flush=True)
                await sleep(0.3)
run(main())
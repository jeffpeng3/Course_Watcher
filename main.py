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
courseList = loads(getenv("COURSES", "[]"))
async def main():
    async with ClientSession() as session:
        while True:
            for i in courseList:
                payload['CourseNo'] = i
                try:
                    async with session.post(url, json=payload, ssl=False) as response:
                        data = (await response.json())[0]
                        if int(data['Restrict2']) - data['ChooseStudent'] > 0:
                            print(data['CourseName'], data['CourseNo'])
                        await sleep(0.3)
                except Exception as e:
                    print("pass i because", e)
run(main())
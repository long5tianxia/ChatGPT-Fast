import orjson
import aiohttp
from time import time
from hashlib import md5
from fastapi import APIRouter, BackgroundTasks, Query
from app.api.v1.chat.schemas import sChat_Body

api = APIRouter()
chat_resp = {}


@api.post('/completions', summary='对话')
async def Chat_Completions(body: sChat_Body, background_tasks: BackgroundTasks):
    ldata = {
        'model': body.model,
        'messages': body.messages,
        'stream': True
    }
    if body.max_tokens > 0:
        ldata['max_tokens'] = body.max_tokens
    if body.temperature >= 0 and body.temperature <= 2:
        ldata['temperature'] = body.temperature
    taskid = time().__str__() + body.messages.__str__()
    taskid = md5(taskid.encode()).hexdigest()[0:16]
    background_tasks.add_task(
        OpenAI_Completions, sk=body.sk, ldata=ldata, taskid=taskid)
    return {'code': 200, 'data': {'taskid': taskid}}


# 后台对话任务
async def OpenAI_Completions(sk: str, ldata: dict, taskid: str):
    lheaders = {
        'Content-Type': 'application/json',
        'Authorization': f'Bearer {sk}',
    }
    global chat_resp
    lproxy = None
    chat_resp[taskid] = {}
    chat_resp[taskid]['code'] = 201
    chat_resp[taskid]['content'] = ''
    try:
        async with aiohttp.ClientSession(headers=lheaders) as lhttp:
            async with lhttp.post(url='https://api.openai.com/v1/chat/completions', proxy=lproxy, data=orjson.dumps(ldata).decode()) as lresp:
                lresp_t = ''
                while True:
                    chunk = await lresp.content.read(n=512)
                    if not chunk:
                        break
                    lresp_t = lresp_t + chunk.decode().strip()
                    larr = lresp_t.split('data: ')
                    lresp_t = ''
                    for chunk in larr:
                        try:
                            chunk_obj = orjson.loads(chunk)
                        except Exception:
                            lresp_t = chunk
                        else:
                            if 'choices' in chunk_obj:
                                choices_: dict = chunk_obj['choices'][0]
                                if 'delta' not in choices_:
                                    continue
                                if 'content' in choices_['delta']:
                                    chat_resp[taskid]['content'] = chat_resp[taskid]['content'] + choices_[
                                        'delta']['content']
        chat_resp[taskid]['code'] = 200
    except Exception as e:
        chat_resp[taskid]['msg'] = e.__str__()
        chat_resp[taskid]['code'] = 500


@api.get('/result.get', summary='获取对话结果')
async def Chat_Result(taskid: str = Query(...)):
    global chat_resp
    if taskid not in chat_resp:
        return {'code': 400, 'message': '对话任务不存在'}
    task_dict = chat_resp[taskid]
    task_code = task_dict['code']
    if task_code == 500:
        return {'code': 500, 'message': task_dict['msg']}
    return {'code': task_code, 'data': task_dict['content']}

from fastapi import FastAPI, HTTPException
import time

# 注释掉requests，改用模拟数据避免SSL问题
# import requests

app = FastAPI()


# 1. MCP描述接口（告诉大模型功能和参数）
@app.get("/mcp/describe")
def describe():
    return {
        "name": "JokeGenerator",
        "description": "生成随机中文笑话，适合聊天互动场景",
        "parameters": {
            "type": "object",
            "properties": {
                "category": {
                    "type": "string",
                    "enum": ["糗事", "冷笑话", "职场", "校园"],
                    "description": "笑话分类，支持糗事/冷笑话/职场/校园"
                }
            }
        }
    }


# 2. 本地模拟笑话数据（完全不依赖外部接口，避免SSL问题）
mock_jokes = {
    "糗事": [
        "今天在超市看到一个长得很凶的大哥，他买了一袋小番茄，一颗颗往嘴里扔，没接住就弯腰去捡。我看他捡了三次，忍不住说：“大哥，用勺子吧？” 他瞪了我一眼：“我乐意，你管得着吗？” 然后下一颗又掉了，他默默从兜里掏出了勺子……",
        "小时候偷穿妈妈的高跟鞋，结果摔了一跤，把牙磕掉了一小块。现在每次相亲，对方都会问：“你牙齿怎么缺了一点？” 我总不能说：“这是我为时尚付出的代价吧……”"
    ],
    "冷笑话": [
        "为什么数学书总是很忧郁？因为它有太多的问题。",
        "什么水果最让人感到害怕？—— 芒果，因为“芒”（盲）目的害怕。"
    ],
    "职场": [
        "老板：“这个项目你加班赶一下，明天必须交。” 我：“好的老板，不过我加班的话，明天可能起不来，上午就没法交了。” 老板：“……”",
        "同事问我：“你上班为什么总带着保温杯？” 我说：“因为我随时可能‘凉’了。”"
    ],
    "校园": [
        "老师：“请用‘一带一路’造句。” 学生：“我家一带一路灯坏了。” 老师：“……”",
        "考试时同桌偷偷问我：“这道题选什么？” 我告诉他：“选C。” 结果他选了B，还抱怨我骗他。后来我才发现，他看的是我的答题卡背面……"
    ]
}


# 3. MCP调用接口（使用本地模拟数据）
@app.post("/mcp/call")
def call(data: dict):
    category = data.get("category", None)

    # 校验分类是否合法
    if category and category not in mock_jokes:
        raise HTTPException(status_code=400, detail="不支持的分类，请从['糗事', '冷笑话', '职场', '校园']中选择")

    # 随机选择一个笑话（如果没指定分类，就随机选一个分类）
    if not category:
        import random
        category = random.choice(list(mock_jokes.keys()))

    import random
    joke = random.choice(mock_jokes[category])

    return {
        "joke": joke,
        "category": category,
        "query_time": time.strftime("%Y-%m-%d %H:%M:%S", time.localtime()),
        "source": "本地模拟数据"
    }


# 启动服务
if __name__ == "__main__":
    import uvicorn

    uvicorn.run(app, host="0.0.0.0", port=8001)

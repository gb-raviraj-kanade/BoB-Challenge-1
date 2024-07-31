from contextlib import asynccontextmanager
from fastapi import FastAPI
from app.agent_chat import Agent
from app.insights import InsightAgent
from app.notification import NotificationGenerator

user_chat_agents = {}

@asynccontextmanager
async def lifespan(app: FastAPI):
    global insight_agent, notification_agent, user_chat_agents
    insight_agent = InsightAgent()
    notification_agent = NotificationGenerator()
    for idx in range(10):
        user_chat_agents[f"Customer{idx+1}"] = None
    yield

app = FastAPI(lifespan=lifespan)


@app.get("/user_insight/{user_name}")
def get_user_insight(user_name: str):
    result = insight_agent.get_insights(user_name)
    return result

@app.get("/notification/email/{user_name}")
def get_user_notification(user_name: str):
    result = notification_agent.generate_email(user_name)
    return result

@app.get("/check_anomaly/{user_name}")
def check_anomaly(user_name: str):
    result = notification_agent.check_anomaly(user_name)
    return result

@app.post("/on_chat_start")
def on_chat_start(user_name: str):
    user_chat_agents[user_name] = Agent(user_name)
    return {"success": True, "message": "Chat initialized"}

@app.post("/on_message")
def on_message(user_name: str, message: str):
    response = user_chat_agents[user_name].chat(message)
    return {"success": True, "response": response}

@app.post("/on_chat_end")
def on_chat_end(user_name: str):
    user_chat_agents[user_name].summarize()
    user_chat_agents[user_name] = None
    return {"success": True, "message": "Chat ended"}

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="127.0.0.1", port=8001)
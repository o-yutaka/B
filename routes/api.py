from fastapi import APIRouter, BackgroundTasks, Form, Request
from fastapi.responses import HTMLResponse, JSONResponse, PlainTextResponse, Response
from fastapi.templating import Jinja2Templates

from agent_state import state_tracker
from ai import run as ollama_run
from memory import memory_store
from runtime import runtime_engine

router = APIRouter()
templates = Jinja2Templates(directory="static")


def process_whatsapp_async(sender: str, body: str) -> None:
    text = (body or "").strip()
    if text.startswith("/run"):
        task = text.replace("/run", "", 1).strip() or "ユーザー指定タスクを実行"
        runtime_engine.enqueue_task(task, "user")
        memory_store.append("whatsapp", "コマンド/run受付", status="success", extra={"from": sender, "task": task})
        return
    if text.startswith("/product"):
        request_text = text.replace("/product", "", 1).strip() or "小規模Webアプリを生成"
        product = runtime_engine.generate_product(request_text)
        memory_store.append("whatsapp", "コマンド/product実行", status="success", extra={"from": sender, "product": product})
        return
    if text.startswith("/push"):
        result = runtime_engine.trigger_auto_pr("AI Generated Update", "Automated PR from BLACK ORIGIN")
        memory_store.append("whatsapp", "コマンド/push実行", status="success", extra={"from": sender, "result": result})
        return

    reply = ollama_run(text or "こんにちは")
    memory_store.append("whatsapp", "非同期AI応答完了", status="success", extra={"from": sender, "reply": reply[:500]})
    print(f"[whatsapp] 非同期処理完了 from={sender}")


def build_whatsapp_message(body: str) -> str:
    text = (body or "").strip()
    if text.startswith("/status"):
        agents = state_tracker.snapshot()
        summary = ", ".join([f"{v['name']}={v['status']}" for v in agents.values()])
        return f"稼働中です。{summary}" if summary else "稼働中です。"
    if text.startswith("/log"):
        logs = memory_store.latest(3)
        lines = [f"{x['category']}:{x['status']}" for x in logs]
        return "最新ログ: " + " | ".join(lines)
    if text.startswith("/run"):
        return "タスクを受付しました。処理を開始します。"
    if text.startswith("/product"):
        return "プロダクト生成を開始しました。"
    if text.startswith("/push"):
        return "GitHub PR処理を開始しました。"
    return "処理中です…"


@router.get("/", response_class=HTMLResponse)
async def dashboard(request: Request) -> HTMLResponse:
    logs = memory_store.latest(10)
    return templates.TemplateResponse("dashboard.html", {"request": request, "logs": logs, "agents": state_tracker.snapshot()})


@router.get("/logs", response_class=JSONResponse)
async def logs() -> JSONResponse:
    return JSONResponse(content={"logs": memory_store.latest(10), "agents": state_tracker.snapshot(), "performance": runtime_engine.monitor.metrics(runtime_engine.task_queue.size())})


@router.post("/chat", response_class=JSONResponse)
async def chat(payload: dict) -> JSONResponse:
    message = payload.get("message", "")
    memory_store.append("chat", "ユーザー入力受信", extra={"message": message})
    runtime_engine.enqueue_task(message, "user")
    reply = ollama_run(message)
    memory_store.append("chat", "AI応答送信", status="success", extra={"reply": reply[:500]})
    return JSONResponse(content={"reply": reply})


@router.post("/whatsapp")
async def whatsapp(
    background_tasks: BackgroundTasks,
    Body: str = Form(default=""),  # noqa: N803
    From: str = Form(default=""),  # noqa: N803
) -> Response:
    memory_store.append("whatsapp", "Webhook受信", extra={"from": From, "body": Body})
    print(f"[whatsapp] 受信 from={From}")
    background_tasks.add_task(process_whatsapp_async, From, Body)
    immediate_message = build_whatsapp_message(Body)
    xml = f"""<?xml version=\"1.0\" encoding=\"UTF-8\"?>
<Response>
  <Message>{immediate_message}</Message>
</Response>"""
    return Response(content=xml, media_type="application/xml")


@router.post("/run-once", response_class=JSONResponse)
async def run_once() -> JSONResponse:
    result = await runtime_engine.loop_once()
    return JSONResponse(content=result)


@router.get("/health", response_class=PlainTextResponse)
async def health() -> PlainTextResponse:
    return PlainTextResponse("ok")

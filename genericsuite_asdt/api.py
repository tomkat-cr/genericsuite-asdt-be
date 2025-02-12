import asyncio

from fastapi import FastAPI, Form
from fastapi.responses import StreamingResponse
from fastapi.staticfiles import StaticFiles

import uvicorn

from genericsuite_asdt.main import stream_run


app = FastAPI()

# Mount the static directory
app.mount("/static", StaticFiles(
    directory="genericsuite_asdt/static"),
    name="static")


def run_api(host: str = "0.0.0.0", port: int = 8001):
    uvicorn.run(app, host=host, port=port)


async def stream_output(project: str, topic: str):
    """
    Generate a stream of data for the client to consume
    """
    # Add a small delay to prevent overwhelming the client
    delay = 0.1
    for output in stream_run(project, topic):
        yield f"data: {output}\n\n"
        await asyncio.sleep(delay)


@app.post("/generate")
async def generate(
    project: str = Form(
        ...,
        description="The project or action(s) to accomplish"),
    topic: str = Form(
        ...,
        description="An additional topic to generate content for")
):
    """
    Generate endpoint to start a CrewAI run

    Args:
    project (str): The project name
    topic (str): The topic to generate content for

    """
    return StreamingResponse(
        stream_output(project, topic),
        media_type="text/event-stream"
    )


if __name__ == "__main__":
    run_api()

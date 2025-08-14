import asyncio
import logging
import json
from quart import Quart, render_template, request, Response
from typing import TypedDict
import ollama

# === App Setup === #
app = Quart(__name__)
logging.basicConfig(level=logging.DEBUG, format='%(asctime)s - %(levelname)s - %(message)s')
logger = logging.getLogger(__name__)

# === Ollama Client === #
ollama_client = ollama.Client()
model = "gemma3:1b-it-qat"

# === Frontend Routes for the new pages === #
@app.route("/")
async def index():
    # This is the home page with the MVP generator
    return await render_template("index_new.html")

@app.route("/about")
async def about():
    # This is the about page
    return await render_template("about.html")

@app.route("/contact")
async def contact():
    # This is the contact page
    return await render_template("contact.html")


# === Health Check === #
@app.route("/health")
async def health_check():
    try:
        test = ollama_client.chat(
            model=model,
            messages=[{"role": "user", "content": "Hi"}],
            stream=False
        )
        logger.info(f"Health check successful for model: {model}")
        return {"status": "ok", "model": model}
    except Exception as e:
        logger.error(f"Health check failed: {str(e)}")
        return {"status": "error", "message": str(e)}, 503

# === MVP Generation Route with immediate initial response === #
@app.route("/generate", methods=["POST", "GET"])
async def generate():
    data = await request.json if request.method == "POST" else request.args
    idea = data.get("idea", "")
    if not idea:
        logger.warning("No idea provided in request")
        return Response(
            json.dumps({"error": "No idea provided."}),
            mimetype='application/json',
            status=400
        )

    logger.info(f"User idea received: '{idea}'")

    async def event_generator():
        try:
            # Send an immediate response to prime the connection
            yield f"data: {json.dumps({'type': 'status', 'message': 'Request received. Starting generation process...'})}\n\n"
            
            sections = [
                {
                    "name": "research",
                    "system": "You are a concise market researcher.",
                    "prompt": f"""Generate a 2-line paragraph on market opportunities for the product idea: **{idea}**, and list 2 key points."""
                },
                {
                    "name": "features",
                    "system": "You are a pragmatic Product Manager.",
                    "prompt": f"""Generate a 2-line paragraph on the user experience and core features for the product: **{idea}**, and list 2 key points on feature prioritization."""
                },
                {
                    "name": "code",
                    "system": "You are a 10x Principal Software Engineer. Write a basic, well-documented FastAPI application. Focus on key fields and note any 'null' or unspecified ones.",
                    "prompt": f"""Write a single FastAPI application file for the product idea: **{idea}**.
The code should be short, well-commented, and include:
- Pydantic models with only the most important fields explicitly defined.
- A comment for a 'null_field' to indicate a field that is unspecified.
- A simple GET and a POST endpoint using the Pydantic models.
"""
                },
                {
                    "name": "review",
                    "system": "You are a succinct Code Reviewer.",
                    "prompt": f"""Generate a 2-line paragraph on security and scalability for the proposed implementation of **{idea}**, and list 2 key points on improvements or risks."""
                }
            ]

            # Yield the first event to reset timers
            yield f"data: {json.dumps({'type': 'start', 'message': 'Starting MVP generation...'})}\n\n"

            for section in sections:
                logger.debug(f"Starting generation for section: {section['name']}")
                yield f"data: {json.dumps({'type': 'step_start', 'step': section['name']})}\n\n"
                
                try:
                    messages = [{"role": "system", "content": section["system"]}, {"role": "user", "content": section["prompt"]}]
                    section_content = ""
                    # Flag to track if we have started streaming substantive content
                    is_first_chunk = True
                    
                    for chunk in ollama_client.chat(model=model, messages=messages, stream=True):
                        if 'message' in chunk and 'content' in chunk['message']:
                            token = chunk['message']['content']
                            if token:
                                if is_first_chunk:
                                    is_first_chunk = False
                                    # Filter out common conversational intros or "inner thoughts"
                                    # This is a heuristic and might need to be refined for other models
                                    if token.strip().lower().startswith(("thought", "i will", "based on")):
                                        continue # Skip this initial, non-substantive chunk
                                    
                                section_content += token
                                yield f"data: {json.dumps({'type': 'text_chunk', 'step': section['name'], 'content': token})}\n\n"
                                await asyncio.sleep(0.005)
                            
                    yield f"data: {json.dumps({'type': 'step_complete', 'step': section['name'], 'final_content': section_content})}\n\n"
                    if section["name"] != sections[-1]["name"]:
                        yield f"data: {json.dumps({'type': 'status_update', 'message': f'Done with {section['name']}. Generating next section...'})}\n\n"
                    logger.debug(f"Completed generation for section: {section['name']}")
                    
                except Exception as e:
                    logger.error(f"Section {section['name']} failed: {str(e)}")
                    yield f"data: {json.dumps({'type': 'error', 'error': f"Section {section['name']} failed: {str(e)}"})}\n\n"

            logger.info("MVP generation completed successfully")
            yield f"data: {json.dumps({'type': 'complete', 'message': 'MVP generation completed!'})}\n\n"

        except Exception as e:
            logger.error(f"Streaming failed: {str(e)}", exc_info=True)
            yield f"data: {json.dumps({'type': 'error', 'error': f"Streaming failed: {str(e)}"})}\n\n"

    return Response(event_generator(), mimetype='text/event-stream', headers={
        'Cache-Control': 'no-cache',
        'X-Accel-Buffering': 'no',
        'Connection': 'keep-alive'
    })

# === Run Server === #
if __name__ == "__main__":
    app.run(host="127.0.0.1", port=8000, debug=True)

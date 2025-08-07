from quart import Quart, render_template, request, jsonify
from mcp.server.fastmcp import FastMCP
import ollama
import logging
import asyncio

app = Quart(__name__)
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

# === Ollama Client === #
ollama_client = ollama.Client()
model = "mistral"

# === Initialize MCP Server === #
mcp = FastMCP("BuildPilot")

# === Agents === #
@mcp.tool("research_idea")
async def research_idea(input: str) -> str:
    logger.info(f"[Researcher] Researching: {input}")
    response = ollama_client.chat(model=model, messages=[{
        "role": "user",
        "content": f"Do quick market research on this app idea: {input}",
    }])
    return response['message']['content']

@mcp.tool("plan_features")
async def plan_features(research: str) -> str:
    logger.info(f"[Planner] Planning features based on research")
    response = ollama_client.chat(model=model, messages=[{
        "role": "user",
        "content": f"Based on this research, break the product into features with priorities:\n{research}",
    }])
    return response['message']['content']

@mcp.tool("generate_code")
async def generate_code(features: str) -> str:
    logger.info(f"[Coder] Generating code")
    response = ollama_client.chat(model=model, messages=[{
        "role": "user",
        "content": f"Generate code for this feature list as a FastAPI backend:\n{features}",
    }])
    return response['message']['content']

@mcp.tool("review_code")
async def review_code(code: str) -> str:
    logger.info(f"[Reviewer] Reviewing code")
    response = ollama_client.chat(model=model, messages=[{
        "role": "user",
        "content": f"Review and improve this code:\n{code}",
    }])
    return response['message']['content']

# === UI === #
@app.route("/")
async def index():
    return await render_template("index_new.html")

# === Main Pipeline === #
@app.route("/process", methods=["POST"])
async def process():
    data = await request.json
    idea = data.get("idea", "")
    logger.info(f"[User Input] Idea: {idea}")

    try:
        research = await mcp.invoke("research_idea", idea)
        plan = await mcp.invoke("plan_features", research)
        code = await mcp.invoke("generate_code", plan)
        review = await mcp.invoke("review_code", code)

        return jsonify({
            "research": research,
            "plan": plan,
            "code": code,
            "review": review
        })

    except Exception as e:
        logger.exception("Pipeline failed")
        return jsonify({"error": str(e)}), 500

# === Start Server === #
if __name__ == "__main__":
    logger.info("Starting Quart server...")
    asyncio.run(app.run_task(host="127.0.0.1", port=8000, debug=True))

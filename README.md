# BuildPilot-Agentic-MVP-Generator-with-MCP
Autonomous platform that transforms user ideas into production-ready MVPs using LangGraph agents and FastMCP. Integrates LLM-driven planning, code generation, and deployment pipelines with contextual memory and feedback loops for hands-free product development

# BuildPilot – Agentic MVP Generator
Overview
BuildPilot is an autonomous system that transforms user ideas into deployable Minimum Viable Products (MVPs) using LangGraph agents and the Model Context Protocol (MCP) via the fastmcp library. It orchestrates a team of intelligent agents—Researcher, Planner, Architect, and Developer—to research tools, design architectures, and generate full-stack code. MCP ensures agents retain long-term memory and pass structured knowledge, while fastmcp provides a high-level, Pythonic interface for building MCP servers with tools and prompts.

For example, a user request like “build a travel planner with weather integration” triggers the agents to:
Research: Identify tools (e.g., OpenWeatherMap API, FastAPI, React) using an MCP tool.
Plan: Define features (e.g., itinerary creation, weather forecasts) with an MCP prompt template.
Architect: Design the system (e.g., REST API, frontend UI).
Develop: Generate backend/frontend code and project structure.

The result is a deployable MVP delivered in minutes, ideal for startups and product teams.

Architecture
BuildPilot uses a LangGraph workflow with four agents:
Researcher: Queries external APIs via an MCP tool (e.g., fetch_weather_data).
Planner: Creates a feature list using an MCP prompt (e.g., plan_template).
Architect: Designs the system architecture.
Developer: Generates code using MCP context.
MCP and FastMCP
MCP: Structures agent memory and interactions via Resources, Tools, and Prompts.
Tools: Executable functions (e.g., fetch_weather_data for API calls, create_itinerary for trip planning).
Prompts: Reusable templates (e.g., plan_template for feature planning).
FastMCP: Simplifies MCP server creation with decorators (@mcp.tool, @mcp.prompt) for high-performance memory and communication.
Workflow
Input: User submits an idea via a REST API (FastAPI).
Agent Coordination: LangGraph manages agent execution, passing MCP-structured context.
MCP Server: Handles tools and prompts for dynamic data fetching and interaction templating.
Output: A zip file or folder with the MVP (e.g., FastAPI backend, React frontend).

Setup

Workflow

Input: User submits an idea via a REST API (FastAPI).
Agent Coordination: LangGraph manages agent execution, passing MCP-structured context.
Memory: fastmcp stores and retrieves agent memory for continuity.
Output: A zip file or folder with the MVP (e.g., FastAPI backend, React frontend).

MCP and FastMCP

MCP: Structures agent memory as key-value pairs with metadata (e.g., context_id, role, data).
FastMCP: A high-performance library (simulated here) for memory storage and inter-agent communication.

Setup

Clone the repository:git clone https://github.com/bharathmrr/BuildPilot-Agentic-MVP-Generator-with-MCP.git
cd BuildPilot-Agentic-MVP-Generator


Install dependencies:pip install -r requirements.txt


Run the FastAPI server:uvicorn main:app --reload


Send a POST request to /generate_mvp with the idea (e.g., {"idea": "travel planner with weather integration"}).

Requirements

Python 3.10+
LangGraph, FastAPI, Pydantic, aiohttp
(Optional) Docker for deployment

Example Usage
curl -X POST http://localhost:8000/generate_mvp -H "Content-Type: application/json" -d '{"idea": "travel planner with weather integration"}'

Output
The system generates a project folder with:

backend/: FastAPI server with weather API integration.
frontend/: React app for the travel planner UI.
README.md: Instructions for running the MVP.

Future Improvements

Add support for database integration (e.g., SQLite, MongoDB).
Enhance fastmcp with distributed memory caching.
Support additional frontend frameworks (e.g., Vue, Svelte).

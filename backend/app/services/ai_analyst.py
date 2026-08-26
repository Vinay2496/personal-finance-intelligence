import os
from google import genai
from google.genai import types
from sqlalchemy.orm import Session

from app.services.ai_tools import TOOL_REGISTRY

client = genai.Client(api_key=os.environ.get("GEMINI_API_KEY"))

SYSTEM_INSTRUCTION = """You are a personal finance analyst assistant inside a budgeting app.
Rules you MUST follow:
- Only state numbers that come from tool results. Never invent or estimate numbers yourself.
- Never mention SQL, databases, internal code, or system architecture.
- Never call anything "fraud detection" — call it "unusual transaction detection" if relevant.
- Be concise, friendly, and specific. Reference actual figures returned by tools.
- All monetary amounts are in Indian Rupees. Always use the ₹ symbol, never $ or USD.
- If a tool returns no data or an error, tell the user honestly that the data isn't available yet.
- Only answer questions about the user's personal finances/spending. Politely decline anything else.
"""

TOOL_DECLARATIONS = [
    types.FunctionDeclaration(
        name="get_monthly_spending",
        description="Get income, expenses, and savings for each month on record.",
        parameters=types.Schema(type=types.Type.OBJECT, properties={}),
    ),
    types.FunctionDeclaration(
        name="get_category_spending",
        description="Get total spending broken down by category (e.g. Food, Utilities).",
        parameters=types.Schema(type=types.Type.OBJECT, properties={}),
    ),
    types.FunctionDeclaration(
        name="compare_months",
        description="Compare the most recent month's spending to the previous month.",
        parameters=types.Schema(type=types.Type.OBJECT, properties={}),
    ),
    types.FunctionDeclaration(
        name="get_top_merchants",
        description="Get the merchants the user spent the most money at.",
        parameters=types.Schema(type=types.Type.OBJECT, properties={}),
    ),
    types.FunctionDeclaration(
        name="get_recurring_expenses",
        description="Get expenses that repeat monthly, like subscriptions or rent.",
        parameters=types.Schema(type=types.Type.OBJECT, properties={}),
    ),
    types.FunctionDeclaration(
        name="get_unusual_transactions",
        description="Get transactions that are statistically much larger than the user's typical spending.",
        parameters=types.Schema(type=types.Type.OBJECT, properties={}),
    ),
    types.FunctionDeclaration(
        name="forecast_spending",
        description="Get a forecast of the user's expenses for next month.",
        parameters=types.Schema(type=types.Type.OBJECT, properties={}),
    ),
    types.FunctionDeclaration(
        name="get_savings_rate",
        description="Get overall income, expenses, total savings, and savings rate percentage.",
        parameters=types.Schema(type=types.Type.OBJECT, properties={}),
    ),
]

TOOLS = types.Tool(function_declarations=TOOL_DECLARATIONS)

MAX_TOOL_ROUNDS = 5


def ask_ai_analyst(question: str, user_id: int, db: Session) -> str:
    config = types.GenerateContentConfig(
        system_instruction=SYSTEM_INSTRUCTION,
        tools=[TOOLS],
    )

    contents = [types.Content(role="user", parts=[types.Part(text=question)])]

    for _ in range(MAX_TOOL_ROUNDS):
        response = client.models.generate_content(
            model="gemini-3.6-flash",
            contents=contents,
            config=config,
        )

        candidate = response.candidates[0]
        function_calls = [
            part.function_call
            for part in candidate.content.parts
            if part.function_call is not None
        ]

        if not function_calls:
            return response.text or "I couldn't generate a response. Please try again."

        contents.append(candidate.content)

        for fc in function_calls:
            tool_fn = TOOL_REGISTRY.get(fc.name)
            if tool_fn is None:
                result = {"error": f"Unknown tool: {fc.name}"}
            else:
                args = dict(fc.args) if fc.args else {}
                result = tool_fn(user_id, db, **args)

            contents.append(
                types.Content(
                    role="user",
                    parts=[
                        types.Part(
                            function_response=types.FunctionResponse(
                                name=fc.name,
                                response={"result": result},
                            )
                        )
                    ],
                )
            )

    return "I gathered the data but had trouble summarizing it. Please try rephrasing your question."
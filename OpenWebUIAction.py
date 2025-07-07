import requests
from datetime import datetime
from pydantic import BaseModel, Field
from typing import Callable, Any, Dict

DEBUG = True


class Action:
    class Valves(BaseModel):
        WEBHOOK_URL: str = Field(
            default="http://127.0.0.1:5000/webhook",
            description="Your custom webhook URL.",
        )
        HOVER_DESCRIPTION: str = Field(
            default="Send Command to Webhook",
            description="Custom description that appears when hovering over the icon.",
        )

    def __init__(self):
        self.valves = self.Valves()

    def status_object(
        self,
        description: str = "Processing",
        status: str = "in_progress",
        done: bool = False,
    ) -> Dict:
        return {
            "type": "status",
            "data": {
                "status": status,
                "description": description,
                "done": done,
            },
        }

    async def action(
        self,
        body: dict,
        __user__: dict = {},
        __event_emitter__: Callable[[dict], Any] = None,
        __event_call__: Callable[[dict], Any] = None,
    ) -> None:
        if DEBUG:
            print(f"Debug: Webhook action invoked")

        try:
            if __event_emitter__:
                await __event_emitter__(self.status_object("Initializing Webhook"))

            if not self.valves.WEBHOOK_URL:
                raise ValueError("Webhook URL is not configured")

            # Get the last assistant message from the conversation
            messages = body.get("messages", [])
            assistant_message = next(
                (
                    message.get("content")
                    for message in reversed(messages)
                    if message.get("role") == "assistant"
                ),
                None,
            )

            if not assistant_message:
                raise ValueError("No assistant message found to send")

            # Prepare the payload
            data = {
                "command": assistant_message,
                "timestamp": datetime.now().isoformat(),
                "source": "OpenWebUI",
            }

            if __event_emitter__:
                await __event_emitter__(
                    self.status_object("Sending Command to WebHook")
                )

            # Send
            response = requests.post(
                self.valves.WEBHOOK_URL,
                json=data,
                headers={
                    "Content-Type": "application/json",
                    "User-Agent": "OpenWebUI-Webhook",
                },
            )

            if response.status_code in [200, 201, 204]:
                if __event_emitter__:
                    await __event_emitter__(
                        self.status_object(
                            "Content successfully sent",
                            status="complete",
                            done=True,
                        )
                    )
            else:
                raise ValueError(
                    f"Failed to send content. Status Code: {response.status_code}"
                )

        except Exception as e:
            if DEBUG:
                print(f"Debug: Error in action method: {str(e)}")
            if __event_emitter__:
                await __event_emitter__(
                    self.status_object(f"Error: {str(e)}", status="error", done=True)
                )

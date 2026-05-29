import os

import gradio as gr


APP_BASE_URL_PATH = os.getenv("APP_BASE_URL_PATH", "").rstrip("/")
APP_PORT = int(os.getenv("APP_PORT", "7860"))
ACCOUNT_VAR = os.getenv("LOAD_TEST_ACCOUNT_VAR", "")
OVERRIDE_VAR = os.getenv("LOAD_TEST_OVERRIDE_VAR", "")


def respond(message: str) -> str:
    return f"You said: {message}"


with gr.Blocks(title="Gradio on Hopsworks") as demo:
    gr.Markdown("# Gradio on Hopsworks")
    gr.Markdown("This app is proxy-aware and works behind the Hopsworks app URL.")
    gr.Markdown(f"Base path: `{APP_BASE_URL_PATH or '/'}`")
    gr.HTML(
        f"""
        <div>
          <p><strong>LOAD_TEST_ACCOUNT_VAR</strong>={ACCOUNT_VAR}</p>
          <p><strong>LOAD_TEST_OVERRIDE_VAR</strong>={OVERRIDE_VAR}</p>
        </div>
        """
    )
    message = gr.Textbox(label="Message")
    reply = gr.Textbox(label="Reply")
    button = gr.Button("Submit")
    button.click(respond, inputs=message, outputs=reply)


demo.launch(
    server_name="0.0.0.0",
    server_port=APP_PORT,
    root_path=APP_BASE_URL_PATH or None,
)

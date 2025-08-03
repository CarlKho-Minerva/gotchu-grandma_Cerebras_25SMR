LiveKit Docs › Integration guides › Large language models (LLM) › Cerebras

---

# Cerebras LLM integration guide

> How to use the Cerebras inference with LiveKit Agents.

## Overview

[Cerebras](https://www.cerebras.net/) provides access to Llama 3.1 and 3.3 models through their inference API. These models are multilingual and text-only, making them suitable for a variety of agent applications.

## Usage

Install the OpenAI plugin to add Cerebras support:

```shell
pip install "livekit-agents[openai]~=1.0"

```

Set the following environment variable in your `.env` file:

```shell
CEREBRAS_API_KEY=<your-cerebras-api-key>

```

Create a Cerebras LLM using the `with_cerebras` method:

```python
from livekit.plugins import openai

session = AgentSession(
    llm=openai.LLM.with_cerebras(
        model="llama3.1-8b",
        temperature=0.7
    ),
    # ... tts, stt, vad, turn_detection, etc.
)

```

## Parameters

This section describes some of the available parameters. See the [plugin reference](https://docs.livekit.io/reference/python/v1/livekit/plugins/openai/index.html.md#livekit.plugins.openai.LLM.with_cerebras) for a complete list of all available parameters.

- **`model`** _(str | CerebrasChatModels)_ (optional) - Default: `llama3.1-8b`: Model to use for inference. To learn more, see [supported models](https://inference-docs.cerebras.ai/api-reference/chat-completions#param-model).

- **`temperature`** _(float)_ (optional) - Default: `1.0`: A measure of randomness in output. A lower value results in more predictable output, while a higher value results in more creative output.

Valid values are between `0` and `1.5`. To learn more, see the [Cerebras documentation](https://inference-docs.cerebras.ai/api-reference/chat-completions#param-temperature).

- **`parallel_tool_calls`** _(bool)_ (optional): Set to true to parallelize tool calls.

- **`tool_choice`** _(ToolChoice | Literal['auto', 'required', 'none'])_ (optional) - Default: `auto`: Specifies whether to use tools during response generation.

## Links

The following links provide more information about the Cerebras LLM integration.

- **[Python package](https://pypi.org/project/livekit-plugins-openai/)**: The `livekit-plugins-openai` package on PyPI.

- **[Plugin reference](https://docs.livekit.run/reference/python/v1/livekit/plugins/openai/index.html#livekit.plugins.openai.LLM.with_cerebras)**: Reference for the `with_cerebras` method of the OpenAI LLM plugin.

- **[GitHub repo](https://github.com/livekit/agents/tree/main/livekit-plugins/livekit-plugins-openai)**: View the source or contribute to the LiveKit OpenAI LLM plugin.

- **[Cerebras docs](https://inference-docs.cerebras.ai/)**: Cerebras inference docs.

- **[Voice AI quickstart](https://docs.livekit.io/agents/start/voice-ai.md)**: Get started with LiveKit Agents and Cerebras.

---

This document was rendered at 2025-08-03T03:16:54.138Z.
For the latest version of this document, see [https://docs.livekit.io/agents/integrations/llm/cerebras.md](https://docs.livekit.io/agents/integrations/llm/cerebras.md).

To explore all LiveKit documentation, see [llms.txt](https://docs.livekit.io/llms.txt).

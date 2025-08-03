api key csk-m95fkpmkcth8wvwyft9ydhrfe2chth5cr893x2n23dptxf3m

# Python
# Cerebras Python API library

[![PyPI version](https://img.shields.io/pypi/v/cerebras_cloud_sdk.svg)](https://pypi.org/project/cerebras_cloud_sdk/)

The Cerebras Python library provides convenient access to the Cerebras REST API from any Python 3.8+
application. The library includes type definitions for all request params and response fields,
and offers both synchronous and asynchronous clients powered by [httpx](https://github.com/encode/httpx).

It is generated with [Stainless](https://www.stainless.com/).

## About Cerebras

At Cerebras, we've developed the world's largest and fastest AI processor, the Wafer-Scale Engine-3 (WSE-3). The Cerebras CS-3 system, powered by the WSE-3, represents a new class of AI supercomputer that sets the standard for generative AI training and inference with unparalleled performance and scalability.

With Cerebras as your inference provider, you can:
- Achieve unprecedented speed for AI inference workloads
- Build commercially with high throughput
- Effortlessly scale your AI workloads with our seamless clustering technology

Our CS-3 systems can be quickly and easily clustered to create the largest AI supercomputers in the world, making it simple to place and run the largest models. Leading corporations, research institutions, and governments are already using Cerebras solutions to develop proprietary models and train popular open-source models.

Want to experience the power of Cerebras? Check out our [website](https://cerebras.net) for more resources and explore options for accessing our technology through the Cerebras Cloud or on-premise deployments!

> [!NOTE]
> This SDK has a mechanism that sends a few requests to `/v1/tcp_warming` upon construction to reduce the TTFT. If this behaviour is not desired, set `warm_tcp_connection=False` in the constructor.
>
> If you are repeatedly reconstructing the SDK instance it will lead to poor performance. It is recommended that you construct the SDK once and reuse the instance if possible.

## Documentation

The REST API documentation can be found on [inference-docs.cerebras.ai](https://inference-docs.cerebras.ai). The full API of this library can be found in [api.md](api.md).

## Installation
```
pip install cerebras_cloud_sdk
```

## API Key
Get an API Key from [cloud.cerebras.ai](https://cloud.cerebras.ai/) and add it to your environment variables:
```
export CEREBRAS_API_KEY="your-api-key-here"
```

## Usage

The full API of this library can be found in [api.md](api.md).

### Chat Completion
<!-- RUN TEST: ChatStandard -->
```python
import os
from cerebras.cloud.sdk import Cerebras

client = Cerebras(
    api_key=os.environ.get("CEREBRAS_API_KEY"),  # This is the default and can be omitted
)

chat_completion = client.chat.completions.create(
    messages=[
        {
            "role": "user",
            "content": "Why is fast inference important?",
        }
    ],
    model="llama3.1-8b",
)

print(chat_completion)
```

### Text Completion
<!-- RUN TEST: TextStandard -->
```python
import os
from cerebras.cloud.sdk import Cerebras

client = Cerebras(
    api_key=os.environ.get("CEREBRAS_API_KEY"),  # This is the default and can be omitted
)

completion = client.completions.create(
    prompt="It was a dark and stormy ",
    max_tokens=100,
    model="llama3.1-8b",
)

print(completion)
```


While you can provide an `api_key` keyword argument,
we recommend using [python-dotenv](https://pypi.org/project/python-dotenv/)
to add `CEREBRAS_API_KEY="My API Key"` to your `.env` file
so that your API Key is not stored in source control.

## Async usage

Simply import `AsyncCerebras` instead of `Cerebras` and use `await` with each API call:

<!-- RUN TEST: ChatAsync -->
```python
import os
import asyncio
from cerebras.cloud.sdk import AsyncCerebras

client = AsyncCerebras(
    api_key=os.environ.get("CEREBRAS_API_KEY"),  # This is the default and can be omitted
)


async def main() -> None:
    chat_completion = await client.chat.completions.create(
        messages=[
            {
                "role": "user",
                "content": "Why is fast inference important?",
            }
        ],
        model="llama3.1-8b",
    )
    print(chat_completion)


asyncio.run(main())
```

Functionality between the synchronous and asynchronous clients is otherwise identical.

## Streaming responses

We provide support for streaming responses using Server Side Events (SSE).

Note that when streaming, `usage` and `time_info` will be information will only be included in the final chunk.

### Chat Completion
<!-- RUN TEST: ChatStreaming -->
```python
import os
from cerebras.cloud.sdk import Cerebras

client = Cerebras(
    # This is the default and can be omitted
    api_key=os.environ.get("CEREBRAS_API_KEY"),
)

stream = client.chat.completions.create(
    messages=[
        {
            "role": "user",
            "content": "Why is fast inference important?",
        }
    ],
    model="llama3.1-8b",
    stream=True,
)

for chunk in stream:
    print(chunk.choices[0].delta.content or "", end="")
```

The async client uses the exact same interface.

<!-- RUN TEST: ChatAsyncStreaming -->
```python
import os
import asyncio
from cerebras.cloud.sdk import AsyncCerebras

client = AsyncCerebras(
    # This is the default and can be omitted
    api_key=os.environ.get("CEREBRAS_API_KEY"),
)


async def main() -> None:
    stream = await client.chat.completions.create(
        messages=[
            {
                "role": "user",
                "content": "Why is fast inference important?",
            }
        ],
        model="llama3.1-8b",
        stream=True,
    )
    async for chunk in stream:
        print(chunk.choices[0].delta.content or "", end="")


asyncio.run(main())
```

### Text Completion
<!-- RUN TEST: TextStreaming -->
```python
import os
from cerebras.cloud.sdk import Cerebras

client = Cerebras(
    # This is the default and can be omitted
    api_key=os.environ.get("CEREBRAS_API_KEY"),
)

stream = client.completions.create(
    prompt="It was a dark and stormy ",
    max_tokens=100,
    model="llama3.1-8b",
    stream=True,
)

for chunk in stream:
    print(chunk.choices[0].text or "", end="")
```


## Using types

Nested request parameters are [TypedDicts](https://docs.python.org/3/library/typing.html#typing.TypedDict). Responses are [Pydantic models](https://docs.pydantic.dev) which also provide helper methods for things like:

- Serializing back into JSON, `model.to_json()`
- Converting to a dictionary, `model.to_dict()`

Typed requests and responses provide autocomplete and documentation within your editor. If you would like to see type errors in VS Code to help catch bugs earlier, set `python.analysis.typeCheckingMode` to `basic`.

## Nested params

Nested parameters are dictionaries, typed using `TypedDict`, for example:

```python
from cerebras.cloud.sdk import Cerebras

client = Cerebras()

chat_completion = client.chat.completions.create(
    messages=[
        {
            "content": "content",
            "role": "system",
        }
    ],
    model="model",
    stream_options={"include_usage": True},
)
print(chat_completion.stream_options)
```

## Handling errors

When the library is unable to connect to the API (for example, due to network connection problems or a timeout), a subclass of `cerebras.cloud.sdk.APIConnectionError` is raised.

When the API returns a non-success status code (that is, 4xx or 5xx
response), a subclass of `cerebras.cloud.sdk.APIStatusError` is raised, containing `status_code` and `response` properties.

All errors inherit from `cerebras.cloud.sdk.APIError`.

<!-- RUN TEST: Error -->
```python
import cerebras.cloud.sdk
from cerebras.cloud.sdk import Cerebras

client = Cerebras()

try:
    client.chat.completions.create(
        messages=[
            {
                "role": "user",
                "content": "This should cause an error!",
            }
        ],
        model="some-model-that-doesnt-exist",
    )
except cerebras.cloud.sdk.APIConnectionError as e:
    print("The server could not be reached")
    print(e.__cause__)  # an underlying Exception, likely raised within httpx.
except cerebras.cloud.sdk.RateLimitError as e:
    print("A 429 status code was received; we should back off a bit.")
except cerebras.cloud.sdk.APIStatusError as e:
    print("Another non-200-range status code was received")
    print(e.status_code)
    print(e.response)
```

Error codes are as follows:

| Status Code | Error Type                 |
| ----------- | -------------------------- |
| 400         | `BadRequestError`          |
| 401         | `AuthenticationError`      |
| 403         | `PermissionDeniedError`    |
| 404         | `NotFoundError`            |
| 422         | `UnprocessableEntityError` |
| 429         | `RateLimitError`           |
| >=500       | `InternalServerError`      |
| N/A         | `APIConnectionError`       |

### Retries

Certain errors are automatically retried 2 times by default, with a short exponential backoff.
Connection errors (for example, due to a network connectivity problem), 408 Request Timeout, 409 Conflict,
429 Rate Limit, and >=500 Internal errors are all retried by default.

You can use the `max_retries` option to configure or disable retry settings:

<!-- RUN TEST: Retries -->
```python
from cerebras.cloud.sdk import Cerebras

# Configure the default for all requests:
client = Cerebras(
    # default is 2
    max_retries=0,
)

# Or, configure per-request:
client.with_options(max_retries=5).chat.completions.create(
    messages=[
        {
            "role": "user",
            "content": "Why is fast inference important?",
        }
    ],
    model="llama3.1-8b",
)
```

### Timeouts

By default requests time out after 1 minute. You can configure this with a `timeout` option,
which accepts a float or an [`httpx.Timeout`](https://www.python-httpx.org/advanced/#fine-tuning-the-configuration) object:

<!-- RUN TEST: Timeout -->
```python
from cerebras.cloud.sdk import Cerebras
import httpx

# Configure the default for all requests:
client = Cerebras(
    # 20 seconds (default is 1 minute)
    timeout=20.0,
)

# More granular control:
client = Cerebras(
    timeout=httpx.Timeout(60.0, read=5.0, write=10.0, connect=2.0),
)

# Override per-request:
client.with_options(timeout=5.0).chat.completions.create(
    messages=[
        {
            "role": "user",
            "content": "Why is fast inference important?",
        }
    ],
    model="llama3.1-8b",
)
```

On timeout, an `APITimeoutError` is thrown.

Note that requests that time out are [retried twice by default](#retries).

## Advanced

### Logging

We use the standard library [`logging`](https://docs.python.org/3/library/logging.html) module.

You can enable logging by setting the environment variable `CEREBRAS_LOG` to `info`.

```shell
$ export CEREBRAS_LOG=info
```

Or to `debug` for more verbose logging.

### How to tell whether `None` means `null` or missing

In an API response, a field may be explicitly `null`, or missing entirely; in either case, its value is `None` in this library. You can differentiate the two cases with `.model_fields_set`:

```py
if response.my_field is None:
  if 'my_field' not in response.model_fields_set:
    print('Got json like {}, without a "my_field" key present at all.')
  else:
    print('Got json like {"my_field": null}.')
```

### Accessing raw response data (e.g. headers)

The "raw" Response object can be accessed by prefixing `.with_raw_response.` to any HTTP method call, e.g.,

<!-- RUN TEST: Advanced -->
```py
from cerebras.cloud.sdk import Cerebras

client = Cerebras()
response = client.chat.completions.with_raw_response.create(
    messages=[{
        "role": "user",
        "content": "Why is fast inference important?",
    }],
    model="llama3.1-8b",
)
print(response.headers.get('X-My-Header'))

completion = response.parse()  # get the object that `chat.completions.create()` would have returned
print(completion)
```

These methods return an [`APIResponse`](https://github.com/Cerebras/cerebras-cloud-sdk-python/tree/main/src/cerebras/cloud/sdk/_response.py) object.

The async client returns an [`AsyncAPIResponse`](https://github.com/Cerebras/cerebras-cloud-sdk-python/tree/main/src/cerebras/cloud/sdk/_response.py) with the same structure, the only difference being `await`able methods for reading the response content.

<!--
#### `.with_streaming_response`

The above interface eagerly reads the full response body when you make the request, which may not always be what you want.

To stream the response body, use `.with_streaming_response` instead, which requires a context manager and only reads the response body once you call `.read()`, `.text()`, `.json()`, `.iter_bytes()`, `.iter_text()`, `.iter_lines()` or `.parse()`. In the async client, these are async methods.

```python
with client.chat.completions.with_streaming_response.create(
    messages=[
        {
            "role": "user",
            "content": "Why is fast inference important?",
        }
    ],
    model="llama3.1-8b",
) as response:
    print(response.headers.get("X-My-Header"))

    for line in response.iter_lines():
        print(line)
```

The context manager is required so that the response will reliably be closed.
-->

### Making custom/undocumented requests

This library is typed for convenient access to the documented API.

If you need to access undocumented endpoints, params, or response properties, the library can still be used.

#### Undocumented endpoints

To make requests to undocumented endpoints, you can make requests using `client.get`, `client.post`, and other
http verbs. Options on the client will be respected (such as retries) when making this request.

```py
import httpx

response = client.post(
    "/foo",
    cast_to=httpx.Response,
    body={"my_param": True},
)

print(response.headers.get("x-foo"))
```

#### Undocumented request params

If you want to explicitly send an extra param, you can do so with the `extra_query`, `extra_body`, and `extra_headers` request
options.

#### Undocumented response properties

To access undocumented response properties, you can access the extra fields like `response.unknown_prop`. You
can also get all the extra fields on the Pydantic model as a dict with
[`response.model_extra`](https://docs.pydantic.dev/latest/api/base_model/#pydantic.BaseModel.model_extra).

### Configuring the HTTP client

You can directly override the [httpx client](https://www.python-httpx.org/api/#client) to customize it for your use case, including:

- Support for [proxies](https://www.python-httpx.org/advanced/proxies/)
- Custom [transports](https://www.python-httpx.org/advanced/transports/)
- Additional [advanced](https://www.python-httpx.org/advanced/clients/) functionality

```python
import httpx
from cerebras.cloud.sdk import Cerebras, DefaultHttpxClient

client = Cerebras(
    # Or use the `CEREBRAS_BASE_URL` env var
    base_url="http://my.test.server.example.com:8083",
    http_client=DefaultHttpxClient(
        proxy="http://my.test.proxy.example.com",
        transport=httpx.HTTPTransport(local_address="0.0.0.0"),
    ),
)
```

You can also customize the client on a per-request basis by using `with_options()`:

```python
client.with_options(http_client=DefaultHttpxClient(...))
```

### Managing HTTP resources

By default the library closes underlying HTTP connections whenever the client is [garbage collected](https://docs.python.org/3/reference/datamodel.html#object.__del__). You can manually close the client using the `.close()` method if desired, or with a context manager that closes when exiting.

```py
from cerebras.cloud.sdk import Cerebras

with Cerebras() as client:
  # make requests here
  ...

# HTTP client is now closed
```

## Versioning

This package generally follows [SemVer](https://semver.org/spec/v2.0.0.html) conventions, though certain backwards-incompatible changes may be released as minor versions:

1. Changes that only affect static types, without breaking runtime behavior.
2. Changes to library internals which are technically public but not intended or documented for external use. _(Please open a GitHub issue to let us know if you are relying on such internals.)_
3. Changes that we do not expect to impact the vast majority of users in practice.

We take backwards-compatibility seriously and work hard to ensure you can rely on a smooth upgrade experience.

We are keen for your feedback; please open an [issue](https://www.github.com/Cerebras/cerebras-cloud-sdk-python/issues) with questions, bugs, or suggestions.

### Determining the installed version

If you've upgraded to the latest version but aren't seeing any new features you were expecting then your python environment is likely still using an older version.

You can determine the version that is being used at runtime with:

```py
import cerebras.cloud.sdk
print(cerebras.cloud.sdk.__version__)
```

## Requirements

Python 3.8 or higher.

## Contributing

See [the contributing documentation](./CONTRIBUTING.md).

# Javascript
# Cerebras Node API Library

[![NPM version](https://img.shields.io/npm/v/@cerebras/cerebras_cloud_sdk.svg)](https://npmjs.org/package/@cerebras/cerebras_cloud_sdk) ![npm bundle size](https://img.shields.io/bundlephobia/minzip/@cerebras/cerebras_cloud_sdk)

This library provides convenient access to the Cerebras REST API from server-side TypeScript or JavaScript.

The REST API documentation can be found on [inference-docs.cerebras.ai](https://inference-docs.cerebras.ai). The full API of this library can be found in [api.md](api.md).

It is generated with [Stainless](https://www.stainless.com/).

> [!NOTE]
> This SDK has a mechanism that sends a few requests to `/v1/tcp_warming` upon construction to reduce the TTFT. If this behaviour is not desired, set `warmTCPConnection=false` in the constructor.
>
> If you are repeatedly reconstructing the SDK instance it will lead to poor performance. It is recommended that you construct the SDK once and reuse the instance if possible.

## About Cerebras

At Cerebras, we've developed the world's largest and fastest AI processor, the Wafer-Scale Engine-3 (WSE-3). The Cerebras CS-3 system, powered by the WSE-3, represents a new class of AI supercomputer that sets the standard for generative AI training and inference with unparalleled performance and scalability.

With Cerebras as your inference provider, you can:
- Achieve unprecedented speed for AI inference workloads
- Build commercially with high throughput
- Effortlessly scale your AI workloads with our seamless clustering technology

Our CS-3 systems can be quickly and easily clustered to create the largest AI supercomputers in the world, making it simple to place and run the largest models. Leading corporations, research institutions, and governments are already using Cerebras solutions to develop proprietary models and train popular open-source models.

Want to experience the power of Cerebras? Check out our [website](https://cerebras.net) for more resources and explore options for accessing our technology through the Cerebras Cloud or on-premise deployments!

## Installation
```
npm install @cerebras/cerebras_cloud_sdk
```

## API Key
Get an API Key from [cloud.cerebras.ai](https://cloud.cerebras.ai/) and add it to your environment variables:
```
export CEREBRAS_API_KEY="your-api-key-here"
```

## Usage

The full API of this library can be found in [api.md](api.md).

### Chat Completion
<!-- RUN TEST: ChatStandard -->
```ts
import Cerebras from '@cerebras/cerebras_cloud_sdk';

const client = new Cerebras({
  apiKey: process.env['CEREBRAS_API_KEY'], // This is the default and can be omitted
});

async function main() {
  const chatCompletion = await client.chat.completions.create({
    messages: [{ role: 'user', content: 'Why is fast inference important?' }],
    model: 'llama3.1-8b',
  });

  console.log(chatCompletion?.choices[0]?.message);
}

main();
```

### Text Completion
<!-- RUN TEST: TextStandard -->
```ts
import Cerebras from '@cerebras/cerebras_cloud_sdk';

const client = new Cerebras({
  apiKey: process.env['CEREBRAS_API_KEY'], // This is the default and can be omitted
});

async function main() {
  const completion = await client.completions.create({
    prompt: "It was a dark and stormy ",
    model: 'llama3.1-8b',
  });

  console.log(completion?.choices[0]?.text);
}

main();
```

## Streaming responses

We provide support for streaming responses using Server Sent Events (SSE).

Note that when streaming, `usage` and `time_info` will be information will only be included in the final chunk.

### Chat Completion
<!-- RUN TEST: ChatStreaming -->
```ts
import Cerebras from '@cerebras/cerebras_cloud_sdk';

const client = new Cerebras({
  apiKey: process.env['CEREBRAS_API_KEY'], // This is the default and can be omitted
});

async function main() {
  const stream = await client.chat.completions.create({
    messages: [{ role: 'user', content: 'Why is fast inference important?' }],
    model: 'llama3.1-8b',
    stream: true,
  });
  for await (const chunk of stream) {
    process.stdout.write(chunk.choices[0]?.delta?.content || '');
  }
}

main();
```

### Text Completion
<!-- RUN TEST: TextStreaming -->
```ts
import Cerebras from '@cerebras/cerebras_cloud_sdk';

const client = new Cerebras({
  apiKey: process.env['CEREBRAS_API_KEY'], // This is the default and can be omitted
});

async function main() {
  const stream = await client.completions.create({
    prompt: "It was a dark and stormy ",
    model: 'llama3.1-8b',
    max_tokens: 10,
    stream: true,
  });
  for await (const chunk of stream) {
    process.stdout.write(chunk.choices[0]?.text || '');
  }
}

main();
```

If you need to cancel a stream, you can `break` from the loop
or call `stream.controller.abort()`.

### Request & Response types

This library includes TypeScript definitions for all request params and response fields. You may import and use them like so:

<!-- RUN TEST: Types -->
```ts
import Cerebras from '@cerebras/cerebras_cloud_sdk';

const client = new Cerebras({
  apiKey: process.env['CEREBRAS_API_KEY'], // This is the default and can be omitted
});

async function main() {
  const params: Cerebras.Chat.ChatCompletionCreateParams = {
    messages: [{ role: 'user', content: 'Why is fast inference important?' }],
    model: 'llama3.1-8b',
  };
  const chatCompletion: Cerebras.Chat.ChatCompletion = await client.chat.completions.create(params);
}

main();
```

Documentation for each method, request param, and response field are available in docstrings and will appear on hover in most modern editors.

## Handling errors

When the library is unable to connect to the API,
or if the API returns a non-success status code (i.e., 4xx or 5xx response),
a subclass of `APIError` will be thrown:

<!-- RUN TEST: Error -->
```ts
import Cerebras from '@cerebras/cerebras_cloud_sdk';

const client = new Cerebras({
  apiKey: process.env['CEREBRAS_API_KEY'], // This is the default and can be omitted
});

async function main() {
  const chatCompletion = await client.chat.completions
    .create({
      messages: [{ role: 'user', content: 'This should cause an error!' }],
      model: 'some-model-that-doesnt-exist' as any, // Ask TS to ignore the obviously invalid model name... Do not do this!
    })
    .catch(async (err) => {
      if (err instanceof Cerebras.APIError) {
        console.log(err.status); // 400
        console.log(err.name); // BadRequestError
        console.log(err.headers); // {server: 'nginx', ...}
        console.log(err); // Full exception
      } else {
        throw err;
      }
    });
}

main();
```

Error codes are as follows:

| Status Code | Error Type                 |
| ----------- | -------------------------- |
| 400         | `BadRequestError`          |
| 401         | `AuthenticationError`      |
| 403         | `PermissionDeniedError`    |
| 404         | `NotFoundError`            |
| 422         | `UnprocessableEntityError` |
| 429         | `RateLimitError`           |
| >=500       | `InternalServerError`      |
| N/A         | `APIConnectionError`       |

### Retries

Certain errors will be automatically retried 2 times by default, with a short exponential backoff.
Connection errors (for example, due to a network connectivity problem), 408 Request Timeout, 409 Conflict,
429 Rate Limit, and >=500 Internal errors will all be retried by default.

You can use the `maxRetries` option to configure or disable this:

<!-- RUN TEST: Retries -->
```js
import Cerebras from '@cerebras/cerebras_cloud_sdk';

// Configure the default for all requests:
const client = new Cerebras({
  maxRetries: 0, // default is 2
});

// Or, configure per-request:
await client.chat.completions.create({ messages: [{ role: 'user', content: 'Why is fast inference important?' }], model: 'llama3.1-8b' }, {
  maxRetries: 5,
});
```

### Timeouts

Requests time out after 1 minute by default. You can configure this with a `timeout` option:

<!-- RUN TEST: Timeout -->
```ts
import Cerebras from '@cerebras/cerebras_cloud_sdk';

// Configure the default for all requests:
const client = new Cerebras({
  timeout: 20 * 1000, // 20 seconds (default is 1 minute)
});

// Override per-request:
await client.chat.completions.create({ messages: [{ role: 'user', content: 'Why is fast inference important?' }], model: 'llama3.1-8b' }, {
  timeout: 5 * 1000,
});
```

On timeout, an `APIConnectionTimeoutError` is thrown.

Note that requests which time out will be [retried twice by default](#retries).

## Advanced Usage

### Accessing raw Response data (e.g., headers)

The "raw" `Response` returned by `fetch()` can be accessed through the `.asResponse()` method on the `APIPromise` type that all methods return.

You can also use the `.withResponse()` method to get the raw `Response` along with the parsed data.

<!-- RUN TEST: Advanced -->
```ts
import Cerebras from '@cerebras/cerebras_cloud_sdk';

const client = new Cerebras();

const response = await client.chat.completions
  .create({ messages: [{ role: 'user', content: 'Why is fast inference important?' }], model: 'llama3.1-8b' })
  .asResponse();
console.log(response.headers.get('X-My-Header'));
console.log(response.statusText); // access the underlying Response object

const { data: chatCompletion, response: raw } = await client.chat.completions
  .create({ messages: [{ role: 'user', content: 'Why is fast inference important?' }], model: 'llama3.1-8b' })
  .withResponse();
console.log(raw.headers.get('X-My-Header'));
console.log(chatCompletion);
```

### Making custom/undocumented requests

This library is typed for convenient access to the documented API. If you need to access undocumented
endpoints, params, or response properties, the library can still be used.

#### Undocumented endpoints

To make requests to undocumented endpoints, you can use `client.get`, `client.post`, and other HTTP verbs.
Options on the client, such as retries, will be respected when making these requests.

```ts
await client.post('/some/path', {
  body: { some_prop: 'foo' },
  query: { some_query_arg: 'bar' },
});
```

#### Undocumented request params

To make requests using undocumented parameters, you may use `// @ts-expect-error` on the undocumented
parameter. This library doesn't validate at runtime that the request matches the type, so any extra values you
send will be sent as-is.

```ts
client.foo.create({
  foo: 'my_param',
  bar: 12,
  // @ts-expect-error baz is not yet public
  baz: 'undocumented option',
});
```

For requests with the `GET` verb, any extra params will be in the query, all other requests will send the
extra param in the body.

If you want to explicitly send an extra argument, you can do so with the `query`, `body`, and `headers` request
options.

#### Undocumented response properties

To access undocumented response properties, you may access the response object with `// @ts-expect-error` on
the response object, or cast the response object to the requisite type. Like the request params, we do not
validate or strip extra properties from the response from the API.

### Customizing the fetch client

By default, this library uses `node-fetch` in Node, and expects a global `fetch` function in other environments.

If you would prefer to use a global, web-standards-compliant `fetch` function even in a Node environment,
(for example, if you are running Node with `--experimental-fetch` or using NextJS which polyfills with `undici`),
add the following import before your first import `from "Cerebras"`:

```ts
// Tell TypeScript and the package to use the global web fetch instead of node-fetch.
// Note, despite the name, this does not add any polyfills, but expects them to be provided if needed.
import '@cerebras/cerebras_cloud_sdk/shims/web';
import Cerebras from '@cerebras/cerebras_cloud_sdk';
```

To do the inverse, add `import "@cerebras/cerebras_cloud_sdk/shims/node"` (which does import polyfills).
This can also be useful if you are getting the wrong TypeScript types for `Response` ([more details](https://github.com/Cerebras/cerebras-cloud-sdk-node/tree/main/src/_shims#readme)).

### Logging and middleware

You may also provide a custom `fetch` function when instantiating the client,
which can be used to inspect or alter the `Request` or `Response` before/after each request:

```ts
import { fetch } from 'undici'; // as one example
import Cerebras from '@cerebras/cerebras_cloud_sdk';

const client = new Cerebras({
  fetch: async (url: RequestInfo, init?: RequestInit): Promise<Response> => {
    console.log('About to make a request', url, init);
    const response = await fetch(url, init);
    console.log('Got response', response);
    return response;
  },
});
```

Note that if given a `DEBUG=true` environment variable, this library will log all requests and responses automatically.
This is intended for debugging purposes only and may change in the future without notice.

### Configuring an HTTP(S) Agent (e.g., for proxies)

By default, this library uses a stable agent for all http/https requests to reuse TCP connections, eliminating many TCP & TLS handshakes and shaving around 100ms off most requests.

If you would like to disable or customize this behavior, for example to use the API behind a proxy, you can pass an `httpAgent` which is used for all requests (be they http or https), for example:

<!-- prettier-ignore -->
```ts
import http from 'http';
import { HttpsProxyAgent } from 'https-proxy-agent';

// Configure the default for all requests:
const client = new Cerebras({
  httpAgent: new HttpsProxyAgent(process.env.PROXY_URL),
});

// Override per-request:
await client.chat.completions.create(
  { messages: [{ role: 'user', content: 'Why is fast inference important?' }], model: 'llama3.1-8b' },
  {
    httpAgent: new http.Agent({ keepAlive: false }),
  },
);
```

## Semantic versioning

This package generally follows [SemVer](https://semver.org/spec/v2.0.0.html) conventions, though certain backwards-incompatible changes may be released as minor versions:

1. Changes that only affect static types, without breaking runtime behavior.
2. Changes to library internals which are technically public but not intended or documented for external use. _(Please open a GitHub issue to let us know if you are relying on such internals.)_
3. Changes that we do not expect to impact the vast majority of users in practice.

We take backwards-compatibility seriously and work hard to ensure you can rely on a smooth upgrade experience.

We are keen for your feedback; please open an [issue](https://www.github.com/Cerebras/cerebras-cloud-sdk-node/issues) with questions, bugs, or suggestions.

## Requirements

TypeScript >= 4.5 is supported.

The following runtimes are supported:

- Web browsers (Up-to-date Chrome, Firefox, Safari, Edge, and more)
- Node.js 18 LTS or later ([non-EOL](https://endoflife.date/nodejs)) versions.
- Deno v1.28.0 or higher.
- Bun 1.0 or later.
- Cloudflare Workers.
- Vercel Edge Runtime.
- Jest 28 or greater with the `"node"` environment (`"jsdom"` is not supported at this time).
- Nitro v2.6 or greater.

Note that React Native is not supported at this time.

If you are interested in other runtime environments, please open or upvote an issue on GitHub.

## Contributing

See [the contributing documentation](./CONTRIBUTING.md).


# Supported Models

## Production Models

Production models are are fully supported offerings intended for use in production environments.

| Model Name                             | Model ID                         | Parameters  | Speed (tokens/s) |
| :------------------------------------- | :------------------------------- | :---------- | :--------------- |
| [Llama 4 Scout](/models/llama-4-scout) | `llama-4-scout-17b-16e-instruct` | 109 billion | \~2600           |
| [Llama 3.1 8B](/models/llama-31-8b)    | `llama3.1-8b`                    | 8 billion   | \~2200           |
| [Llama 3.3 70B](/models/llama-33-70b)  | `llama-3.3-70b`                  | 70 billion  | \~2100           |
| [Qwen 3 32B](/models/qwen-3-32b)       | `qwen-3-32b`                     | 32 billion  | \~2600           |

## Preview Models

Preview models are hosted on Cerebras with full accuracy and performance. Please note that these preview models are intended for evaluation purposes only and should not be used in production, as they may be discontinued with short notice.

| Model Name                                           | Model ID                             | Parameters  | Speed (tokens/s) |
| :--------------------------------------------------- | :----------------------------------- | :---------- | :--------------- |
| [Llama 4 Maverick](/models/llama-4-maverick)         | `llama-4-maverick-17b-128e-instruct` | 17 billion  | \~1500           |
| [Qwen 3 235B Instruct](/models/qwen-3-235b-2507)     | `qwen-3-235b-a22b-instruct-2507`     | 235 billion | \~1400           |
| [Qwen 3 235B Thinking](/models/qwen-3-235b-thinking) | `qwen-3-235b-a22b-thinking-2507`     | 235 billion | \~1700           |
| [Qwen 3 480B Coder](/models/qwen-3-480b)             | `qwen-3-coder-480b`                  | 480 billion | \~2000           |
| DeepSeek R1 Distill Llama 70B\*                      | `deepseek-r1-distill-llama-70b`      | 70 billion  | \~1700           |

<Warning>\* DeepSeek R1 Distill Llama 70B is to be deprecated on August 12, 2025. We recommend migrating to [Qwen 3 32B ](/models/qwen-3-32b).</Warning>

# Enable Llama 2 AI in Baserow

In order to activate the AI features in Baserow you must first download the Llama 2-7B
chat model into this folder, and set the `BASEROW_LLAMA_AI_ENABLED` environment variable
to `true`.

```
wget https://huggingface.co/TheBloke/Llama-2-7B-chat-GGML/resolve/main/llama-2-7b-chat.ggmlv3.q4_0.bin
```

## Verification

After starting the development environment, you can verify if the models work correctly
by visiting http://localhost:9000/v1/models.

## Alternative models

### Llama 2-13B chat

Download the following model into this folder, and set the `BASEROW_LLAMA_MODEL` environment
variable to `/models/llama-2-13b-chat.ggmlv3.q4_0.bin`.

```
wget https://huggingface.co/TheBloke/Llama-2-13B-chat-GGML/resolve/main/llama-2-13b-chat.ggmlv3.q4_0.bin
```

### Llama 2 70B chat

Download the following model into this folder, and set the `BASEROW_LLAMA_MODEL` environment
variable to `/models/llama-2-70b-chat.ggmlv3.q4_0.bin`.

```
wget https://huggingface.co/TheBloke/Llama-2-70B-chat-GGML/resolve/main/llama-2-70b-chat.ggmlv3.q4_0.bin
```

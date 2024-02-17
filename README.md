# Simple-Proxy-Server-in-Python

This project consists of a simple proxy server implemented in Python that intercepts HTTP requests and responses between a client and a server. It features URL filtering, image filtering (with the ability to turn it on or off), and request redirection based on specific criteria.

## Features

- **HTTP Request & Response Handling**: Intercepts and logs HTTP requests and responses, including headers and content.
- **Image Filtering**: Can filter out image content based on file extensions. This feature can be toggled on or off through query parameters in the URL.
- **Request Redirection**: Redirects requests containing specific keywords to predefined URLs.
- **Concurrency Support**: Handles multiple client connections concurrently using threads.

## Implementation Details

The proxy server is implemented in a single Python script (`prx.py`) with the following key functionalities:
- Parsing HTTP headers to apply redirection or filtering based on the request URL.
- Establishing connections with the destination server and relaying requests/responses between the client and the server.
- Filtering image content by intercepting responses with image content types and preventing them from being sent to the client when image filtering is enabled.
- Using threading to manage multiple connections, allowing the proxy to handle simultaneous client requests efficiently.

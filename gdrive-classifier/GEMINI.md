
# Google OAuth API Guidelines

When using `google_auth_oauthlib.flow.InstalledAppFlow` in Python:
- **CSRF Mismatch Pitfall**: Do NOT call `flow.authorization_url()` manually if you intend to use `flow.run_local_server()`. Calling `authorization_url()` generates an OAuth state. `run_local_server()` generates a new state internally. When the browser redirects back, the state doesn't match, causing a `MismatchingStateError` (CSRF Warning).
- **Correct Usage**: Let `run_local_server()` generate the URL. Use the `authorization_prompt_message` argument to print the URL, or subclass `InstalledAppFlow` and override `run_local_server` to intercept the URL and write it to a file.
- **Redirect URI Error**: If `flow.redirect_uri` is not set before generating an authorization URL, Google OAuth rejects the request with a 400 invalid_request error.

# Python Background Tasks

When running Python scripts as asynchronous background tasks:
- **Stdout Buffering**: Python block-buffers stdout when not connected to a terminal. Real-time prompts (like an OAuth URL) will not appear in the log file immediately.
- **Fix**: Either launch the script with `python -u` or explicitly call `sys.stdout.flush()` after printing important prompts.

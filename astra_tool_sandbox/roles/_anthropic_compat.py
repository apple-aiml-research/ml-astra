# For licensing see accompanying LICENSE file.
# Copyright (C) 2026 Apple Inc. All Rights Reserved.
# mypy: disable-error-code="attr-defined,assignment,no-redef,import-not-found"
"""Compatibility shim spanning the anthropic SDK range ``>=0.26,<0.40``.

Older releases (``0.26.x``) exposed tool-use types under
``anthropic.types.beta.tools`` and the create call at
``client.beta.tools.messages.create``. Newer releases (``0.39.x``) removed
that submodule and moved the equivalents to the stable
``anthropic.types`` namespace and ``client.messages.create``.

Both SDKs accept the same create-call signature
(``model, messages, system, tools, max_tokens, temperature, extra_headers``),
so we detect the world once at import time and re-export a single set of
names that the rest of the codebase can use.

The runtime imports below intentionally probe both attribute paths and
are opaque to static typing (mypy sees only whichever SDK is installed
locally, but the intent is to span both). Callers get a plain ``Any``
handle for the shim types and rely on ``isinstance`` at the call sites.
"""

from __future__ import annotations

from typing import Any

# Runtime-detected exports; declared as ``Any`` on purpose so mypy doesn't
# have to reason about which SDK path was taken at import time.
MessageParam: Any
ResponseMessage: Any
TextBlock: Any
TextBlockParam: Any
ToolParam: Any
ToolResultBlockParam: Any
ToolUseBlock: Any

try:
    # New SDK (>=~0.36): stable types at anthropic.types.*
    from anthropic.types import Message as _ResponseMessage
    from anthropic.types import MessageParam as _MessageParam
    from anthropic.types import TextBlock as _TextBlock
    from anthropic.types import TextBlockParam as _TextBlockParam
    from anthropic.types import ToolParam as _ToolParam
    from anthropic.types import ToolResultBlockParam as _ToolResultBlockParam
    from anthropic.types import ToolUseBlock as _ToolUseBlock

    _USE_STABLE_API = True
except ImportError:
    # Old SDK (0.26.x): tool types live under the beta.tools submodule.
    from anthropic.types import TextBlock as _TextBlock
    from anthropic.types import TextBlockParam as _TextBlockParam
    from anthropic.types.beta.tools import ToolParam as _ToolParam
    from anthropic.types.beta.tools import ToolResultBlockParam as _ToolResultBlockParam
    from anthropic.types.beta.tools import ToolsBetaMessage as _ResponseMessage
    from anthropic.types.beta.tools import ToolsBetaMessageParam as _MessageParam
    from anthropic.types.beta.tools import ToolUseBlock as _ToolUseBlock

    _USE_STABLE_API = False


MessageParam = _MessageParam
ResponseMessage = _ResponseMessage
TextBlock = _TextBlock
TextBlockParam = _TextBlockParam
ToolParam = _ToolParam
ToolResultBlockParam = _ToolResultBlockParam
ToolUseBlock = _ToolUseBlock


def messages_create(client: Any, **kwargs: Any) -> Any:
    """Call the SDK's tool-capable ``messages.create`` on either SDK.

    The keyword arguments are identical across both versions; only the
    attribute path on the client differs.
    """
    if _USE_STABLE_API:
        return client.messages.create(**kwargs)
    return client.beta.tools.messages.create(**kwargs)


__all__ = [
    "MessageParam",
    "ResponseMessage",
    "TextBlock",
    "TextBlockParam",
    "ToolParam",
    "ToolResultBlockParam",
    "ToolUseBlock",
    "messages_create",
]

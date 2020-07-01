from vse.core import VSE_MAP_AGENT

from vse.handlers import (
    TestHandler,
    DefaultHandler,
    FindLinesHandler,
    FindLinesParamSchema,
    TestHandlerParams
)

VSE_MAP_AGENT.register_handler('test_handler', TestHandler, TestHandlerParams)
VSE_MAP_AGENT.register_handler('h_find_lines', FindLinesHandler, FindLinesParamSchema)

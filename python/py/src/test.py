import os
import tempfile

tempfile.mkdtemp(dir = "wms")
f = tempfile.mkstemp(suffix='.csv', prefix="sendtoallmessage", dir="wms", text=False)

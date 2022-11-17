from fastapi import Header


async def valid_content_length(content_length: int = Header(..., lt=1_000_000_001)): # only allows file upload of upto 1 GB
    return content_length
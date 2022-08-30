import json
import re


class Sentence:
    def __init__(self, string: str | None) -> None:
        if string is None:
            return
        string = re.sub(r"(?<=\s)\s*|^\s+|\s+$", "", string)

        self.command: re.Match[str] | None | str = re.search(r"^\w+\S", string)
        assert self.command is not None, response(
            status_code=400, message="Bad request"
        )

        self.command = self.command.group()
        self.options: list[str] = re.findall(r"(?<=\s)-+\w+", string)
        self.files: list[str] = re.findall(r"(?<=\s)\w+", string)

    def __str__(self) -> str:
        return f"{self.command} {' '.join(self.options)} {' '.join(self.files)}"


def request(method: str, uri: str) -> str:
    return json.dumps(
        {"http": {"method": method, "uri": uri}},
    )

def response(
    status_code: int,
    message: str,
    content_length: int = 0,
    content_type: str | None = None,
    content: str | None = None,
) -> str:
    if content_length == 0 or content_type is None or content is None:
        return json.dumps(
            {
                "http": {
                    "statusCode": status_code,
                    "message": message,
                    "content-length": content_length,
                },
                #"data": bytes("", "utf-8"),
            }
        )
    return json.dumps(
        {
            "http": {
                "statusCode": status_code,
                "message": message,
                "content-type": content_type,
                "content-length": content_length,
            },
            "data": bytes(content, "utf-8"),
        }
    )

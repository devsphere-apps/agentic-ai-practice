from pydantic import BaseModel, Field
from typing import Literal

class KBLookup(BaseModel):

    category:Literal[
        "Soaking",
        "Order",
        "Complaint"
    ] = Field(
        ...,
        description="Knowledge Base Category"
        )

if __name__ == "__main__":
    lookup = KBLookup(
        category="Order"
    )

import json

print(json.dumps(KBLookup.model_json_schema(),indent=2))
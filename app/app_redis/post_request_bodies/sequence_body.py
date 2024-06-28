from typing import Dict, List

from pydantic import BaseModel


class SequenceFormatBody(BaseModel):
    sequence_dict: Dict[str, int] | List[int] | int = None

# None -> [4]
# {"sequence_dict": 8} -> [5, 6,7,8,9,10,11, 12]
# {"sequence_dict": [3, 5, 7]} -> [[1,2,3], [4,5,6,7,8], [9,10,11,12,13,14,15]]
# {"sequence_dict": {"a": 3, "b": 5} } -> {"a": [1,2,3] , "b": [4,5,6,7,8]}

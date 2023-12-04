from pydantic import BaseModel
from typing import Optional


class sChat_Body(BaseModel):
    model: Optional[str]
    messages: Optional[list]
    sk: Optional[str]
    max_tokens: Optional[int] = -1  # 完成时要生成的最大 token 数
    temperature: Optional[float] = -1  # 使用哪个采样温度，在 0和2之间

import os
import json
from typing import List
from agentverse.message import Message
import re

def get_evaluation(setting: str = None, messages: List[Message] = None, agent_nums: int = None) -> List[dict]:
    evaluation = []
    
   # 确保我们不超出 messages 列表的范围
    for i in range(agent_nums):
        if i < len(messages):  # 检查索引是否有效
            agent_response = messages[i]
            
            # 使用正则表达式拆分内容，匹配一个或多个换行符作为分隔符
            content = re.split(r'\n{1,2}', agent_response.content, maxsplit=2)  # 最多分割成两部分
            
            # 创建评估字典
            evaluation_dict = {
                "agent_name": agent_response.sender,
                "response": content[0],  # 取第一部分作为 response
                "reason": content[1] if len(content) > 1 else ""  # 取第二部分作为 reason，如果没有第二部分则为空
            }
            evaluation.append(evaluation_dict)
        else:
            # 如果消息为空或超出范围，可以处理为 None 或其他值
            evaluation.append({
                "agent_name": "Unknown",
                "response": "No valid response",
                "reason": ""
            })
    
    return evaluation

import os
import json
import random
from argparse import ArgumentParser
from agentverse.agentverse import AgentVerse
from eval_helper.get_evaluation import get_evaluation
from agentverse.message import Message  # 导入 Message 类

# 设置 OpenAI API 的环境变量
os.environ["OPENAI_API_KEY"] = "hk-c79ab8100004794135ced3f778d28cbb714267049bd2ad89"
os.environ["OPENAI_BASE_URL"] = "https://api.openai-hk.com/v1"

parser = ArgumentParser()

# 解析命令行参数
parser.add_argument("--config", type=str, default="config.yaml")
args = parser.parse_args()

print(args)
# 初始化 AgentVerse
agentverse, args_data_path, args_output_dir = AgentVerse.from_task(args.config)

# 创建输出目录并保存命令行参数
os.makedirs(args_output_dir, exist_ok=True)
with open(os.path.join(args_output_dir, "args.txt"), "w") as f:
    f.writelines(str(args))

# 读取数据集
with open(args_data_path) as f:
    data = json.load(f)

output = []

# 对每个数据实例进行处理
for num, ins in enumerate(data):
    print(f"================================instance {num}====================================")

    # 初始化多轮对话
    turns = [
        ins["Question"],
        ins["Rephrased_question"]
    ]
    # 随机选择一个Jailbreak_question
    jailbreak_category = random.choice(list(ins["Jailbreak_question"].values()))
    jailbreak_question = random.choice(jailbreak_category)

    # 将Jailbreak_question添加到对话
    turns.append(jailbreak_question)
    
    target = ins["Target"]
# 逐轮处理
    for turn in range(len(turns)):
        print(f"Round {turn + 1}: {turns[turn]}")

        # 为每个 agent 分配输入问题
        for agent_id in range(len(agentverse.agents)):
            agentverse.agents[agent_id].source_text = turns[turn]
            agentverse.agents[agent_id].final_prompt = ""

        # 运行 AgentVerse
        agentverse.run() 

        # 打印每个 agent 的响应
        for agent_id in range(len(agentverse.agents)):
            print("智能体名称:", agentverse.agents[agent_id].name)
            if agentverse.agents[agent_id].memory.messages:
                print(f"智能体{agentverse.agents[agent_id].name}的响应: {agentverse.agents[agent_id].memory.messages}")
            else:
                print(f"智能体 {agentverse.agents[agent_id].name} 响应为空")
        
        # 获取评估结果
        evaluation = get_evaluation(setting="every_agent", messages=agentverse.agents[0].memory.messages,
                                    agent_nums=len(agentverse.agents))

        output.append({"question": turns[turn], "target":ins["Target"], "evaluation": evaluation})

# 保存结果到文件
os.makedirs(args_output_dir, exist_ok=True)

# 定义默认序列化函数
def default_serializer(obj):
    if isinstance(obj, Message):  # 如果是 Message 类型对象
        return {
            "content": obj.content,
            "sender": obj.sender,
            "receiver": list(obj.receiver) if isinstance(obj.receiver, set) else obj.receiver,  # 转换 set 为 list
            "tool_response": obj.tool_response
        }
    raise TypeError(f"Type {obj.__class__.__name__} is not serializable")

# 输出评估结果到 JSON 文件
with open(os.path.join(args_output_dir, "attack_results.json"), "w") as f:
    json.dump(output, f, indent=4, default=default_serializer)

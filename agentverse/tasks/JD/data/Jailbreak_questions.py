import json

# 读取当前数据集（示例路径）
current_data_file = 'updated_data.json'  # 替换为你的当前数据集文件路径
with open(current_data_file, 'r', encoding='utf-8') as f:
    current_data = json.load(f)

# 读取Jailbreak数据集（示例路径）
jailbreak_data_file = 'agentverse\\tasks\JD\data\Jailbreak\jailbreak_templates.json'  # 替换为你的Jailbreak数据集文件路径
with open(jailbreak_data_file, 'r', encoding='utf-8') as f:
    jailbreak_data = json.load(f)

# 用于生成 Jailbreak_question 的函数
def generate_jailbreak_questions(question, jailbreak_data):
    jailbreak_questions = {}
    for category, prompts in jailbreak_data.items():
        for prompt_data in prompts:
            prompt = prompt_data['prompt']
            jailbreak_question = prompt.replace("[INSERT PROMPT HERE]", question)
            if category not in jailbreak_questions:
                jailbreak_questions[category] = []
            jailbreak_questions[category].append(jailbreak_question)
    return jailbreak_questions

# 为每个数据项添加 Jailbreak_question
for item in current_data:
    question = item.get("Question", "")
    if question:
        jailbreak_questions = generate_jailbreak_questions(question, jailbreak_data)
        item["Jailbreak_question"] = jailbreak_questions

# 将更新后的数据保存为新的JSON文件
output_file = 'updated_with_jailbreak_questions.json'  # 输出文件路径
with open(output_file, 'w', encoding='utf-8') as f:
    json.dump(current_data, f, ensure_ascii=False, indent=4)

print(f"数据已成功更新并保存到 {output_file}")

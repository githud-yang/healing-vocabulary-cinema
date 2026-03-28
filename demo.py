#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
治愈系单词放映机 - 演示脚本
Healing Vocabulary Cinema - Demo Script

一个多智能体协作系统，将英语单词转化为治愈系爱情故事
"""

import json
import os
import sys
import requests
import re
from typing import Dict, List, Any

# 真实多智能体协作系统 (接入通义千问)
class HealingVocabularyCinema:
    """治愈系单词放映机主类"""
    
    def __init__(self, config_path: str = "config.json"):
        """初始化系统"""
        with open(config_path, 'r', encoding='utf-8') as f:
            self.config = json.load(f)
        
        self.agents = {}
        self._load_agents()
    
    def _load_agents(self):
        """加载所有AI Agent"""
        for agent_config in self.config['agents']:
            agent_name = agent_config['name']
            prompt_file = agent_config['prompt_file']
            
            with open(prompt_file, 'r', encoding='utf-8') as f:
                prompt_content = f.read()
            
            self.agents[agent_name] = {
                'config': agent_config,
                'prompt': prompt_content
            }
        
        print(f"✅ 已加载 {len(self.agents)} 个AI Agent")
    
    def run_workflow(self, words: str) -> Dict[str, Any]:
        """
        运行完整工作流
        
        Args:
            words: 四个英语单词，空格分隔
        
        Returns:
            包含最终故事、评分和反馈的字典
        """
        print(f"\n{'='*60}")
        print(f"🎬 治愈系单词放映机 - 开始放映")
        print(f"{'='*60}")
        print(f"\n输入单词: {words}")
        
        # Step 1: 词语拆解
        print("\n🎬 Step 1: 词语拆解者正在分析...")
        word_analysis = self._call_agent('WordAnalyzer', {'words': words})
        print("✅ 词语分析完成")
        
        # Step 2: 故事创作
        print("\n✍️ Step 2: 治愈系编剧正在创作...")
        story = self._call_agent('StoryWriter', {
            'words': words,
            'word_analysis': word_analysis
        })
        print("✅ 故事创作完成")
        
        # Step 3: 质量评审
        print("\n⚖️ Step 3: 放映机评委正在评审...")
        judgment = self._call_agent('StoryJudge', {
            'words': words,
            'story': story
        })
        print(f"✅ 评审完成 - 得分: {judgment.get('score', 0)}/100")
        
        # 检查是否需要重写
        rewrite_count = 0
        final_story = story
        final_judgment = judgment
        
        while judgment.get('score', 0) < 85 and rewrite_count < 2:
            rewrite_count += 1
            print(f"\n🔄 第{rewrite_count}次重写...")
            
            # 重写故事
            print(f"\n✍️ Step {3 + rewrite_count * 2 - 1}: 根据反馈改进故事...")
            story = self._call_agent('StoryWriter', {
                'words': words,
                'word_analysis': word_analysis,
                'feedback': judgment.get('feedback', '')
            })
            
            # 重新评审
            print(f"\n⚖️ Step {3 + rewrite_count * 2}: 重新评审...")
            judgment = self._call_agent('StoryJudge', {
                'words': words,
                'story': story
            })
            print(f"✅ 重新评审完成 - 得分: {judgment.get('score', 0)}/100")
            
            final_story = story
            final_judgment = judgment
        
        # 输出最终结果
        print(f"\n{'='*60}")
        print("🎬 放映结束 - 最终结果")
        print(f"{'='*60}\n")
        
        return {
            'final_story': final_story,
            'score': final_judgment.get('score', 0),
            'feedback': final_judgment.get('feedback', ''),
            'rewrite_count': rewrite_count
        }
    
    def _call_agent(self, agent_name: str, inputs: Dict[str, Any]) -> Any:
        """
        调用真实大模型 API (通义千问)
        """
        agent = self.agents.get(agent_name)
        if not agent:
            raise ValueError(f"未知的Agent: {agent_name}")
        
        # 1. 获取系统提示词 (Prompt)
        system_prompt = agent['prompt']
        
        # 2. 将输入变量拼接成用户提问
        user_content = "请根据以下信息执行任务：\n"
        for key, value in inputs.items():
            user_content += f"【{key}】\n{value}\n\n"
            
        # 3. 读取 config.json 里的 API 配置
        api_key = self.config.get("api_key", "")
        api_url = self.config.get("api_url", "https://dashscope.aliyuncs.com/compatible-mode/v1/chat/completions")
        model = self.config.get("model", "qwen-plus")
        
        if not api_key or "填入" in api_key or api_key == "YOUR_API_KEY_HERE":
            raise ValueError("请先在 config.json 中配置你真实的 API_KEY！")

        # 4. 发送网络请求给大模型
        headers = {
            "Content-Type": "application/json",
            "Authorization": f"Bearer {api_key}"
        }
        payload = {
            "model": model,
            "messages": [
                {"role": "system", "content": system_prompt},
                {"role": "user", "content": user_content}
            ],
            "temperature": 0.7
        }
        
        print(f"  [网络呼叫] 正在联系 {agent_name} (这可能需要几秒钟)...")
        try:
            response = requests.post(api_url, headers=headers, json=payload, timeout=60)
            response.raise_for_status() # 检查是否发生网络错误
        except Exception as e:
            error_msg = response.text if 'response' in locals() else str(e)
            raise Exception(f"大模型调用失败: {error_msg}")
            
        result_text = response.json()['choices'][0]['message']['content']
        
        # 5. 特殊处理：如果是评审员(StoryJudge)，需要提取分数并返回字典结构
        if agent_name == 'StoryJudge':
            # 用正则提取大模型回答中的数字作为分数
            scores = re.findall(r'\d+', result_text)
            # 过滤掉不合理的数字，取最后一个小于等于100的数字
            valid_scores = [int(s) for s in scores if int(s) <= 100]
            score = valid_scores[-1] if valid_scores else 80 
            
            return {
                'score': score,
                'feedback': result_text
            }
            
        # 其他 Agent 直接返回大模型生成的文本
        return result_text


def main():
    """主函数"""
    print("🎬 治愈系单词放映机 - AI Agent Demo")
    print("=" * 60)
    
    # 初始化系统
    try:
        cinema = HealingVocabularyCinema()
    except FileNotFoundError:
        print("❌ 错误：找不到配置文件 config.json")
        print("请确保在正确的目录下运行此脚本")
        return
    
    # 获取用户输入
    print("\n请输入4个英语单词（用空格分隔）：")
    print("示例：serendipity ephemeral luminescence ethereal")
    
    try:
        words = input("\n> ").strip()
    except KeyboardInterrupt:
        print("\n\n👋 再见！")
        return
    
    if not words:
        words = "serendipity ephemeral luminescence ethereal"
        print(f"使用默认单词：{words}")
    
    # 运行工作流
    try:
        result = cinema.run_workflow(words)
        
        # 显示结果
        print(result['final_story'])
        print(f"\n**最终评分**：{result['score']}/100 {'✅ 通过' if result['score'] >= 85 else '❌ 未通过'}")
        print(f"**重写次数**：{result['rewrite_count']}")
        print(f"\n**评审意见**：{result['feedback']}")
        
    except Exception as e:
        print(f"\n❌ 运行出错：{e}")
        import traceback
        traceback.print_exc()

if __name__ == "__main__":
    main()

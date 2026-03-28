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
from typing import Dict, List, Any

# 模拟多智能体协作系统
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
        调用AI Agent（模拟）
        
        在实际实现中，这里会调用OpenAI API或其他大模型API
        为了演示，我们返回模拟数据
        """
        agent = self.agents.get(agent_name)
        if not agent:
            raise ValueError(f"未知的Agent: {agent_name}")
        
        # 模拟API调用延迟
        import time
        time.sleep(0.5)
        
        # 根据Agent类型返回模拟数据
        if agent_name == 'WordAnalyzer':
            return self._mock_word_analysis(inputs.get('words', ''))
        elif agent_name == 'StoryWriter':
            return self._mock_story_generation(inputs)
        elif agent_name == 'StoryJudge':
            return self._mock_judgment(inputs.get('story', ''))
        
        return {}
    
    def _mock_word_analysis(self, words: str) -> str:
        """模拟词语分析"""
        word_list = words.split()
        analysis = []
        for word in word_list[:4]:
            analysis.append(f"- **{word}**: 已分析其词源、意象和融入方案")
        return "\n".join(analysis)
    
    def _mock_story_generation(self, inputs: Dict) -> str:
        """模拟故事生成"""
        words = inputs.get('words', '').split()[:4]
        word_str = ', '.join([f"**{w}**" for w in words])
        
        story = f"""🎬 **《霓虹灯下的邂逅》**

雨后的街道泛着微光，空气中弥漫着湿润的青草香。林夕推开那扇挂着铜铃的木门，走进了街角那家名为 {word_str.split(',')[0] if words else '**Serendipity**'} 的黑胶唱片行。

店里正放着一首老爵士，暖黄的灯光落在满墙的唱片封面上。她随手抽出一张，封面上写着 {word_str.split(',')[1] if len(words) > 1 else '**Ephemeral**'} ——一支她从未听过的独立乐队。

"那是我的最爱。"一个声音从阴影处传来...

[故事正文包含4个单词的自然融入，400-600字]

---
📖 **【放映机词汇卡】**
"""
        for word in words:
            story += f"- **{word}** - 词性：[释义] ✧ 记忆联想：[诗意线索]\n"
        
        return story
    
    def _mock_judgment(self, story: str) -> Dict[str, Any]:
        """模拟评审"""
        import random
        score = random.randint(88, 95)
        
        return {
            'score': score,
            'feedback': f"这是一个极具电影感的故事。词汇融入自然，画面描写细腻，情感真挚温暖。评分：{score}/100",
            'passed': score >= 85
        }


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

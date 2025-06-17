#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
测试越南语翻译功能
"""

import sys
import os
sys.path.append(os.path.dirname(os.path.abspath(__file__)))

from tools.step033_translation_translator import translator_response

def test_vietnamese_translation():
    """测试越南语翻译功能"""
    
    test_texts = [
        "你好，世界！",
        "今天天气很好。",
        "我喜欢学习新技术。",
        "这是一个很有趣的视频。",
        "人工智能正在改变我们的生活。"
    ]
    
    print("=== 测试越南语翻译功能 ===\n")
    
    for i, text in enumerate(test_texts, 1):
        try:
            # 使用Bing Translate进行翻译
            translation_bing = translator_response(text, 'Vietnamese', 'bing')
            print(f"测试 {i}:")
            print(f"原文: {text}")
            print(f"越南语 (Bing): {translation_bing}")
            
            # 使用Google Translate进行翻译
            try:
                translation_google = translator_response(text, 'Vietnamese', 'google')
                print(f"越南语 (Google): {translation_google}")
            except Exception as e:
                print(f"Google翻译失败: {e}")
            
            print("-" * 50)
            
        except Exception as e:
            print(f"翻译失败: {e}")
            continue

if __name__ == "__main__":
    test_vietnamese_translation()

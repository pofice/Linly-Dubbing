# -*- coding: utf-8 -*-
"""
测试中文视频翻译成越南语的完整流程
"""
import os
import json
import sys
sys.path.append('/media/pofice/PM1725A/pofice/Linly-Dubbing')

from tools.step030_translation import translate_all_transcript_under_folder

def create_test_video_data():
    """创建测试用的视频数据"""
    test_folder = '/media/pofice/PM1725A/pofice/Linly-Dubbing/test_vietnamese'
    
    # 创建测试文件夹
    os.makedirs(test_folder, exist_ok=True)
    
    # 创建测试transcript
    test_transcript = [
        {
            "start": 0.0,
            "end": 3.5,
            "text": "欢迎大家来到我的技术分享频道。",
            "speaker": "Speaker 1"
        },
        {
            "start": 3.5,
            "end": 7.0,
            "text": "今天我们要学习关于人工智能的知识。",
            "speaker": "Speaker 1"
        },
        {
            "start": 7.0,
            "end": 11.0,
            "text": "人工智能正在改变我们的生活和工作方式。",
            "speaker": "Speaker 1"
        },
        {
            "start": 11.0,
            "end": 15.0,
            "text": "让我们一起探索这个令人兴奋的技术领域。",
            "speaker": "Speaker 1"
        },
        {
            "start": 15.0,
            "end": 18.0,
            "text": "希望这个视频对大家有所帮助。",
            "speaker": "Speaker 1"
        }
    ]
    
    # 保存transcript文件
    with open(os.path.join(test_folder, 'transcript.json'), 'w', encoding='utf-8') as f:
        json.dump(test_transcript, f, indent=2, ensure_ascii=False)
    
    # 创建基本的视频信息
    video_info = {
        "title": "人工智能技术介绍",
        "uploader": "技术博主",
        "description": "这是一个关于人工智能技术的介绍视频",
        "upload_date": "20250617",
        "tags": ["人工智能", "技术", "教程"]
    }
    
    with open(os.path.join(test_folder, 'download.info.json'), 'w', encoding='utf-8') as f:
        json.dump(video_info, f, indent=2, ensure_ascii=False)
    
    return test_folder

def test_vietnamese_translation():
    """测试越南语翻译功能"""
    print("=== 创建测试视频数据 ===")
    test_folder = create_test_video_data()
    print(f"测试文件夹: {test_folder}")
    
    print("\n=== 开始越南语翻译测试 ===")
    
    # 测试不同的翻译方法
    methods = ['Bing Translate', 'Google Translate']
    
    for method in methods:
        print(f"\n--- 测试 {method} ---")
        try:
            result, summary, translation = translate_all_transcript_under_folder(
                test_folder, 
                method, 
                'Vietnamese'
            )
            
            print(f"翻译结果: {result}")
            print(f"摘要: {summary}")
            
            if translation:
                print("\n翻译对比:")
                for item in translation:
                    print(f"原文: {item['text']}")
                    print(f"越南语: {item.get('translation', '未翻译')}")
                    print("-" * 50)
            
        except Exception as e:
            print(f"翻译失败: {e}")
    
    print(f"\n=== 测试完成 ===")
    print(f"您可以查看 {test_folder} 文件夹中的翻译结果文件")

if __name__ == '__main__':
    test_vietnamese_translation()

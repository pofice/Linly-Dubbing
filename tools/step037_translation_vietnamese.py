# -*- coding: utf-8 -*-
"""
越南语专用翻译模块
支持通过Google Translate、Bing Translate和LLM进行中文到越南语的翻译
"""
import json
import os
import re
import time
import sys
from loguru import logger

# 添加父目录到Python路径以便导入其他工具模块
parent_dir = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
if parent_dir not in sys.path:
    sys.path.insert(0, parent_dir)

try:
    from tools.step033_translation_translator import translator_response
    from tools.step032_translation_llm import llm_response
    from tools.step031_translation_openai import openai_response
    from tools.step034_translation_ernie import ernie_response
    from tools.step035_translation_qwen import qwen_response
    from tools.step036_translation_ollama import ollama_response
except ImportError:
    # 如果从tools目录导入失败，尝试直接导入
    from step033_translation_translator import translator_response
    from step032_translation_llm import llm_response
    from step031_translation_openai import openai_response
    from step034_translation_ernie import ernie_response
    from step035_translation_qwen import qwen_response
    from step036_translation_ollama import ollama_response

def vietnamese_translation_prompt(summary):
    """为越南语翻译创建专用的prompt模板"""
    info = f'This is a video called "{summary["title"]}". {summary["summary"]}.'
    return [
        {'role': 'system', 'content': f'You are an expert translator specializing in Vietnamese language. The current task involves translating the transcript of a video titled "{summary["title"]}". The summary of the video is: {summary["summary"]}. Your goal is to translate the following sentences into natural, fluent Vietnamese. Please ensure the translations maintain the original meaning and tone while being expressed in natural Vietnamese that Vietnamese speakers would use in daily conversation. Only provide the Vietnamese translation without any additional text or explanations.'},
        {'role': 'user', 'content': 'Translate into Vietnamese: "Knowledge is power."'},
        {'role': 'assistant', 'content': 'Kiến thức là sức mạnh.'},
        {'role': 'user', 'content': 'Translate into Vietnamese: "To be or not to be, that is the question."'},
        {'role': 'assistant', 'content': 'Sống hay không sống, đó là câu hỏi.'},
        {'role': 'user', 'content': 'Translate into Vietnamese: "The weather is very nice today."'},
        {'role': 'assistant', 'content': 'Hôm nay thời tiết rất đẹp.'},
        {'role': 'user', 'content': 'Translate into Vietnamese: "I love learning new technologies."'},
        {'role': 'assistant', 'content': 'Tôi thích học các công nghệ mới.'},
    ]

def valid_vietnamese_translation(text, translation):
    """验证越南语翻译的有效性"""
    translation = translation.strip()
    
    # 移除常见的包装格式
    if (translation.startswith('```') and translation.endswith('```')):
        translation = translation[3:-3].strip()
    
    if (translation.startswith('"') and translation.endswith('"')) or (translation.startswith('"') and translation.endswith('"')):
        translation = translation[1:-1].strip()
    
    # 检查是否包含翻译提示词
    forbidden_words = ['translate', 'Translate', 'translation', 'Translation', 'Vietnamese', 'Tiếng Việt', 'dịch thuật', 'bản dịch']
    for word in forbidden_words:
        if word in translation and len(translation.split()) <= 3:  # 只检查短文本
            return False, "Please provide only the Vietnamese translation without any additional text."
    
    # 基本长度检查
    if len(text) <= 10 and len(translation) > len(text) * 3:
        return False, "Translation is too long for short text."
    elif len(translation) > len(text) * 2:
        return False, "Translation appears to be too long."
    
    return True, translation

def translate_to_vietnamese(summary, transcript, method='Bing Translate'):
    """
    将转录文本翻译成越南语
    
    Args:
        summary: 视频摘要信息
        transcript: 转录文本列表
        method: 翻译方法 ('Bing Translate', 'Google Translate', 'LLM', 'OpenAI', 'Ernie', 'Qwen', 'Ollama')
    
    Returns:
        list: 翻译后的文本列表
    """
    full_translation = []
    
    # 使用在线翻译服务
    if method in ['Google Translate', 'Bing Translate']:
        translator_server = 'google' if method == 'Google Translate' else 'bing'
        
        for line in transcript:
            text = line['text']
            try:
                translation = translator_response(text, to_language='Vietnamese', translator_server=translator_server)
                logger.info(f'原文：{text}')
                logger.info(f'越南语译文：{translation}')
                full_translation.append(translation)
            except Exception as e:
                logger.error(f'翻译失败: {e}')
                full_translation.append(text)  # 如果翻译失败，保留原文
            time.sleep(0.1)
    
    # 使用AI模型翻译
    else:
        fixed_message = vietnamese_translation_prompt(summary)
        history = []
        
        for line in transcript:
            text = line['text']
            translation = text  # 默认值
            
            for retry in range(5):  # 减少重试次数
                try:
                    messages = fixed_message + history[-20:] + [
                        {'role': 'user', 'content': f'Translate into Vietnamese: "{text}"'}
                    ]
                    
                    # 根据方法选择相应的AI服务
                    if method == 'LLM':
                        response = llm_response(messages)
                    elif method == 'OpenAI':
                        response = openai_response(messages)
                    elif method == 'Ernie':
                        system_content = messages[0]['content']
                        user_messages = messages[1:]
                        response = ernie_response(user_messages, system=system_content)
                    elif method == 'Qwen':
                        response = qwen_response(messages)
                    elif method == 'Ollama':
                        response = ollama_response(messages)
                    else:
                        raise Exception(f'Unsupported method: {method}')
                    
                    translation = response.replace('\n', '').strip()
                    logger.info(f'原文：{text}')
                    logger.info(f'越南语译文：{translation}')
                    
                    success, validated_translation = valid_vietnamese_translation(text, translation)
                    if success:
                        translation = validated_translation
                        break
                    else:
                        logger.warning(f'翻译验证失败: {validated_translation}')
                        
                except Exception as e:
                    logger.error(f'翻译失败 (重试 {retry + 1}): {e}')
                    time.sleep(1)
            
            full_translation.append(translation)
            
            # 更新历史记录
            history.append({'role': 'user', 'content': f'Translate into Vietnamese: "{text}"'})
            history.append({'role': 'assistant', 'content': translation})
            time.sleep(0.1)
    
    return full_translation

def translate_vietnamese_main(method, folder):
    """
    主要的越南语翻译函数
    
    Args:
        method: 翻译方法
        folder: 视频文件夹路径
    
    Returns:
        tuple: (summary, transcript) 或 False
    """
    translation_path = os.path.join(folder, 'translation_vietnamese.json')
    
    if os.path.exists(translation_path):
        logger.info(f'Vietnamese translation already exists in {folder}')
        summary = json.load(open(os.path.join(folder, 'summary.json'), 'r', encoding='utf-8'))
        transcript = json.load(open(translation_path, 'r', encoding='utf-8'))
        return summary, transcript
    
    # 读取必要文件
    transcript_path = os.path.join(folder, 'transcript.json')
    if not os.path.exists(transcript_path):
        logger.error(f'Transcript file not found in {folder}')
        return False
    
    with open(transcript_path, 'r', encoding='utf-8') as f:
        transcript = json.load(f)
    
    # 读取或创建摘要
    summary_path = os.path.join(folder, 'summary.json')
    if os.path.exists(summary_path):
        with open(summary_path, 'r', encoding='utf-8') as f:
            summary = json.load(f)
    else:
        # 创建基本摘要信息
        info_path = os.path.join(folder, 'download.info.json')
        if os.path.exists(info_path):
            with open(info_path, 'r', encoding='utf-8') as f:
                info = json.load(f)
            summary = {
                'title': info.get('title', os.path.basename(folder)),
                'summary': info.get('description', 'Video content'),
                'language': 'Vietnamese'
            }
        else:
            summary = {
                'title': os.path.basename(folder),
                'summary': 'Video content',
                'language': 'Vietnamese'
            }
        
        with open(summary_path, 'w', encoding='utf-8') as f:
            json.dump(summary, f, indent=2, ensure_ascii=False)
    
    # 执行翻译
    try:
        translation_list = translate_to_vietnamese(summary, transcript, method)
        
        # 添加翻译到transcript中
        for i, line in enumerate(transcript):
            line['translation'] = translation_list[i]
        
        # 保存翻译结果
        with open(translation_path, 'w', encoding='utf-8') as f:
            json.dump(transcript, f, indent=2, ensure_ascii=False)
        
        logger.info(f'Vietnamese translation completed for {folder}')
        return summary, transcript
        
    except Exception as e:
        logger.error(f'Failed to translate to Vietnamese: {e}')
        return False

if __name__ == '__main__':
    # 测试函数
    test_summary = {
        'title': '测试视频',
        'summary': '这是一个关于技术的测试视频'
    }
    
    test_transcript = [
        {'text': '你好，欢迎观看这个视频。', 'start': 0.0, 'end': 2.0, 'speaker': 'Speaker 1'},
        {'text': '今天我们来学习新技术。', 'start': 2.0, 'end': 4.0, 'speaker': 'Speaker 1'},
        {'text': '希望大家能够喜欢。', 'start': 4.0, 'end': 6.0, 'speaker': 'Speaker 1'}
    ]
    
    print("=== 测试越南语翻译模块 ===")
    translation = translate_to_vietnamese(test_summary, test_transcript, 'Bing Translate')
    
    for i, item in enumerate(test_transcript):
        print(f"原文: {item['text']}")
        print(f"越南语: {translation[i]}")
        print("-" * 40)

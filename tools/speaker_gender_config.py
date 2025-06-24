import json
import os
from loguru import logger

# EdgeTTS 越南语声音选项（按性别分类）
VIETNAMESE_VOICES = {
    'male': ['vi-VN-NamMinhNeural'],
    'female': ['vi-VN-HoaiMyNeural']
}

# 中文声音选项（按性别分类）
CHINESE_VOICES = {
    'male': ['zh-CN-YunxiNeural', 'zh-CN-YunjianNeural'],
    'female': ['zh-CN-XiaoxiaoNeural', 'zh-CN-XiaoyiNeural', 'zh-CN-YunxiaNeural']
}

# 英文声音选项（按性别分类）
ENGLISH_VOICES = {
    'male': ['en-US-DavisNeural', 'en-US-JasonNeural', 'en-US-TonyNeural'],
    'female': ['en-US-JennyNeural', 'en-US-AriaNeural', 'en-US-SaraNeural']
}

ALL_VOICES_BY_LANGUAGE = {
    'Vietnamese': VIETNAMESE_VOICES,
    '中文': CHINESE_VOICES,
    'English': ENGLISH_VOICES
}

def create_speaker_gender_config(folder, speakers, target_language='Vietnamese'):
    """为说话人创建性别配置文件"""
    config_path = os.path.join(folder, 'speaker_gender_config.json')
    
    if os.path.exists(config_path):
        logger.info(f"Speaker gender config already exists: {config_path}")
        with open(config_path, 'r', encoding='utf-8') as f:
            return json.load(f)
    
    # 创建默认配置
    voices = ALL_VOICES_BY_LANGUAGE.get(target_language, VIETNAMESE_VOICES)
    config = {
        "target_language": target_language,
        "speakers": {}
    }
    
    # 为每个说话人分配默认配置
    for i, speaker in enumerate(sorted(speakers)):
        # 交替分配男女性别作为默认值
        gender = 'male' if i % 2 == 0 else 'female'
        voice = voices[gender][0]  # 选择该性别的第一个声音
        
        config["speakers"][speaker] = {
            "gender": gender,
            "voice": voice,
            "description": f"说话人 {speaker} - 默认设置为{gender}，请根据实际情况修改"
        }
    
    # 保存配置文件
    with open(config_path, 'w', encoding='utf-8') as f:
        json.dump(config, f, indent=2, ensure_ascii=False)
    
    logger.info(f"Created speaker gender config: {config_path}")
    logger.info("请编辑 speaker_gender_config.json 文件，为每个说话人设置正确的性别")
    
    return config

def get_voice_for_speaker(folder, speaker, target_language='Vietnamese'):
    """根据说话人和配置获取对应的声音"""
    config_path = os.path.join(folder, 'speaker_gender_config.json')
    
    if not os.path.exists(config_path):
        logger.warning(f"Speaker gender config not found: {config_path}")
        # 返回默认声音
        voices = ALL_VOICES_BY_LANGUAGE.get(target_language, VIETNAMESE_VOICES)
        return voices['female'][0]  # 默认女声
    
    try:
        with open(config_path, 'r', encoding='utf-8') as f:
            config = json.load(f)
        
        if speaker in config.get("speakers", {}):
            return config["speakers"][speaker]["voice"]
        else:
            logger.warning(f"Speaker {speaker} not found in config, using default voice")
            voices = ALL_VOICES_BY_LANGUAGE.get(target_language, VIETNAMESE_VOICES)
            return voices['female'][0]  # 默认女声
    
    except Exception as e:
        logger.error(f"Error reading speaker config: {e}")
        voices = ALL_VOICES_BY_LANGUAGE.get(target_language, VIETNAMESE_VOICES)
        return voices['female'][0]  # 默认女声

if __name__ == '__main__':
    # 测试
    test_speakers = ['SPEAKER_00', 'SPEAKER_01']
    config = create_speaker_gender_config('.', test_speakers, 'Vietnamese')
    print(json.dumps(config, indent=2, ensure_ascii=False))

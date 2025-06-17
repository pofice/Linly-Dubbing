# -*- coding: utf-8 -*-
"""
测试一键自动化越南语翻译功能
"""
import os
import json
import sys

# 添加项目根目录到sys.path
project_root = '/media/pofice/PM1725A/pofice/Linly-Dubbing'
sys.path.append(project_root)
os.chdir(project_root)

from tools.do_everything import do_everything

def create_vietnamese_config():
    """创建越南语配置文件"""
    config = {
        "video_folder": "test_vietnamese_auto",
        "resolution": "720p",
        "video_count": 1,
        "model": "htdemucs_ft",
        "device": "auto",
        "shifts": 5,
        "asr_model": "WhisperX",
        "whisperx_size": "large",
        "batch_size": 32,
        "separate_speakers": True,
        "min_speakers": None,
        "max_speakers": None,
        "translation_method": "Bing Translate",
        "target_language_translation": "Vietnamese",
        "tts_method": "EdgeTTS",
        "target_language_tts": "Vietnamese",
        "edge_tts_voice": "vi-VN-HoaiMyNeural",
        "add_subtitles": True,
        "speed_factor": 1.0,
        "frame_rate": 30,
        "background_music": None,
        "bg_music_volume": 0.5,
        "video_volume": 1.0,
        "output_resolution": "720p",
        "max_workers": 1,
        "max_retries": 3
    }
    
    config_path = os.path.join(project_root, 'tabs', 'config.json')
    with open(config_path, 'w', encoding='utf-8') as f:
        json.dump(config, f, indent=2, ensure_ascii=False)
    
    print(f"已创建越南语配置文件: {config_path}")
    return config

def test_vietnamese_auto():
    """测试越南语一键自动化功能"""
    print("=== 测试越南语一键自动化功能 ===")
    
    # 创建配置
    config = create_vietnamese_config()
    
    # 使用一个短视频进行测试
    test_url = "https://www.bilibili.com/video/BV1kr421M7vz/"  # 可以替换为其他短视频
    
    print(f"测试视频URL: {test_url}")
    print(f"输出文件夹: {config['video_folder']}")
    print(f"翻译方法: {config['translation_method']}")
    print(f"翻译目标语言: {config['target_language_translation']}")
    print(f"TTS方法: {config['tts_method']}")
    print(f"TTS目标语言: {config['target_language_tts']}")
    print(f"TTS语音: {config['edge_tts_voice']}")
    
    print("\n开始一键自动化处理...")
    
    try:
        # 进度回调函数
        def progress_callback(progress, status):
            print(f"进度: {progress}% - {status}")
        
        # 调用do_everything函数
        result, video_path = do_everything(
            root_folder=config['video_folder'],
            url=test_url,
            num_videos=config['video_count'],
            resolution=config['resolution'],
            demucs_model=config['model'],
            device=config['device'],
            shifts=config['shifts'],
            asr_method=config['asr_model'],
            whisper_model=config['whisperx_size'],
            batch_size=config['batch_size'],
            diarization=config['separate_speakers'],
            whisper_min_speakers=config['min_speakers'],
            whisper_max_speakers=config['max_speakers'],
            translation_method=config['translation_method'],
            translation_target_language=config['target_language_translation'],
            tts_method=config['tts_method'],
            tts_target_language=config['target_language_tts'],
            voice=config['edge_tts_voice'],
            subtitles=config['add_subtitles'],
            speed_up=config['speed_factor'],
            fps=config['frame_rate'],
            background_music=config['background_music'],
            bgm_volume=config['bg_music_volume'],
            video_volume=config['video_volume'],
            target_resolution=config['output_resolution'],
            max_workers=config['max_workers'],
            max_retries=config['max_retries'],
            progress_callback=progress_callback
        )
        
        print(f"\n=== 处理完成 ===")
        print(f"结果: {result}")
        if video_path:
            print(f"生成的视频路径: {video_path}")
        
        return True
        
    except Exception as e:
        print(f"\n=== 处理失败 ===")
        print(f"错误: {str(e)}")
        import traceback
        traceback.print_exc()
        return False

if __name__ == '__main__':
    success = test_vietnamese_auto()
    if success:
        print("\n🎉 越南语一键自动化测试成功！")
    else:
        print("\n❌ 越南语一键自动化测试失败！")

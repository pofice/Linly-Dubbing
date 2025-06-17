# -*- coding: utf-8 -*-
"""
测试越南语TTS功能修复
"""
import os
import sys

# 添加项目根目录到sys.path
project_root = '/media/pofice/PM1725A/pofice/Linly-Dubbing'
sys.path.append(project_root)
os.chdir(project_root)

from tools.step040_tts import generate_all_wavs_under_folder

def test_vietnamese_tts():
    """测试越南语TTS功能"""
    print("=== 测试越南语TTS功能 ===")
    
    # 使用之前创建的测试文件夹
    test_folder = '/media/pofice/PM1725A/pofice/Linly-Dubbing/test_vietnamese'
    
    if not os.path.exists(test_folder):
        print(f"测试文件夹不存在: {test_folder}")
        print("请先运行越南语翻译测试创建测试数据")
        return False
    
    # 检查是否有越南语翻译文件
    vietnamese_file = os.path.join(test_folder, 'translation_vietnamese.json')
    if not os.path.exists(vietnamese_file):
        print(f"越南语翻译文件不存在: {vietnamese_file}")
        print("请先运行越南语翻译测试")
        return False
    
    print(f"测试文件夹: {test_folder}")
    print(f"使用翻译文件: {vietnamese_file}")
    
    try:
        # 测试越南语TTS
        result, wav_combined, wav_ori = generate_all_wavs_under_folder(
            test_folder,
            method='EdgeTTS',
            target_language='Vietnamese',
            voice='vi-VN-HoaiMyNeural'
        )
        
        print(f"\nTTS结果: {result}")
        if wav_combined:
            print(f"合成音频路径: {wav_combined}")
            print(f"原始音频路径: {wav_ori}")
            
            # 检查文件是否真的生成了
            if os.path.exists(wav_combined):
                print("✅ 越南语TTS合成成功！")
                
                # 列出生成的wav文件
                wavs_folder = os.path.join(test_folder, 'wavs')
                if os.path.exists(wavs_folder):
                    wav_files = [f for f in os.listdir(wavs_folder) if f.endswith('.wav')]
                    print(f"生成了 {len(wav_files)} 个语音片段:")
                    for wav_file in sorted(wav_files):
                        print(f"  - {wav_file}")
                        
                return True
            else:
                print("❌ 音频文件未生成")
                return False
        else:
            print("❌ TTS返回了空结果")
            return False
            
    except Exception as e:
        print(f"❌ TTS测试失败: {str(e)}")
        import traceback
        traceback.print_exc()
        return False

if __name__ == '__main__':
    success = test_vietnamese_tts()
    if success:
        print("\n🎉 越南语TTS修复成功！")
    else:
        print("\n❌ 越南语TTS仍有问题，需要进一步检查")

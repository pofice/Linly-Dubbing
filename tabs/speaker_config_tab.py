import gradio as gr
import json
import os
from loguru import logger
from tools.speaker_gender_config import create_speaker_gender_config, ALL_VOICES_BY_LANGUAGE

def load_speaker_config(folder):
    """加载说话人配置"""
    config_path = os.path.join(folder, 'speaker_gender_config.json')
    if os.path.exists(config_path):
        with open(config_path, 'r', encoding='utf-8') as f:
            return json.load(f)
    return None

def save_speaker_config(folder, config_json):
    """保存说话人配置"""
    try:
        config = json.loads(config_json)
        config_path = os.path.join(folder, 'speaker_gender_config.json')
        with open(config_path, 'w', encoding='utf-8') as f:
            json.dump(config, f, indent=2, ensure_ascii=False)
        return "配置保存成功！"
    except Exception as e:
        return f"保存失败：{str(e)}"

def check_speaker_config(folder, target_language='Vietnamese'):
    """检查并显示说话人配置"""
    config_path = os.path.join(folder, 'speaker_gender_config.json')
    
    # 检查是否有转录文件
    transcript_path = os.path.join(folder, 'transcript.json')
    if not os.path.exists(transcript_path):
        return "请先完成语音识别步骤", ""
    
    # 读取说话人信息
    with open(transcript_path, 'r', encoding='utf-8') as f:
        transcript = json.load(f)
    
    speakers = set()
    for line in transcript:
        speakers.add(line['speaker'])
    
    if not speakers:
        return "未找到说话人信息", ""
    
    # 创建或加载配置
    if not os.path.exists(config_path):
        config = create_speaker_gender_config(folder, speakers, target_language)
        status = f"已为 {len(speakers)} 个说话人创建默认配置：{', '.join(speakers)}"
    else:
        with open(config_path, 'r', encoding='utf-8') as f:
            config = json.load(f)
        status = f"已加载现有配置，包含 {len(speakers)} 个说话人：{', '.join(speakers)}"
    
    config_text = json.dumps(config, indent=2, ensure_ascii=False)
    return status, config_text

# 创建说话人配置界面
def create_speaker_config_interface():
    with gr.Column():
        gr.Markdown("## 🎭 说话人性别配置")
        gr.Markdown("""
        **使用说明：**
        1. 先完成语音识别，系统会自动识别说话人
        2. 点击"检查说话人配置"查看当前配置
        3. 编辑下方JSON配置，为每个说话人设置正确的性别和声音
        4. 男声选项：vi-VN-NamMinhNeural
        5. 女声选项：vi-VN-HoaiMyNeural
        """)
        
        folder_input = gr.Textbox(label="视频文件夹", value="videos", placeholder="输入包含转录文件的文件夹路径")
        target_lang = gr.Dropdown(['Vietnamese', '中文', 'English'], label='目标语言', value='Vietnamese')
        
        check_btn = gr.Button("🔍 检查说话人配置", variant="primary")
        status_output = gr.Textbox(label="状态", interactive=False)
        
        config_editor = gr.Textbox(
            label="说话人配置 (JSON格式)", 
            lines=15, 
            placeholder="配置将在此显示...",
            info="修改gender字段为'male'或'female'，修改voice字段选择声音"
        )
        
        save_btn = gr.Button("💾 保存配置", variant="secondary")
        save_status = gr.Textbox(label="保存状态", interactive=False)
        
        # 绑定事件
        check_btn.click(
            fn=check_speaker_config,
            inputs=[folder_input, target_lang],
            outputs=[status_output, config_editor]
        )
        
        save_btn.click(
            fn=save_speaker_config,
            inputs=[folder_input, config_editor],
            outputs=[save_status]
        )
        
        return folder_input, target_lang, config_editor

if __name__ == '__main__':
    # 测试界面
    demo = gr.Interface(fn=lambda: None, inputs=[], outputs=[])
    demo.launch()

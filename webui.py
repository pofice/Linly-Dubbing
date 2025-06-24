import gradio as gr
from tools.step000_video_downloader import download_from_url
from tools.step010_demucs_vr import separate_all_audio_under_folder
from tools.step020_asr import transcribe_all_audio_under_folder
from tools.step030_translation import translate_all_transcript_under_folder
from tools.step040_tts import generate_all_wavs_under_folder
from tools.step050_synthesize_video import synthesize_all_video_under_folder
from tools.do_everything import do_everything
from tools.utils import SUPPORT_VOICE
from tabs.speaker_config_tab import create_speaker_config_interface

# 一键自动化界面
full_auto_interface = gr.Interface(
    fn=do_everything,
    inputs=[
        gr.Textbox(label='视频输出文件夹', value='videos'),
        gr.Textbox(label='视频URL', placeholder='请输入Youtube或Bilibili的视频、播放列表或频道的URL', 
                   value='https://www.bilibili.com/video/BV1kr421M7vz/'),
        gr.Slider(minimum=1, maximum=100, step=1, label='下载视频数量', value=5),
        gr.Radio(['4320p', '2160p', '1440p', '1080p', '720p', '480p', '360p', '240p', '144p'], label='分辨率', value='1080p'),

        gr.Radio(['htdemucs', 'htdemucs_ft', 'htdemucs_6s', 'hdemucs_mmi', 'mdx', 'mdx_extra', 'mdx_q', 'mdx_extra_q', 'SIG'], label='模型', value='htdemucs_ft'),
        gr.Radio(['auto', 'cuda', 'cpu'], label='计算设备', value='auto'),
        gr.Slider(minimum=0, maximum=10, step=1, label='移位次数 Number of shifts', value=5),

        gr.Dropdown(['WhisperX', 'FunASR'], label='ASR模型选择', value='WhisperX'),
        gr.Radio(['large', 'medium', 'small', 'base', 'tiny'], label='WhisperX模型大小', value='large'),
        gr.Slider(minimum=1, maximum=128, step=1, label='批处理大小 Batch Size', value=32),
        gr.Checkbox(label='分离多个说话人', value=True),
        gr.Radio([None, 1, 2, 3, 4, 5, 6, 7, 8, 9], label='最小说话人数', value=None),
        gr.Radio([None, 1, 2, 3, 4, 5, 6, 7, 8, 9], label='最大说话人数', value=None),

        gr.Dropdown(['OpenAI', 'LLM', 'Google Translate', 'Bing Translate', 'Ernie'], label='翻译方式', value='Bing Translate'),
        gr.Dropdown(['简体中文', '繁体中文', 'English', 'Cantonese', 'Japanese', 'Korean', 'Vietnamese'], label='目标语言', value='Vietnamese'),

        gr.Dropdown(['xtts', 'cosyvoice', 'EdgeTTS'], label='AI语音生成方法', value='EdgeTTS'),
        gr.Dropdown(['中文', 'English', '粤语', 'Japanese', 'Korean', 'Spanish', 'French', 'Vietnamese'], label='目标语言', value='Vietnamese'),
        gr.Dropdown(SUPPORT_VOICE, value='vi-VN-HoaiMyNeural', label='EdgeTTS声音选择'),

        gr.Checkbox(label='添加字幕', value=True),
        gr.Slider(minimum=0.5, maximum=2, step=0.05, label='加速倍数', value=1.00),
        gr.Slider(minimum=1, maximum=60, step=1, label='帧率', value=30),
        gr.Audio(label='背景音乐', sources=['upload']),
        gr.Slider(minimum=0, maximum=1, step=0.05, label='背景音乐音量', value=0.5),
        gr.Slider(minimum=0, maximum=1, step=0.05, label='视频音量', value=1.0),
        gr.Radio(['4320p', '2160p', '1440p', '1080p', '720p', '480p', '360p', '240p', '144p'], label='分辨率', value='1080p'),

        gr.Slider(minimum=1, maximum=100, step=1, label='Max Workers', value=1),
        gr.Slider(minimum=1, maximum=10, step=1, label='Max Retries', value=3),
    ],
    outputs=[gr.Text(label='合成状态'), gr.Video(label='合成视频样例结果')],
    allow_flagging='never',
)    

# 下载视频接口
download_interface = gr.Interface(
    fn=download_from_url,
    inputs=[
        gr.Textbox(label='视频URL', placeholder='请输入Youtube或Bilibili的视频、播放列表或频道的URL', 
                   value='https://www.bilibili.com/video/BV1kr421M7vz/'),
        gr.Textbox(label='视频输出文件夹', value='videos'),
        gr.Radio(['4320p', '2160p', '1440p', '1080p', '720p', '480p', '360p', '240p', '144p'], label='分辨率', value='1080p'),
        gr.Slider(minimum=1, maximum=100, step=1, label='下载视频数量', value=5),
        # gr.Checkbox(label='单个视频', value=False),
    ],
    outputs=[
        gr.Textbox(label='下载状态'), 
        gr.Video(label='示例视频'), 
        gr.Json(label='下载信息')
    ],
    allow_flagging='never',
)

# 人声分离接口
demucs_interface = gr.Interface(
    fn=separate_all_audio_under_folder,
    inputs=[
        gr.Textbox(label='视频文件夹', value='videos'),
        gr.Radio(['htdemucs', 'htdemucs_ft', 'htdemucs_6s', 'hdemucs_mmi', 'mdx', 'mdx_extra', 'mdx_q', 'mdx_extra_q', 'SIG'], label='模型', value='htdemucs_ft'),
        gr.Radio(['auto', 'cuda', 'cpu'], label='计算设备', value='auto'),
        gr.Checkbox(label='显示进度条', value=True),
        gr.Slider(minimum=0, maximum=10, step=1, label='移位次数 Number of shifts', value=5),
    ],
    outputs=[
        gr.Text(label='分离结果状态'), 
        gr.Audio(label='人声音频'), 
        gr.Audio(label='伴奏音频')
    ],
    allow_flagging='never',
)

# AI智能语音识别接口
asr_inference = gr.Interface(
    fn=transcribe_all_audio_under_folder,
    inputs=[
        gr.Textbox(label='视频文件夹', value='videos'),
        gr.Dropdown(['WhisperX', 'FunASR'], label='ASR模型选择', value='WhisperX'),
        gr.Radio(['large', 'medium', 'small', 'base', 'tiny'], label='WhisperX模型大小', value='large'),
        gr.Radio(['auto', 'cuda', 'cpu'], label='计算设备', value='auto'),
        gr.Slider(minimum=1, maximum=128, step=1, label='批处理大小 Batch Size', value=32),
        gr.Checkbox(label='分离多个说话人', value=True),
        gr.Radio([None, 1, 2, 3, 4, 5, 6, 7, 8, 9], label='最小说话人数', value=None),
        gr.Radio([None, 1, 2, 3, 4, 5, 6, 7, 8, 9], label='最大说话人数', value=None),
    ],
    outputs=[
        gr.Text(label='语音识别状态'), 
        gr.Json(label='识别结果详情')
    ],
    allow_flagging='never',
)

# 翻译字幕接口
translation_interface = gr.Interface(
    fn=translate_all_transcript_under_folder,
    inputs=[
        gr.Textbox(label='视频文件夹', value='videos'),
        gr.Dropdown(['OpenAI', 'LLM', 'Google Translate', 'Bing Translate', 'Ernie'], label='翻译方式', value='Bing Translate'),
        gr.Dropdown(['简体中文', '繁体中文', 'English', 'Cantonese', 'Japanese', 'Korean', 'Vietnamese'], label='目标语言', value='Vietnamese'),
    ],
    outputs=[
        gr.Text(label='翻译状态'), 
        gr.Json(label='总结结果'), 
        gr.Json(label='翻译结果')
    ],
    allow_flagging='never',
)

# AI语音合成接口
tts_interface = gr.Interface(
    fn=generate_all_wavs_under_folder,
    inputs=[
        gr.Textbox(label='视频文件夹', value='videos'),
        gr.Dropdown(['xtts', 'cosyvoice', 'EdgeTTS'], label='AI语音生成方法', value='EdgeTTS'),
        gr.Dropdown(['中文', 'English', '粤语', 'Japanese', 'Korean', 'Spanish', 'French', 'Vietnamese'], label='目标语言', value='Vietnamese'),
        gr.Dropdown(SUPPORT_VOICE, value='vi-VN-HoaiMyNeural', label='EdgeTTS声音选择'),
    ],
    outputs=[
        gr.Text(label='合成状态'), 
        gr.Audio(label='合成语音'), 
        gr.Audio(label='原始音频')
    ],
    allow_flagging='never',
)

# 视频合成接口
synthesize_video_interface = gr.Interface(
    fn=synthesize_all_video_under_folder,
    inputs=[
        gr.Textbox(label='视频文件夹', value='videos'),
        gr.Checkbox(label='添加字幕', value=True),
        gr.Slider(minimum=0.5, maximum=2, step=0.05, label='加速倍数', value=1.00),
        gr.Slider(minimum=1, maximum=60, step=1, label='帧率', value=30),
        gr.Audio(label='背景音乐', sources=['upload'], type='filepath'),
        gr.Slider(minimum=0, maximum=1, step=0.05, label='背景音乐音量', value=0.5),
        gr.Slider(minimum=0, maximum=1, step=0.05, label='视频音量', value=1.0),
        gr.Radio(['4320p', '2160p', '1440p', '1080p', '720p', '480p', '360p', '240p', '144p'], label='分辨率', value='1080p'),

    ],
    outputs=[
        gr.Text(label='合成状态'), 
        gr.Video(label='合成视频')
    ],
    allow_flagging='never',
)

linly_talker_interface = gr.Interface(
    fn=lambda: None,
    inputs=[
        gr.Textbox(label='视频文件夹', value='videos'),
        gr.Dropdown(['Wav2Lip', 'Wav2Lipv2','SadTalker'], label='AI配音方式', value='Wav2Lip'),
    ],      
    outputs=[
        gr.Markdown(value="施工中，请静候佳音 可参考 [https://github.com/Kedreamix/Linly-Talker](https://github.com/Kedreamix/Linly-Talker)"),
        gr.Text(label='合成状态'),
        gr.Video(label='合成视频')
    ],
)

# 说话人性别配置界面
speaker_config_interface = gr.Interface(
    fn=lambda: ("请使用下方的配置工具", ""),
    inputs=[],
    outputs=[gr.Text(label="说明"), gr.Text(label="配置")],
    allow_flagging='never',
)

# 在界面中嵌入说话人配置组件
with gr.Blocks() as speaker_config_block:
    create_speaker_config_interface()

my_theme = gr.themes.Soft()
# 应用程序界面
app = gr.TabbedInterface(
    theme=my_theme,
    interface_list=[
        full_auto_interface,
        download_interface,
        demucs_interface,
        asr_inference,
        translation_interface,
        speaker_config_block,
        tts_interface,
        synthesize_video_interface,
        linly_talker_interface
    ],
    tab_names=[
        '一键自动化 One-Click', 
        '自动下载视频 ', '人声分离', 'AI智能语音识别', '字幕翻译', '🎭 说话人配置', 'AI语音合成', '视频合成',
        'Linly-Talker 对口型（开发中）'],
    title='智能视频多语言AI配音/翻译工具 - Linly-Dubbing'
)

if __name__ == '__main__':
    app.launch(
        server_name="127.0.0.1", 
        server_port=6006,
        share=True,
        inbrowser=True
    )
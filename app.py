from flask import Flask, request, render_template, send_file, jsonify
from rembg import remove
from PIL import Image
import io
import os

# 初始化 Flask
app = Flask(__name__)

# 配置：允许上传更大的图片
app.config['MAX_CONTENT_LENGTH'] = 32 * 1024 * 1024  # 32MB

# 首页
@app.route('/')
def index():
    return render_template('index.html')

# 去背景接口（优化版）
@app.route('/remove-bg', methods=['POST'])
def remove_bg():
    try:
        # 1. 检查是否上传图片
        if 'image' not in request.files:
            return jsonify({"error": "请上传图片"}), 400

        file = request.files['image']
        if file.filename == '':
            return jsonify({"error": "未选择文件"}), 400

        # 2. 打开图片并统一格式
        input_img = Image.open(file.stream).convert("RGBA")

        # 3. 去背景（核心）
        output_img = remove(input_img)

        # 4. 生成返回图片
        img_bytes = io.BytesIO()
        output_img.save(img_bytes, format="PNG")
        img_bytes.seek(0)

        return send_file(
            img_bytes,
            mimetype="image/png",
            as_attachment=False
        )

    except Exception as e:
        print(f"错误：{str(e)}")
        return jsonify({"error": f"处理失败：{str(e)}"}), 500

# 启动
if __name__ == '__main__':
    app.run(
        host="0.0.0.0",
        port=5000,
        debug=False  # 关闭调试，避免模型重复加载
    )
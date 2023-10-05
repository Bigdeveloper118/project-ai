from flask import Flask, render_template, request, jsonify
import os
import openai
import textwrap

app = Flask(__name__)
openai.api_key = "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"

# ... (เพิ่มเส้นที่ไม่เกี่ยวข้องได้ที่นี่)
# Define a function to format the email text
def format_email_text(email_text):
    # Split the text into lines
    lines = email_text.strip().split("\n")

    # Create a list to store the formatted lines
    formatted_lines = []

    # Check if the email starts with "greet"
    if lines and lines[0] == "greet":
        formatted_lines.append("greet")

        # Check if there's a subject line and add it
        if len(lines) > 1 and lines[1].startswith("Subject: "):
            formatted_lines.append(lines[1])
            start_idx = 2
        else:
            start_idx = 1

        # Add the rest of the lines
        formatted_lines.extend(lines[start_idx:])

    # Combine the formatted lines into a single text
    formatted_email_text = "\n".join(formatted_lines)

    return formatted_email_text
@app.route('/')
def index():
    return render_template('index.html')
@app.route('/generate_email', methods=['POST'])
def generate_email():
    # รับข้อมูลที่ส่งมาจาก PyQt5
    recipient_name = request.form['recipient_name']
    sender_name = request.form['sender_name']
    keywords = request.form['keywords']
    topic = request.form['topic']
    language = request.form['language']

    # สร้าง prompt โดยขึ้นอยู่กับภาษาที่เลือก
    if language == "Japanese":
        prompt = (f"{sender_name}から{recipient_name}に宛てた『{topic}』についてのメールを、以下のキーワードを使って書いてください: {keywords}")
    else:
        prompt = (f"Write an email about {topic} addressed to {recipient_name} from {sender_name} using the following keywords: {keywords}")

    # เรียกใช้งาน OpenAI API เพื่อสร้างอีเมล
    response = openai.Completion.create(
        engine="text-davinci-003",
        prompt=prompt,
        max_tokens=2048,  # สามารถปรับตามความต้องการ
        n=1,
        stop=None,
        temperature=0.3
    )
    
    email_text = response["choices"][0]["text"]
    
    # ใช้ฟังก์ชันเพื่อจัดรูปแบบข้อความ
    formatted_email_text = format_email_text(email_text)

    # ส่งผลลัพธ์เป็น JSON กลับไปยัง PyQt5
    return jsonify({'email_text': formatted_email_text})

# ... (เพิ่มส่วนที่ไม่เกี่ยวข้องได้ที่นี่)

if __name__ == '__main__':
    port = int(os.environ.get('PORT', 5000))
    app.run(port=port, debug=True, use_reloader=False)

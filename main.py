import openai
from PyQt5.QtWidgets import QWidget, QApplication, QLabel, QLineEdit, QComboBox, QPushButton, QVBoxLayout, QInputDialog
import sys
import requests
class EmailGenerator(QWidget):
    def __init__(self):
        super().__init__()
        openai.api_key = "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"
        # Create widgets
        self.setWindowTitle("Email Generator by Open AI")
        self.resize(800, 400)
        self.recipient_label = QLabel("Recipient's name:")
        self.recipient_edit = QLineEdit()
        self.sender_label = QLabel("Sender's name:")
        self.sender_edit = QLineEdit()
        self.keywords_label = QLabel("Keywords:")
        self.keywords_edit = QLineEdit()
        self.topic_label = QLabel("Topic:")
        self.topic_edit = QLineEdit()
        self.language_label = QLabel("Language:")
        self.language_combo = QComboBox()
        self.language_combo.addItem("Japanese")
        self.language_combo.addItem("English")
        self.max_tokens_button = QPushButton("Set max_tokens")
        self.n_button = QPushButton("Set n")
        self.stop_button = QPushButton("Set stop")
        self.temperature_button = QPushButton("Set temperature")
        self.api_key_button = QPushButton("Set API Key")
        self.generate_button = QPushButton("Generate Email")
        self.result_label = QLabel()
        
        self.max_tokens_button.clicked.connect(self.set_max_tokens)
        self.n_button.clicked.connect(self.set_n)
        self.stop_button.clicked.connect(self.set_stop)
        self.temperature_button.clicked.connect(self.set_temperature)
        self.api_key_button.clicked.connect(self.set_api_key)

        # Create layout and add widgets
        self.layout = QVBoxLayout()
        self.layout.addWidget(self.recipient_label)
        self.layout.addWidget(self.recipient_edit)
        self.layout.addWidget(self.sender_label)
        self.layout.addWidget(self.sender_edit)
        self.layout.addWidget(self.keywords_label)
        self.layout.addWidget(self.keywords_edit)
        self.layout.addWidget(self.topic_label)
        self.layout.addWidget(self.topic_edit)
        self.layout.addWidget(self.language_label)
        self.layout.addWidget(self.language_combo)
       
        self.layout.addWidget(self.generate_button)
        self.layout.addWidget(self.result_label)
        self.setLayout(self.layout)
        
        self.generate_button.clicked.connect(self.generate_email)
        self.show()
        # Set default values
        self.max_tokens = 2048
        self.n = 1
        self.stop = None
        self.temperature = 0.3
        self.api_key = "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"

    def set_max_tokens(self):
        # code to set max_tokens value
        new_value, ok = QInputDialog.getInt(self, "Set max_tokens", "Enter new value for max_tokens:")
        if ok:
            self.max_tokens = new_value
        pass
    def set_n(self):
        # code to set n value
       
        new_value, ok = QInputDialog.getInt(self, "Set n", "Enter new value for n:")
        if ok:
            self.n = new_value
        pass
    def set_stop(self):
        # code to set stop value
        new_value, ok = QInputDialog.getText(self, "Set stop", "Enter new value for stop:")
        if ok:
            self.stop = new_value
        pass
    def set_temperature(self):
        # code to set temperature value
        new_value, ok = QInputDialog.getDouble(self, "Set temperature", "Enter new value for temperature:")
        if ok:
            self.temperature = new_value
        pass
    def set_api_key(self):
        # code to set api key value
        new_value, ok = QInputDialog.getText(self, "Set API Key", "Enter new value for API Key:")
        if ok:
            self.api_key = new_value
        pass
    
    def generate_email(self):
        recipient_name = self.recipient_edit.text()
        sender_name = self.sender_edit.text()
        keywords = self.keywords_edit.text()
        topic = self.topic_edit.text()
        language = self.language_combo.currentText()
    
        if language == "Japanese":
            prompt = (f"{sender_name}から{recipient_name}に宛てた『{topic}』についてのメールを、以下のキーワードを使って書いてください: {keywords}")
        else:
            prompt = (f"Write an email about {topic} addressed to {recipient_name} from {sender_name} using the following keywords: {keywords}")
    
        url = 'http://localhost:5000/generate_email'  # แก้ไข URL ตามที่คุณใช้
        data = {
            'recipient_name': recipient_name,
            'sender_name': sender_name,
            'keywords': keywords,
            'topic': topic,
            'language': language
        }
        response = requests.post(url, data=data)

        # แสดงผลลัพธ์จากแอป Flask ใน result_label
        if response.status_code == 200:
            email_text = response.text
            self.result_label.setText(email_text)
        else:
            self.result_label.setText("Error: Unable to generate email")    
        response = openai.Completion.create(
            engine="text-davinci-003",
            prompt=prompt,
            max_tokens=self.max_tokens,
            n =self.n,
            stop=self.stop,
            temperature=self.temperature
        )
        email_text = response["choices"][0]["text"]
        self.result_label.setText(email_text)
if __name__ == '__main__':
    app = QApplication(sys.argv)
    email_generator = EmailGenerator()
    email_generator.show()  # แสดงหน้าต่าง GUI
    sys.exit(app.exec_())        
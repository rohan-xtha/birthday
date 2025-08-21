from PyQt5.QtWidgets import QApplication, QWidget, QLabel, QPushButton
from PyQt5.QtGui import QPixmap, QMovie, QFont
from PyQt5.QtCore import Qt, QUrl
from PyQt5.QtMultimedia import QMediaPlayer, QMediaContent
import sys
import os

# ================= QUIZ DATA =================
quiz = [
    {"question": "Does Dad love listening to news more than music? 🤔",
     "options": ["Yes", "No"], "answer": "Yes"},
    {"question": "Which cake flavor does Dad prefer? 🎂",
     "options": ["Vanilla", "Chocolate", "Strawberry", "Carrot"], "answer": "Chocolate"},
    {"question": "Has Dad ever danced at his birthday party? 💃",
     "options": ["Yes", "No"], "answer": "Yes"},
    {"question": "Dad's favorite child 😍:", "options": [
        "Shreya", "Shishir"], "answer": "Shreya"},
    {"question": "Does Dad miss his child? 🥹",
     "options": ["Yes", "No"], "answer": "Yes"},
    {"question": "What makes Dad happy? 😊",
     "options": ["His family", "Chai", "Beer", "Gifts"], "answer": "His family"},
]


class BirthdayQuiz(QWidget):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("🎉 Birthday Quiz for Dad 🎉")
        self.setFixedSize(800, 600)
        self.score = 0
        self.current_q = 0
        self.option_buttons = []
        
        # ================= MUSIC PLAYER =================
        self.music_player = QMediaPlayer()
        music_path = os.path.join(os.path.dirname(__file__), "birthday.mp3")
        if os.path.exists(music_path):
            self.music_player.setMedia(QMediaContent(QUrl.fromLocalFile(music_path)))
            self.music_player.setVolume(50)  # Set volume to 50%
            self.music_player.play()

        # ================= BACKGROUND =================
        self.bg_label = QLabel(self)
        bg_path = os.path.join(os.path.dirname(__file__), "birthday.jpg")
        pixmap = QPixmap(bg_path)
        self.bg_label.setPixmap(pixmap.scaled(800, 600))
        self.bg_label.setGeometry(0, 0, 800, 600)

        # ================= TITLE =================
        self.title_label = QLabel("🎉 Birthday Quiz for Dad 🎉", self)
        self.title_label.setStyleSheet(
            "color: white; background: transparent;")
        self.title_label.setFont(QFont("Arial", 22, QFont.Bold))
        self.title_label.setGeometry(200, 20, 400, 50)
        self.title_label.setAlignment(Qt.AlignCenter)

        # ================= CAKE IMAGE =================
        self.cake_label = QLabel(self)
        cake_path = os.path.join(os.path.dirname(__file__), "cake.png")
        cake_pixmap = QPixmap(cake_path)
        self.cake_label.setPixmap(
            cake_pixmap.scaled(150, 150, Qt.KeepAspectRatio))
        self.cake_label.setGeometry(325, 80, 150, 150)

        # ================= QUESTION =================
        self.question_label = QLabel("", self)
        self.question_label.setWordWrap(True)
        self.question_label.setGeometry(50, 250, 700, 100)
        self.question_label.setFont(QFont("Arial", 18, QFont.Bold))
        self.question_label.setStyleSheet(
            "color: white; background: transparent;")
        self.question_label.setAlignment(Qt.AlignCenter)

        # ================= FEEDBACK =================
        self.feedback_label = QLabel("", self)
        self.feedback_label.setGeometry(200, 460, 400, 30)
        self.feedback_label.setFont(QFont("Arial", 14, QFont.Bold))
        self.feedback_label.setStyleSheet(
            "color: yellow; background: transparent;")
        self.feedback_label.setAlignment(Qt.AlignCenter)

        # ================= NEXT BUTTON =================
        self.next_btn = QPushButton("Next", self)
        self.next_btn.setGeometry(340, 500, 120, 40)
        self.next_btn.setStyleSheet("""
            QPushButton {
                background-color: #2196F3;
                color: white;
                font-size: 14px;
                font-weight: bold;
                border-radius: 10px;
                padding: 8px;
            }
            QPushButton:hover {
                background-color: #1976D2;
            }
        """)
        self.next_btn.clicked.connect(self.next_question)

        # Start quiz
        self.show_question()

    # ================= SHOW QUESTION =================
    def show_question(self):
        # Remove old buttons
        for btn in self.option_buttons:
            btn.hide()
            btn.deleteLater()
        self.option_buttons.clear()

        q = quiz[self.current_q]
        self.question_label.setText(q["question"])
        self.feedback_label.setText("")

        # Dynamically create buttons (centered)
        btn_width, btn_height = 140, 40
        spacing = 20
        num_options = len(q["options"])
        total_width = num_options * btn_width + (num_options - 1) * spacing
        start_x = (800 - total_width) // 2
        y_pos = 400

        for i, option in enumerate(q["options"]):
            btn = QPushButton(option, self)
            btn.setGeometry(start_x + i * (btn_width + spacing),
                            y_pos, btn_width, btn_height)
            btn.setStyleSheet("""
                QPushButton {
                    background-color: #4CAF50;
                    color: white;
                    font-size: 14px;
                    font-weight: bold;
                    border-radius: 10px;
                    padding: 8px;
                }
                QPushButton:hover {
                    background-color: #45a049;
                }
            """)
            btn.clicked.connect(
                lambda checked, ans=option: self.check_answer(ans))
            btn.show()
            self.option_buttons.append(btn)

    # ================= CHECK ANSWER =================
    def check_answer(self, ans):
        if ans == quiz[self.current_q]["answer"]:
            self.score += 1
            self.feedback_label.setText("✅ Correct!")
        else:
            self.feedback_label.setText("❌ Wrong!")

    # ================= NEXT QUESTION =================
    def next_question(self):
        self.current_q += 1
        if self.current_q < len(quiz):
            self.show_question()
        else:
            self.show_results_with_gif()

    # ================= SHOW RESULTS WITH GIF =================
    def show_results_with_gif(self):
        # Hide quiz-specific widgets but keep background
        self.question_label.hide()
        self.feedback_label.hide()
        self.next_btn.hide()
        self.cake_label.hide()
        for btn in self.option_buttons:
            btn.hide()

        # Result text
        result_label = QLabel(
            f"You got {self.score} out of {len(quiz)} correct! 🎂", self)
        result_label.setFont(QFont("Arial", 20, QFont.Bold))
        result_label.setStyleSheet("color: white; background: transparent;")
        result_label.setGeometry(150, 50, 500, 50)
        result_label.setAlignment(Qt.AlignCenter)
        result_label.show()

        # End button
        end_btn = QPushButton("End", self)
        end_btn.setGeometry(340, 500, 120, 40)
        end_btn.setStyleSheet("""
            QPushButton {
                background-color: #ff6961;
                color: white;
                font-size: 14px;
                font-weight: bold;
                border-radius: 10px;
                padding: 8px;
            }
            QPushButton:hover {
                background-color: #e53935;
            }
        """)
        end_btn.clicked.connect(self.close_app)
        end_btn.show()

        # GIF above End button
        gif_label = QLabel(self)
        gif_width, gif_height = 500,500
        gif_x = (1000 - gif_width) // 2
        gif_y = end_btn.y() - gif_height - 20
        gif_label.setGeometry(gif_x, gif_y, gif_width, gif_height)
        gif_path = os.path.join(os.path.dirname(__file__), "birthday.gif")
        movie = QMovie(gif_path)
        gif_label.setMovie(movie)
        movie.start()
        gif_label.show()

    # ================= CLOSE APP =================
    def close_app(self):
        if hasattr(self, 'music_player'):
            self.music_player.stop()
        self.close()


# ================= RUN APP =================
if __name__ == "__main__":
    app = QApplication(sys.argv)
    quiz_app = BirthdayQuiz()
    quiz_app.show()
    sys.exit(app.exec_())

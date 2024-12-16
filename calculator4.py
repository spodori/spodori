import tkinter as tk
import math

# 스타일 설정
LARGE_FONT_STYLE = ("Arial", 24, "bold")
SMALL_FONT_STYLE = ("Arial", 16)
DIGITS_FONT_STYLE = ("Arial", 20, "bold")
DEFAULT_FONT_STYLE = ("Arial", 18)

OFF_WHITE = "#F8FAFF"
WHITE = "#FFFFFF"
LIGHT_BLUE = "#CCEDFF"
LIGHT_GRAY = "#F5F5F5"
LABEL_COLOR = "#25265E"

# 진공 유전율 (ε₀)
EPSILON_0 = 8.854187817e-12  # 단위: F/m (패럿/미터)


class Calculator:
    def __init__(self):
        self.window = tk.Tk() 
	# Tkinter 윈도우 생성
        self.window.title("Calculator")  
	# 창 제목
        self.window.geometry("375x667") 
	 # 창 크기
        self.window.resizable(0, 0) 
	# 크기 조절 불가

        self.total_expression = "" 
	 # 전체 계산식 (사용자가 입력한 값)
        self.current_expression = "" 
	 # 현재 입력식 (현재 입력값)

        self.display_frame = self.create_display_frame()  
	# 디스플레이 프레임 생성
        self.total_label, self.label = self.create_display_labels() 
	 # 디스플레이 레이블 생성

        # 숫자 버튼 위치
        self.digits = {
            7: (1, 1), 8: (1, 2), 9: (1, 3),
            4: (2, 1), 5: (2, 2), 6: (2, 3),
            1: (3, 1), 2: (3, 2), 3: (3, 3),
            0: (4, 2), '.': (4, 1)
        }
        
        # 연산자 매핑 (기호 변경)
        self.operations = {"/": "\u00F7", "*": "\u00D7", "-": "-", "+": "+"}

        # 버튼 프레임 생성
        self.buttons_frame = self.create_buttons_frame()
        self.create_digit_buttons() 
	 # 숫자 버튼 생성
        self.create_operator_buttons() 
	 # 연산자 버튼 생성
        self.create_special_buttons() 
	 # 특별한 버튼 생성 (예: 점전하 전기장 계산)

        # 버튼 행과 열 설정 (비율을 맞추기 위해)
        self.buttons_frame.rowconfigure(0, weight=1)
        for i in range(1, 5):
            self.buttons_frame.rowconfigure(i, weight=1)
            self.buttons_frame.columnconfigure(i, weight=1)

    def create_display_frame(self):
        # 디스플레이 영역을 위한 프레임 생성
        frame = tk.Frame(self.window, height=221, bg=LIGHT_GRAY)
        frame.pack(expand=True, fill="both")
        return frame

    def create_display_labels(self):
        # 전체 수식 레이블 (상단에 표시)
        total_label = tk.Label(self.display_frame, text=self.total_expression, anchor=tk.E,
                               bg=LIGHT_GRAY, fg=LABEL_COLOR, padx=24, font=SMALL_FONT_STYLE)
        total_label.pack(expand=True, fill="both")

        # 현재 수식 레이블 (하단에 표시)
        label = tk.Label(self.display_frame, text=self.current_expression, anchor=tk.E,
                         bg=LIGHT_GRAY, fg=LABEL_COLOR, padx=24, font=LARGE_FONT_STYLE)
        label.pack(expand=True, fill="both")

        return total_label, label

    def create_buttons_frame(self):
        # 버튼들이 배치될 프레임 생성
        frame = tk.Frame(self.window)
        frame.pack(expand=True, fill="both")
        return frame

    def create_digit_buttons(self):
        # 숫자 버튼 생성
        for digit, grid_value in self.digits.items():
            button = tk.Button(self.buttons_frame, text=str(digit), bg=WHITE, fg=LABEL_COLOR,
                               font=DIGITS_FONT_STYLE, borderwidth=0,
                               command=lambda x=digit: self.add_to_expression(x)) 
				 # 버튼 누르면 수식에 숫자 추가
            button.grid(row=grid_value[0], column=grid_value[1], sticky=tk.NSEW)

    def create_operator_buttons(self):
        # 연산자 버튼 생성
        for i, (operator, symbol) in enumerate(self.operations.items()):
            button = tk.Button(self.buttons_frame, text=symbol, bg=OFF_WHITE, fg=LABEL_COLOR,
                               font=DEFAULT_FONT_STYLE, borderwidth=0,
                               command=lambda x=operator: self.append_operator(x)) 
				 # 연산자 추가
            button.grid(row=i, column=4, sticky=tk.NSEW)

    def create_special_buttons(self):
        # C 버튼 (초기화), = 버튼 (결과 계산), 전기장 버튼 생성
        self.create_clear_button()
        self.create_equals_button()
        self.create_electric_field_button() 
	 # 점전하 전기장 계산 버튼 생성

    def create_clear_button(self):
        # C 버튼 (초기화)
        button = tk.Button(self.buttons_frame, text="C", bg=OFF_WHITE, fg=LABEL_COLOR,
                           font=DEFAULT_FONT_STYLE, borderwidth=0, command=self.clear) 
	 # 수식 초기화
        button.grid(row=0, column=1, columnspan=2, sticky=tk.NSEW)

    def create_equals_button(self):
        # = 버튼 (수식 평가)
        button = tk.Button(self.buttons_frame, text="=", bg=LIGHT_BLUE, fg=LABEL_COLOR,
                           font=DEFAULT_FONT_STYLE, borderwidth=0, command=self.evaluate)
        button.grid(row=4, column=3, columnspan=2, sticky=tk.NSEW)

    def create_electric_field_button(self):
        # 점전하 전기장 계산 버튼 생성
        button = tk.Button(self.buttons_frame, text="E=Q/4πεr²", bg=OFF_WHITE, fg=LABEL_COLOR,
                           font=DEFAULT_FONT_STYLE, borderwidth=0, command=self.calculate_electric_field)
        button.grid(row=5, column=1, columnspan=3, sticky=tk.NSEW)

    def add_to_expression(self, value):
        # 숫자나 기호를 현재 수식에 추가
        self.current_expression += str(value)
        self.update_label()

    def append_operator(self, operator):
        # 연산자를 수식에 추가
        if self.current_expression:
            self.total_expression += self.current_expression + operator
            self.current_expression = ""
            self.update_total_label()
            self.update_label()

    def clear(self):
        # 수식 초기화
        self.current_expression = ""
        self.total_expression = ""
        self.update_total_label()
        self.update_label()

    def evaluate(self):
        # 수식을 평가하여 결과를 계산
        self.total_expression += self.current_expression
        try:
            self.current_expression = str(eval(self.total_expression)) 
		 # 수식을 실행
            self.total_expression = ""
        except Exception as e:
            self.current_expression = "Error" 
		 # 예외 처리
        finally:
            self.update_total_label()
            self.update_label()

    def calculate_electric_field(self):
        # 점전하 전기장 계산 (Q와 r을 입력받음)
        input_window = tk.Toplevel(self.window)
        input_window.title("Electric Field")  # 팝업 창 제목
        input_window.geometry("300x200")

        tk.Label(input_window, text="Q (전하량, C):").pack(pady=5)
        q_entry = tk.Entry(input_window)  # 전하량 입력
        q_entry.pack(pady=5)

        tk.Label(input_window, text="r (거리, m):").pack(pady=5)
        r_entry = tk.Entry(input_window)  # 거리 입력
        r_entry.pack(pady=5)

        def compute():
            # 전기장 계산
            try:
                Q = float(q_entry.get())  # 전하량
                r = float(r_entry.get())  # 거리
                if r == 0:
                    result = "Error (r=0)"  # r이 0일 경우 오류
                else:
                    # 전기장 공식 E = Q / (4 * π * ε₀ * r²)
                    E = Q / (4 * math.pi * EPSILON_0 * r**2)
                    result = f"{E:.2e} N/C"  # 결과를 과학적 표기법으로 출력
                self.current_expression = result
                self.update_label()
                input_window.destroy()  # 팝업 창 닫기
            except Exception as e:
                self.current_expression = "Error"  # 오류 처리
                self.update_label()
                input_window.destroy()

        tk.Button(input_window, text="Calculate", command=compute).pack(pady=10)  
	# 계산 버튼

    def update_total_label(self):
        # 전체 수식 레이블 업데이트
        self.total_label.config(text=self.total_expression)

    def update_label(self):
        # 현재 수식 레이블 업데이트
        self.label.config(text=self.current_expression[:20]) 
	 # 수식 길이가 길어지면 20자리까지만 표시

    def run(self):
        # 프로그램 실행
        self.window.mainloop()


if __name__ == "__main__":
    calc = Calculator()  # 계산기 객체 생성
    calc.run()  # 계산기 실행


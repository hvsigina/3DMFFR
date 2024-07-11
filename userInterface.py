import numpy as np
import gradio as gr

def sepia(image):
    sepia_filter = np.array([
        [0.393, 0.769, 0.189], 
        [0.349, 0.686, 0.168], 
        [0.272, 0.534, 0.131]
    ])
    sepia_img = image.dot(sepia_filter.T)
    sepia_img /= sepia_img.max()
    return sepia_img


def test(name, intensity):
    return "HELLO " + name +"!" * int(intensity)

#text inputs
demo = gr.Interface(
    fn = test,
    inputs = ["text",gr.Slider(value=4, minimum=2, maximum=8, step=2)],
    outputs=[gr.Textbox(label="GREETINGS", lines=3)],
)

#image inputs
imgDemo = gr.Interface(
    fn = sepia,
    inputs = [gr.Image()],
    outputs= [gr.Image()],
)

#text inputs
def calculator(num1, operation, num2):
    if operation == "add":
        return num1 + num2
    elif operation == "subtract":
        return num1 - num2
    elif operation == "multiply":
        return num1 * num2
    elif operation == "divide":
        if num2 == 0:
            raise gr.Error("Cannot divide by zero!")
        return num1 / num2
    
calcDemo = gr.Interface(
    calculator,
    [
        "number",
        gr.Radio(["add","subtract","multiply","divide"]),
        "number"
    ],
    "number",
    examples=[
        [45,"add",89],
    ],
    title = "CALC",
    description="Here's a sample toy calculator."
)

calcDemo.launch()


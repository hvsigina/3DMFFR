import numpy as np
import gradio as gr


image_count = 0

def change_tab(i):
    return gr.Tabs(selected=i)

def goto_step2():
    return change_tab(2)

def goto_step3():
    return change_tab(3)

def goto_step4():
    return change_tab(4)

def galFunc():
    global image_count
    image_count = image_count+1
    return

demo = gr.Blocks()

with demo:
    gr.Markdown(
        """
    # 3DMFFR
    3D Face Reconstruction from one or Multiple 2D images, using cuda-accelerated renderer.
    """
    )
    with gr.Tabs() as tabs:
        with gr.TabItem("Step 1: Faceset extraction", id=1 ):
            with gr.Row():
                text_input1 = gr.Textbox(placeholder="dummy")
                text_output1 = gr.Textbox(placeholder="dummy")
                text_button1 = gr.Button("dumbo")
                
            with gr.Row():
                text_input2 = gr.Textbox(placeholder="dummy")
                text_output2 = gr.Textbox(placeholder="dummy")
            text_button2 = gr.Button("CONTINUE TO STEP 2")
        with gr.TabItem("Step 2: Landmarks creation and options selection", id=2):
            with gr.Row():
                image_input3 = gr.Image()
                image_output3 = gr.Image()
                image_button3 = gr.Button("Flip")
            with gr.Row():
                radio1 = gr.Radio(choices=["Jaffa","Guffa","Laffa","Ruffa"])
            radio_button = gr.Button("CONINUE TO STEP 3")
        with gr.TabItem("Step 3: Training", id=3):
            with gr.Row():
                image_input9 = gr.Image()
                gallery = gr.Gallery()
            final_button = gr.Button("CONTINUE TO STEP 4")
        with gr.TabItem("Step 4: Object Creation", id=4):
            textoutputfinal = gr.Textbox(value=image_count)
            
            text_button2.click()
    text_button2.click(goto_step2)
    
    radio_button.click(goto_step3)
    
    final_button.click(goto_step4)
    
    gallery.upload(galFunc)
    
demo.launch()

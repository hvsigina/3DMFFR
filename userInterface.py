
from ast import Interactive, Lambda
from logging import PlaceHolder
import numpy as np
import gradio as gr
import old.faceset as faceset 
import configs.config_mffr

config1 = configs.config_mffr.config1("Tab1")

def tab1_config_set(imageCount,maxImageCount,facesetResolution,faceType):
    
    config1.tab1_set_parameters(imageCount=imageCount,maxImageCount=maxImageCount,facesetResolution=facesetResolution,faceType=faceType)
    return True

def tab1_input_gallery_update(upload,gallery,count):
    
    if gallery is None:
        img_list = []
    else:
        img_list = gallery
    
    img_list.append(upload)
    return gr.Image(value=None),gr.Gallery(value=img_list),str(int(count)+1)

def tab1_advanced_settings(value, evt: gr.EventData):
    #Check if checkbox is enabled or not
    if value:
        config1.tab1_set_parameters(advancedSettings=True)
        return [gr.Slider(interactive=False),gr.Slider(interactive=False),gr.Slider(interactive=True),gr.Slider(interactive=True),gr.Radio(interactive=True)]
    else:
        config1.tab1_set_parameters(advancedSettings=False)
        return [gr.Slider(interactive=True),gr.Slider(interactive=True),gr.Slider(interactive=False),gr.Slider(interactive=False),gr.Radio(interactive=False)]

def tab1_faceset_extract(gallery,imageCount,advfacesetImagesMax,advfacesetResolution,facesetImagesMax,facesetResolution,faceType):
    
    #set config params
    if config1.tab1_get_advancedSettings() == None or not config1.tab1_get_advancedSettings() :
        tab1_config_set(imageCount=imageCount,maxImageCount=facesetImagesMax,facesetResolution=facesetResolution,faceType=faceType)
    else:
        tab1_config_set(imageCount=imageCount,maxImageCount=advfacesetImagesMax,facesetResolution=advfacesetResolution,faceType=faceType)


    #Run faceset extract task
    locations = []
    extracted_imgs = []
    img_list = gallery
    iter = 0
    
    if faceType=="face":
        faceTyp = 0
    elif faceType=="wholeface":
        faceTyp = 4
    elif faceType=="head":
        faceTyp = 8

    for img in img_list: 
        iter += 1
        location = faceset.faceset_create(img,faceTyp,iter,config1.tab1_get_facesetResolution())
        maxCount = 0
        for loc in location:
            maxCount += 1
            if maxCount<=int(config1.tab1_get_maxImageCount()) :
                locations.append(loc)
    
    
                             
    #Faceset gallery and step2 button clickable
    return [gr.Gallery(value=locations, interactive=False),gr.Button(interactive=True)]

def tab1_faceset_delete(facesetImageGalleryTab1,deleteImageCount):
    #Delete chosen image from images
    imGallery = facesetImageGalleryTab1
    if not (deleteImageCount is None) and not (facesetImageGalleryTab1 is None):
        
        imCount = int(deleteImageCount)
    
        if imCount > 0 and imCount <= len(imGallery):
            del imGallery[imCount-1]
            imCount-=1
        
    return [gr.Gallery(value=imGallery),"0"]

step1_str="Step 1: Faceset extraction"
step2_str="Step 2: Landmarks creation and options selection"
step3_str="Step 3: Training"
step4_str="Step 4: Object Creation"

demo = gr.Blocks()

with demo:
    gr.Markdown(
        """
    # **3DMFFR : 3-DIMENSIONAL MULTI FRAME FACE RECONSTRUCTION**
    *3D Face Reconstruction from one or Multiple 2D images, using cuda-accelerated renderer.*
    """
    )
    #BODY
    with gr.Tabs() as tabs:

        with gr.Tab(step1_str, id=1) as tab1:
            gr.Markdown(
            """ 
            ## """ + step1_str + """
            """)
            with gr.Row():
                with gr.Column(scale=1):
                    addImageTab1 = gr.Image(scale=2,sources="upload",label="Upload image/images/video",interactive=True)
                    addedImageCountTab1 = gr.Textbox(scale=1,value=0,label="Uploaded Images count",interactive=False)
                with gr.Column(scale=6):
                    inputImageGalleryTab1 = gr.Gallery(scale=3,label="Uploaded Images",interactive=False)
            with gr.Row():
                with gr.Column(scale=3):
                    facesetImagesMax = gr.Slider(scale=1,minimum=1,maximum=10,step=1,value=1,label="Max No. of Images",info="Choose maximum number of faces to be extracted from uploaded images. Best images will be chosen first.")
                    facesetResolution = gr.Slider(scale=1,minimum=256,maximum=1024,value=256,step=256,label="Faceset Resolution",info="Choose faceset resolution. Extracted faces will be set to the selected resolution. Higher resolutions will need higher VideoMemory. Images lower than selected resolution will be automatically resized to the selected resolution.")
                    facesetType = gr.Radio(scale=1,choices=["face","wholeface","head"],label="Face Type",interactive=True,value="wholeface")
                    
                with gr.Column(scale=1):
                    with gr.Accordion(label="Advanced Options"):
                        gr.Markdown("**Extreme settings intended for high-end GPU's**")
                        advancedSettingsEnableTab1 = gr.Checkbox(value=False,label="Enable",interactive=True)
                        advancedFacesetImagesMax = gr.Slider(minimum=11,maximum=30,value=11,step=1,label="Max No.of Images",info="Choose maximum number of faces to be extracted from uploaded images. Best images will be chosen first.")
                        advancedFacesetResolution = gr.Slider(minimum=1280,maximum=2048,value=1280,step=256,label="Faceset Resolution",info="Choose faceset resolution. Extracted faces will be set to the selected resolution. Higher resolutions will need higher VideoMemory. Images lower than selected resolution will be automatically resized to the selected resolution.")
                        #advancedRenderer = gr.Radio(choices=["CUDA","CPU"],label="Renderer backend",info="CUDA for NVIDIA GPU's")
                    
            with gr.Row():
                facesetExtractButton = gr.Button("FACESET EXTRACT",interactive=True,scale=1)
                facesetExtractProgressBar = gr.Progress(track_tqdm=False)
            with gr.Row():
                with gr.Column(scale=9):
                    facesetImageGalleryTab1 = gr.Gallery(scale=9,label="Faceset Images",interactive=False)
                with gr.Column(scale=1):
                    deleteImageCount = gr.Number(value=0,scale=1,label="Enter image number to be deleted")
                    deleteImageButton = gr.Button("Delete Image",scale=1)
                    nextStepButtonTab1 = gr.Button("STEP 2",scale=3,interactive=False)

        with gr.Tab(step2_str, id=2) as tab2:
            gr.Markdown(
            """ 
            ## """ + step2_str + """
            """)
            back_button2 = gr.Button("Back to "+step1_str)
            with gr.Row():
                image_input3 = gr.Image()
            with gr.Row():
                radio1 = gr.Radio(choices=["Jaffa","Guffa","Laffa","Ruffa"])
            radio_button = gr.Button("CONINUE TO STEP 3")

        with gr.Tab(step3_str, id=3) as tab3:
            gr.Markdown(
            """ 
            ## """ + step3_str + """
            """)
            back_button3 = gr.Button("<<< Back to "+step2_str)
            with gr.Row():
                image_input9 = gr.Image()
                gallery = gr.Gallery()
            final_button = gr.Button("CONTINUE TO STEP 4")

        with gr.Tab(step4_str, id=4) as tab4:
            gr.Markdown(
            """ 
            ## """ + step4_str + """
            """)
            back_button4 = gr.Button("<<<< Back to "+step3_str)
            textoutputfinal = gr.Textbox(value="3")
    
    #initial TABS visibility
    tab1.visible = True
    tab2.visible = False
    tab3.visible = False
    tab4.visible = False
    
    #initial OPTIONS interactivity
    facesetImagesMax.interactive=True
    facesetResolution.interactive=True
    advancedFacesetImagesMax.interactive=False
    advancedFacesetResolution.interactive=False
    #advancedRenderer.interactive=False
    
    #TAB1 FUNCTIONS:
    
    #IMAGE GALLERY FUNC
    addImageTab1.upload(tab1_input_gallery_update,[addImageTab1,inputImageGalleryTab1,addedImageCountTab1],[addImageTab1,inputImageGalleryTab1,addedImageCountTab1])
    
    #FACESET EXTRACTION
    #check if advanced settings are enabled
    facesetExtractButton.click(tab1_faceset_extract,[inputImageGalleryTab1,addedImageCountTab1,advancedFacesetImagesMax,advancedFacesetResolution,facesetImagesMax,facesetResolution,facesetType],[facesetImageGalleryTab1,nextStepButtonTab1])
    
    #ADVANCED SETTINGS
    advancedSettingsEnableTab1.select(tab1_advanced_settings,advancedSettingsEnableTab1,[facesetImagesMax,facesetResolution,advancedFacesetImagesMax,advancedFacesetResolution])

    #DELETE IMAGE FROM FACESET
    deleteImageButton.click(tab1_faceset_delete,[facesetImageGalleryTab1,deleteImageCount],[facesetImageGalleryTab1,deleteImageCount])

    #CHANGING TABS
    #Step 1-->2
    nextStepButtonTab1.click(lambda :gr.Tab(step2_str, id=2, visible=True),None,tab2).then(lambda :gr.Tabs(selected=2), None, tabs).then(lambda :gr.Tab(step1_str, id=1, visible=False),None,tab1)
    #Step 2-->3
    radio_button.click(lambda :gr.Tab(step3_str, id=3, visible=True),None,tab3).then(lambda :gr.Tabs(selected=3), None, tabs).then(lambda :gr.Tab(step2_str, id=2, visible=False),None,tab2)
    #Step 3-->4
    final_button.click(lambda :gr.Tab(step4_str, id=4, visible=True),None,tab4).then(lambda :gr.Tabs(selected=4), None, tabs).then(lambda :gr.Tab(step3_str, id=3, visible=False),None,tab3)
    
    #Step 2-->1
    back_button2.click(lambda :gr.Tab(step1_str, id=1, visible=True),None,tab1).then(lambda :gr.Tabs(selected=1), None, tabs).then(lambda :gr.Tab(step2_str, id=2, visible=False),None,tab2)
    #Step 3-->2
    back_button3.click(lambda :gr.Tab(step2_str, id=2, visible=True),None,tab2).then(lambda :gr.Tabs(selected=2), None, tabs).then(lambda :gr.Tab(step3_str, id=3, visible=False),None,tab3)
    #Step 4-->3
    back_button4.click(lambda :gr.Tab(step3_str, id=3, visible=True),None,tab3).then(lambda :gr.Tabs(selected=3), None, tabs).then(lambda :gr.Tab(step4_str, id=4, visible=False),None,tab4)
    
    
demo.launch()

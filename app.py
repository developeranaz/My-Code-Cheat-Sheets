import warnings
warnings.filterwarnings('ignore')
import ipywidgets as widgets
from IPython.display import display, clear_output
####### please don't delete below line ########
# Author https://github/developeranaz
####### Please don't delete above line ########
# support me star my repo

# Image Widget
file = open("Aria2Rclone.jpg", "rb")
image = file.read()
image_headline = widgets.Image(
                    value=image,
                    format='jpg',
                    width='400'
                )
label_headline = widgets.Label(
                    #value='Aria2Mega',
                    #style={'description_width': 'large'}
                )
vbox_headline = widgets.VBox([label_headline])


# magnet/url
toruri = widgets.Text(placeholder='http://ser.ver.mp4 OR magnet:?xt=ur..annonce' ,flex_flow='column' ,align_items='center')

cloudname = widgets.Dropdown(
    options=['selectone',
'0unlimited-gd4', 
'1sundaran1', 
'2sundaran2', 
'3sundaran3', 
'4sundaran4', 
'Fauthor', 
'JinjaMega', 
'Pingme998', 
'sundaranmega', 
'zunlimited-gd4-s1', 
'zunlimited-gd4-s2', 
'zunlimited-gd4-s3', 
'zunlimited-gd4-s4' 
            ],
    value='selectone',
    description='cloudname:',
    disabled=False,
)


# number of threads
threats = widgets.IntSlider(
            value=10, # default value
            min=2, 
            max=12,
            step=1,
            style={'description_width': 'initial', 'handle_color': '#f84834'} 
        )

# button down and up
from ipywidgets import Button
button_send= Button(description='START UPLOAD',button_style='danger' ,border='solid',width='50%',tooltip='Send')
button_send.layout.align_items = 'center'
output = widgets.Output()
def on_button_clicked(event):
    with output:
        clear_output()
        ! echo "$toruri" >/urlraw
        ! cat urlraw |sed 's/(/\n/g' |sed 's/,/\n/g' |grep value |sed 's/value=//g' |sed "s/'//g" |sed 's/ /\n/g' |grep 'http\|https\|magnet' >/urls.txt
        #rclone version
        %mkdir /home/{cloudname.value}
        %cd /home/{cloudname.value}
        ! rclone copy /Essential-Files/d {cloudname.value}:
        ! touch /progression.log
        clear_output()
        ! echo "Your File is downloading.. don't close this tab"
        ! while sleep 60; do clear; cat /progression.log | grep ETA: |tail -1; if grep --quiet 'SEED\|(OK):download completed' '/progression.log'; then pkill aria2c; fi; done & aria2c --dir=/home/{cloudname.value} --input-file=/urls.txt --max-concurrent-downloads=1 --connect-timeout=60 --max-connection-per-server="{threats.value}" --split="{threats.value}" --min-split-size=1M --human-readable=true --download-result=full --file-allocation=none >/progression.log
        ! echo 'Download Complete'
        ! echo 'Uploading Started'
        ! rclone copy --progress --stats-one-line /home/{cloudname.value} {cloudname.value}:
        print(f"Your file uploaded to {cloudname.value} at {threats.value} x threads")
button_send.on_click(on_button_clicked)
vbox_result = widgets.VBox([button_send, output])

import ipywidgets as widgets


link01 = widgets.HTML(
    value="<font color='lime'><center><h6>DONATE BTC: 1J48LksQNiASuj48nwYATXdFzQSwdrnx7c <br><a href=https://github.com/developeranaz target='_blank'>DEVELOPERANAZ </a> <br><a href=https://github.com/developeranaz/Aria2-Rclone-Remote-Uploader-HEROKU target='_blank'>Trouble Uploading ? Readme </a><br><a href=https://github.com/developeranaz/Aria2-Rclone-Remote-Uploader-HEROKU/issues target='_blank'>Issues can be reported here </a>",
)



text_1 = widgets.HTML(value="<h4>Thread or Max connection Per download</h4>")
line1 = widgets.HTML(value="<hr>")

text_4= widgets.HTML(value="<h4>Paste magnet/direct links here</h4>")
text_5= widgets.HTML(value="<h4>Select your Remote</h4>")
vbox_text = widgets.VBox([image_headline, line1, text_4, toruri, line1, text_1, threats, line1, text_5, cloudname, line1,line1, vbox_result, link01])
page = widgets.HBox([vbox_headline, vbox_text])
display(page)

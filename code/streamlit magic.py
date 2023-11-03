import streamlit as st
from PIL import Image, ImageFont, ImageDraw
import gpt_2_simple as gpt2

st.title("Magic card maker")

sess = gpt2.start_tf_sess()
gpt2.load_gpt2(sess, checkpoint = 'latest', run_name='run_2', checkpoint_dir = 'checkpoint')

def generate_text(prompt):
    return gpt2.generate(sess, temperature=.5, prefix= prompt, length=45, top_k=10, nsamples=1, run_name= 'run_2', model_dir= 'models/124M', return_as_list=True)[0]

def card_image(color, card_name, cardtext, subtype, type, power, toughness, iscreature = False):
    if iscreature == True: 
        im = Image.open(f"{color}creature.png")
        title = ImageDraw.Draw(im)
        beleren = ImageFont.truetype('Beleren2016-bold.ttf', size = 35)
        #adding cardname
        title.text((48, 48), f'{card_name}', (0,0,0), font=beleren)
        #making rules text
        title.text((68, 525), f'{cardtext}', (0,0,0), font = ImageFont.truetype('Beleren2016-Bold.ttf', size= 20))
        #adding P/T
        title.text((467,717), f'{power}/{toughness}', (0,0,0),font = beleren )
        #adding type/subtype
        title.text((42,458), f'{type} - {subtype}', (0,0,0), font = beleren)
        return im
    else:
        im = Image.open(f"{color}.png")
        title = ImageDraw.Draw(im)
        beleren = ImageFont.truetype('Beleren2016-bold.ttf', size = 35)
        #adding cardname
        title.text((48, 48), f'{card_name}', (0,0,0), font=beleren)
        #making rules text
        title.text((68, 525), f'{cardtext}', (0,0,0), font = ImageFont.truetype('Beleren2016-Bold.ttf', size= 20))
        #no P/T for non creatures
        #adding type/subtype
        title.text((50,458), f'{type} - {subtype}', (0,0,0), font = beleren)
        return im
    


cname = st.text_input(label= 'Card Name', max_chars=20)

ccolor = st.text_input(label = 'Card Color(white, blue, black, red, or green)', max_chars=20)

ctype = st.text_input(label= 'Card Type', max_chars=20)

csubtype = st.text_input(label= 'Card Subtype', max_chars=20)

ccreature = st.checkbox(label= 'Is this a creature?')

cpower = st.number_input(label= 'Power(if creature)', min_value= 0)

ctoughness = st.number_input(label= 'Toughness(if creature)', min_value= 0)


if st.button('make a card'):
    st.image(card_image(color = ccolor, card_name= cname, cardtext=generate_text('When [CARDNAME] enters the battlefield'),subtype= csubtype, type=ctype, power=cpower, toughness= ctoughness, iscreature= ccreature))
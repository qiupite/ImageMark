class ImageMark(object):
    def __init__(self):
        self.margin=5
        pass
    def get_mark_position(self,img_width,img_height,mark_width,mark_height,position):
        if mark_width+self.margin>=img_width or mark_height+self.margin>=img_height:
            raise Exception('text size bigger than image')
        if position=='bottom_right':
            mark_pos=(img_width-mark_width-self.margin,img_height-mark_height-self.margin)
        elif position=='bottom_left':
            mark_pos=(self.margin,img_height-mark_height-self.margin)
        elif position=='top_left':
            mark_pos=(self.margin,self.margin)
        elif position=='top_right':
            mark_pos=(img_width-mark_width-self.margin,self.margin)
        elif position=='center':
            mark_pos=((img_width-2*self.margin-mark_width)/2,(img_height-2*self.margin-mark_height)/2)
        elif position=='random':
            mark_pos=(random.randint(self.margin,img_width--mark_width-self.margin),random.randint(self.margin,img_height-mark_height-self.margin))
        else:
            print('using default position')
            mark_pos=(self.margin,self.margin)
        return mark_pos

    def get_save_path(self,img_path,marked_path):
        path_lst=img_path.split(os.path.sep)
        img_name=path_lst[-1]
        if marked_path is None:
            marked_path=os.path.sep.join(path_lst[:-1])
        name_lst=img_name.split('.')
        self.marked_img_path=marked_path+os.path.sep+name_lst[0]+'-marked.'+name_lst[1]
        pass
    def mark_text(self,img_path,marked_path=None,text='test_mark',size=20,position='top_left',opacity=0.5):
        self.marked_img_path=None
        if not os.path.exists(img_path):
            raise Exception('file not exists: '+img_path)
        img=Image.open(img_path).convert('RGBA')
        img_width,img_height=img.width,img.height
        # font
        txt_font=ImageFont.truetype('/Library/Fonts/Arial.ttf',size)
        mark_width,mark_height=txt_font.getsize(text)
        
        # mark position
        mark_pos=self.get_mark_position(img_width,img_height,mark_width,mark_height,position)
        
        # make a blank image for the text, initialized to transparent text color
        blank_img = Image.new('RGBA', img.size, (0,0,0,0))
        
        # set text opacity
        opacity=int(opacity*255)
        # get backgroud color
        bg_color=img.getpixel(mark_pos)
        # set text color, different from backgroud
        txt_color=(255-bg_color[0],255-bg_color[1],255-bg_color[2],opacity)
        
        img_draw=ImageDraw.Draw(blank_img)
        img_draw.text(mark_pos,text,font=txt_font,fill=txt_color)
        marked_img = Image.alpha_composite(img, blank_img).convert("RGB")
        
        # save
        self.get_save_path(img_path,marked_path)
        marked_img.save(self.marked_img_path)
        pass
    def batch_mark_text(self,raw_path,marked_path=None,text='test_mark',size=20,position='top_left',opacity=0.5,rm_org=False):
        raw_path=raw_path
        marked_path=marked_path if marked_path else raw_path
        file_lst=glob.glob(raw_path+os.path.sep+'*')
        file_lst=[f for f in file_lst if (f.endswith('.png') or f.endswith('.jpg') or f.endswith('.jpeg'))]
        for raw_img_path in file_lst:
            self.mark_text(raw_img_path,marked_path,text,size,position,opacity)
            if rm_org and self.marked_img_path and os.path.exists(self.marked_img_path):
                os.remove(raw_img_path)
        pass
    def mark_logo(self,img_path,logo_path,marked_path=None,position='top_left',opacity=0.5):
        self.marked_img_path=None
        if not os.path.exists(img_path):
            raise Exception('file not exists: '+img_path)
        if not os.path.exists(logo_path):
            raise Exception('logo image not exists: '+logo_path)
        img=Image.open(img_path)
        logo_img=Image.open(logo_path).convert("RGBA")
        img_width,img_height=img.width,img.height
        mark_width,mark_height=logo_img.width,logo_img.height

        # mark position
        mark_pos=self.get_mark_position(img_width,img_height,mark_width,mark_height,position)
     
        # make a blank image for the text, initialized to transparent text color
        marked_img = Image.new('RGBA', img.size, (0,0,0,0))
        marked_img.paste(img,(0,0))
        marked_img.paste(logo_img,mark_pos,mask=logo_img)
        marked_img=marked_img.convert("RGB")
        
        # save
        self.get_save_path(img_path,marked_path)
        marked_img.save(self.marked_img_path)

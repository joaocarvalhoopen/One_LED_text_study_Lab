# Proj. name:   One LED text study Lab
# Program name: one_led_text_study_lab.py
# Author:       João Nuno Carvalho
# Date:         2021.03.15
# License:      MIT Open Source License
# Description:  This is a program to study and simulate a new idea that I had
#               for a simple way to encode text in a one LED interface. It
#               doesn't require any remembering of a translation table, like
#               Morse Code, because it is a simple mapping. But it is less
#               efficient then Morse Code. It uses 3 levels for the LED,
#               1 - OFF, 2 - Medium amplitude (PWM or resistor) and 3 - Full
#               amplitude. The timing of the sequence can be easily adjusted
#               in the code for a complete simulation study of the timings and
#               of the method. Each character is composed by 3 columns of 5
#               rows each, the display in the LED is made by a scan of the
#               character vertically, from the top to the bottom, one column
#               at at a time. Top to bottom, left to right. And any different
#               order can be easily achieved with a small modification to the
#               code.  
#               In the scan line of the char, it starts LED OFF then if the
#               first pixel of the character is ON it shows yellow FULL ON
#               and it it's is OFF the LED shows Middle amplitude yellow
#               (with some green for better visualization). Then a fast
#               period of separation of LED OFF and then the next pixel is
#               processed. Then when it terminates a column a some what bigger
#               pause of LED OFF, then it start on the next column. When it
#               end the character it will make a bigger LED OFF pause.
#               The full alphabet, the full numerics, the principal math
#               operations, and some language signs are mapped to this
#               schema of characters.
#               The string that is being written can be easily customized. 
#               The idea is to study the multiple variations in the simulator
#               and implement the best one in a micro-controller Arduino,
#               ESP32 IDF, or any ARM micro. 
#               One possible application is for easily and cheaply have a
#               one led printf() method for debugging in microcontrollers that
#               are already deployed.
#               I would like to remember you that one doesn't need to remember
#               a mapping table, it's a simple normal character that will be
#               rendered.

import tkinter as tk
import time
import copy

my_string = 'HELLO WORLD!'
# my_string = 'HE'

char_dic = {
    ' ' : ['   ',
           '   ',
           '   ',
           '   ',
           '   '],

    'A' : ['***',
           '* *',
           '***',
           '* *',
           '* *'],

    'B' : ['** ',
           '* *',
           '** ',
           '* *',
           '** '],

    'C' : ['***',
           '*  ',
           '*  ',
           '*  ',
           '***'],

    'D' : ['** ',
           '* *',
           '* *',
           '* *',
           '** '],
           
    'E' : ['***',
           '*  ',
           '***',
           '*  ',
           '***'],

    'F' : ['***',
           '*  ',
           '***',
           '*  ',
           '*  '],

    'G' : ['***',
           '*  ',
           '* *',
           '* *',
           '***'],

    'H' : ['* *',
           '* *',
           '***',
           '* *',
           '* *'],

    'I' : ['***',
           ' * ',
           ' * ',
           ' * ',
           '***'],

    'J' : ['***',
           ' * ',
           ' * ',
           '** ',
           '** '],

    'K' : ['* *',
           '** ',
           '** ',
           '* *',
           '* *'],

    'L' : ['*  ',
           '*  ',
           '*  ',
           '*  ',
           '***'],

    'M' : ['* *',
           '***',
           '* *',
           '* *',
           '* *'],

    'N' : ['* *',
           '* *',
           '* *',
           '***',
           '* *'],

    'O' : [' * ',
           '* *',
           '* *',
           '* *',
           ' * '],

    'P' : ['***',
           '* *',
           '***',
           '*  ',
           '*  '],

    'Q' : ['***',
           '* *',
           '* *',
           '***',
           '  *'],

    'R' : ['** ',
           '* *',
           '** ',
           '* *',
           '* *'],

    'S' : ['***',
           '*  ',
           '***',
           '  *',
           '***'],

    'T' : ['***',
           ' * ',
           ' * ',
           ' * ',
           ' * '],

    'U' : ['* *',
           '* *',
           '* *',
           '* *',
           '***'],

    'V' : ['* *',
           '* *',
           '* *',
           '* *',
           ' * '],

    'W' : ['* *',
           '* *',
           '***',
           '***',
           '* *'],

    'X' : ['* *',
           ' * ',
           ' * ',
           ' * ',
           '* *'],

    'Y' : ['* *',
           '* *',
           ' * ',
           ' * ',
           ' * '],

    'Z' : ['***',
           '  *',
           ' * ',
           '*  ',
           '***'],

    '0' : ['***',
           '* *',
           '* *',
           '* *',
           '***'],

    '1' : ['  *',
           ' **',
           '* *',
           '  *',
           '  *'],

    '2' : ['***',
           '  *',
           '***',
           '* *',
           '***'],

    '3' : ['***',
           '  *',
           '***',
           '  *',
           '***'],

    '4' : ['* *',
           '* *',
           '***',
           '  *',
           '  *'],

    '5' : ['** ',
           '*  ',
           '***',
           '  *',
           '***'],

    '6' : ['***',
           '*  ',
           '***',
           '* *',
           '***'],

    '7' : ['***',
           '  *',
           '***',
           '  *',
           '  *'],

    '8' : ['***',
           '* *',
           '***',
           '* *',
           '***'],

    '9' : ['***',
           '* *',
           '***',
           '  *',
           '  *'],

    '-' : ['   ',
           '   ',
           '***',
           '   ',
           '   '],

    '+' : ['   ',
           ' * ',
           '***',
           ' * ',
           '   '],

    '*' : ['   ',
           '* *',
           ' * ',
           ' * ',
           '* *'],

    '/' : ['  ',
           '  *',
           ' * ',
           '*  ',
           '   '],

    '.' : ['   ',
           '   ',
           '   ',
           '   ',
           '*  '],

    ',' : ['   ',
           '   ',
           '   ',
           ' * ',
           '*  '],

    ':' : ['   ',
           ' * ',
           '   ',
           ' * ',
           '   '],

    '!' : [' * ',
           ' * ',
           ' * ',
           '   ',
           ' * ']

}

LED_DISABLE = 'LED_DISABLE'
LED_ENABLE  = 'LED_ENABLE'

class Application(tk.Frame):
    def __init__(self, master=None):
        super().__init__(master)
        
        self.COLOR_OFF  = 'black'  
        self.COLOR_BASE = 'yellow3'
        self.COLOR_ON   = 'green yellow'

        self.factor = 0.5 # 1.0
        self.time_led_light = 0.8
        self.time_delta_led_light = 0.2
        self.time_delta_column = 1.5 
        self.time_delta_carater = 1.5 * 2

        self.time_seq = [(self.time_led_light * self.factor, LED_ENABLE),
                         (self.time_delta_led_light * self.factor, LED_DISABLE),
                         (self.time_led_light * self.factor, LED_ENABLE),
                         (self.time_delta_led_light * self.factor, LED_DISABLE),
                         (self.time_led_light * self.factor, LED_ENABLE),
                         (self.time_delta_led_light * self.factor, LED_DISABLE),
                         (self.time_led_light * self.factor, LED_ENABLE),
                         (self.time_delta_led_light * self.factor, LED_DISABLE),
                         (self.time_led_light * self.factor, LED_ENABLE),
                         
                         (self.time_delta_column * self.factor, LED_DISABLE),

                         (self.time_led_light * self.factor, LED_ENABLE),
                         (self.time_delta_led_light * self.factor, LED_DISABLE),
                         (self.time_led_light * self.factor, LED_ENABLE),
                         (self.time_delta_led_light * self.factor, LED_DISABLE),
                         (self.time_led_light * self.factor, LED_ENABLE),
                         (self.time_delta_led_light * self.factor, LED_DISABLE),
                         (self.time_led_light * self.factor, LED_ENABLE),
                         (self.time_delta_led_light * self.factor, LED_DISABLE),
                         (self.time_led_light * self.factor, LED_ENABLE),
                         
                         (self.time_delta_column * self.factor, LED_DISABLE),

                         (self.time_led_light * self.factor, LED_ENABLE),
                         (self.time_delta_led_light * self.factor, LED_DISABLE),
                         (self.time_led_light * self.factor, LED_ENABLE),
                         (self.time_delta_led_light * self.factor, LED_DISABLE),
                         (self.time_led_light * self.factor, LED_ENABLE),
                         (self.time_delta_led_light * self.factor, LED_DISABLE),
                         (self.time_led_light * self.factor, LED_ENABLE),
                         (self.time_delta_led_light * self.factor, LED_DISABLE),
                         (self.time_led_light * self.factor, LED_ENABLE),

                         (self.time_delta_carater * self.factor, LED_DISABLE) ]

        self.time_seq_index = 0

        self.my_string_tmp = my_string

        self.iterator = None

        self.char_buf = [[' ', ' ', ' '],
                        [' ', ' ', ' '],
                        [' ', ' ', ' '],
                        [' ', ' ', ' '],
                        [' ', ' ', ' ']]

        self.list_char_buf = [copy.deepcopy(self.char_buf),
                              copy.deepcopy(self.char_buf),
                              copy.deepcopy(self.char_buf),
                              copy.deepcopy(self.char_buf),
                              copy.deepcopy(self.char_buf),
                              copy.deepcopy(self.char_buf),
                              copy.deepcopy(self.char_buf),
                              copy.deepcopy(self.char_buf),
                              copy.deepcopy(self.char_buf),
                              copy.deepcopy(self.char_buf),
                              copy.deepcopy(self.char_buf),
                              copy.deepcopy(self.char_buf)]

        self.master = master
        self.pack()
        self.create_widgets()


    def create_widgets(self):
        self.label = tk.Label(text="")
        self.label.pack()

        self.master.title("One LED Text Study Lab")
        self.pack(fill=tk.BOTH, expand=1)

        canvas = tk.Canvas(self)

        self.canvas = canvas

        self.flag_color = False

        pos_x = 20
        pos_y = 100
        pos_delta_y = 40
        d_s = 6
        len_list_digits = 12

        dxi = pos_x + int(672 / float(len_list_digits)) * (len_list_digits - 1) - d_s
        dyi = 20

        self.id_led = canvas.create_oval(dxi, dyi, dxi + 50, dyi + 50, outline="#f11",
            fill="#1f1", width=1)

        # dxi = pos_x + int(414 / 10.0) * 9
        dxi = pos_x + int(672 / float(len_list_digits)) * (len_list_digits - 1) - d_s
        dyi = pos_y
        start_shifted = True
        last = True
        dxx, dyy, self.id_led_dic_char_one = self.gen_char(canvas, dxi, dyi, start_shifted, d_s, last)
        
        dxi = pos_x
        dyi = dyy + pos_delta_y
        start_shifted = False
        last = False
        self.id_led_list_char = []
        for x in range(0, len_list_digits):
            if x == (len_list_digits -1):
                last = True
            dxx, dyy, dic_char = self.gen_char(canvas, dxi, dyi, start_shifted, d_s, last)
            dxi = dxx
            start_shifted = True
            self.id_led_list_char.append(dic_char)
            print("dxx: ", dxx)

        canvas.pack(fill=tk.BOTH, expand=1)
        self.update_clock()


    def gen_char(self, canvas, dxi, dyi, start_shifted, d_s, last):
        # dxi = 100
        # dyi = 100
        dx = 8
        dy = 8
        # d_s = 6
        dxx = 0
        dyy = 0
        dic_char = {}
        for x in range(0, 4):
            for y in range(0, 5):
                if (y != 4 and x == 3) or (x == 3 and last):
                    continue
                dxx = dxi + dx*(x+1) + d_s*(x + start_shifted)
                dyy = dyi + dy*(y+1) + d_s*y
                id = canvas.create_oval(dxi + dx*x + d_s*(x + start_shifted),
                                   dyi + dy*y + d_s*y,
                                   dxx,
                                   dyy,
                                   # outline="#f11", fill="#1f1", width=1)
                                   outline="#f11", fill="black", width=1)
                dic_char[str(x) + "-" + str(y)] = id
        return (dxx, dyy, dic_char)


    def get_char(self, char):
        if char not in char_dic:
            return
        char_display = char_dic[char]
        for x in range(0, 3):
            for y in range(0, 5):
                value = '*' if char_display[y][x] == '*' else '.'
                yield (x, y, value)


    def update_char(self, char):
        x = None
        y = None
        value = None
        if self.iterator == None:
            self.iterator = self.get_char(char)
            x, y, value = next(self.iterator)
        else:
            x, y, value = next(self.iterator)
        if y==4  and x==2:
            self.iterator = None
        self.char_buf[y][x] = value
        return (x, y, value)        


    def clear_char(self):
        for x in range(0, 3):
            for y in range(0, 5):        
                self.char_buf[y][x] = ' '

    def copy_char_to_list_char(self):
        # Removes the first char from the list.
        self.list_char_buf = self.list_char_buf[1: ]
        # Appends the current char to the list.
        self.list_char_buf.append(copy.deepcopy(self.char_buf))

    def display_char_buf(self):
        for x in range(0, 3):
            for y in range(0, 5):
                color = None
                if self.char_buf[y][x] == '*':
                    # LED ON
                    color = self.COLOR_ON
                elif self.char_buf[y][x] == '.':
                    # LED LOW DIM
                    color = self.COLOR_BASE
                else:
                    # LED OFF
                    color = self.COLOR_OFF
                id = self.id_led_dic_char_one[str(x) + "-" + str(y)]
                self.canvas.itemconfigure(id, fill=color)


    def display_list_char_bufs(self):
        for i in range(0, len(self.list_char_buf)):
            for x in range(0, 3):
                for y in range(0, 5):
                    color = None
                    if self.list_char_buf[i][y][x] == '*':
                        # LED ON
                        color = self.COLOR_ON
                    elif self.list_char_buf[i][y][x] == '.':
                        # LED LOW DIM
                        color = self.COLOR_BASE
                    else:
                        # LED OFF
                        color = self.COLOR_OFF
                    id = self.id_led_list_char[i][str(x) + "-" + str(y)]
                    self.canvas.itemconfigure(id, fill=color)


    def update_clock(self):
        # print('self.my_string_tmp: ',self.my_string_tmp)
        # print('len(self.time_seq): ', len(self.time_seq) )

        now = time.strftime("%H:%M:%S")
        self.label.configure(text=now)

        index = self.time_seq_index

        if self.my_string_tmp != '':
            if index == len(self.time_seq):
                # Last step on the sequence of the char.   
                self.time_seq_index = 0
                index = self.time_seq_index
                # Remove one carater from string.
                if len(self.my_string_tmp) > 1:
                    self.copy_char_to_list_char()
                    self.display_list_char_bufs()
                    self.clear_char()
                    self.my_string_tmp = self.my_string_tmp[1: ]
                    # Schedule the next time step.
                    # print("index_last_in_char: ", index)
                    next_time, led_type = self.time_seq[index]
                    self.master.after(int(next_time * 1000), self.update_clock)
                else:
                    self.copy_char_to_list_char()
                    self.display_list_char_bufs()
                    self.my_string_tmp = ''
            else:
                # Schedule the next time step.
                # print("index: ", index)
                next_time, led_type = self.time_seq[index]
                self.master.after(int(next_time * 1000), self.update_clock)

                if led_type == LED_ENABLE:
                    # Fill the LED position int he buffer.
                    x, y, value = self.update_char(self.my_string_tmp[0])
                    color = self.COLOR_BASE
                    if value == '*':
                         color = self.COLOR_ON
                    self.canvas.itemconfigure(self.id_led, fill=color)
                else:
                    # LED_DISABLE
                    color = self.COLOR_OFF
                    self.canvas.itemconfigure(self.id_led, fill=color)
                
                self.time_seq_index += 1

        self.display_char_buf()
        # self.display_list_char_bufs()


def main():
    root = tk.Tk()
    app = Application(master=root)
    root.geometry("700x300+700+300")
    # To center the window on the screen.
    root.eval('tk::PlaceWindow %s center' % root.winfo_pathname(root.winfo_id()))
    app.mainloop()


if __name__ == "__main__":
    main()

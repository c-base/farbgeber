#!/usr/bin/python3

import threading
import math

import pygame

from colour import Color


class FarbgeberNew:
    def __init__(self, *colors):
        hex_list = [c.hex_l for c in colors]
        steps = int(3600 / len(hex_list))
        self.colors = list()

        for i, c in enumerate(hex_list):
            self.colors.extend(self.linear_gradient(hex_list[i], hex_list[i + 1 if i < len(hex_list) - 1 else 0], steps))


    def linear_gradient(self, start_hex, finish_hex="#FFFFFF", n=10):
        """ 
        returns a gradient list of (n) colors between
        two hex colors. start_hex and finish_hex
        should be the full six-digit color string,
        inlcuding the number sign ("#FFFFFF") 
        """

        def hex_to_rgb(hex_value):
            """ 
            #FFFFFF" -> [255,255,255] 
            """
            # Pass 16 to the integer function for change of base
            return [int(hex_value[i:i + 2], 16) for i in range(1, 6, 2)]


        def rgb_to_hex(rgb):
            """ 
            [255,255,255] -> "#FFFFFF" 
            """
            # Components need to be integers for hex to make sense
            rgb = [int(x) for x in rgb]
            return "#"+"".join(["0{0:x}".format(v) if v < 16 else
                "{0:x}".format(v) for v in rgb])


        def color_dict(gradient):
            """ 
            Takes in a list of RGB sub-lists and returns dictionary of
            colors in RGB and hex form for use in a graphing function
            defined later on 
            """

            return {"hex":[rgb_to_hex(rgb) for rgb in gradient],
                    "r":[rgb[0] for rgb in gradient],
                    "g":[rgb[1] for rgb in gradient],
                    "b":[rgb[2] for rgb in gradient]}

        s = hex_to_rgb(start_hex)
        f = hex_to_rgb(finish_hex)

        rgb_list = [s]

        # Calcuate a color at each evenly spaced value of t from 1 to n
        for t in range(1, n):
            # Interpolate RGB vector for color at the current value of t
            curr_vector = [int(s[j] + (float(t)/(n-1))*(f[j]-s[j])) for j in range(3)]
            rgb_list.append(curr_vector)

        return [Color(x) for x in color_dict(rgb_list)['hex']]


    def gen_palette(self, time_value):
        base_color = self.colors[int(time_value)]
        base_hue = base_color.get_hue()

        base_degree = base_hue * 360                                                
        if base_degree < 180:                                                       
            contrast_hue = base_degree + 180                                        
        else:                                                                       
            contrast_hue = base_degree - 180

        base_saturation = base_color.get_saturation()
        base_luminance = base_color.get_luminance()

        contrast_hue /= 360
        contrast_color = Color(hsl=(contrast_hue, base_saturation, base_luminance))

        hue_modifier = 0.03
        lum_modifier = 0.07
        sat_modifier = 0.2

        base_color_variant_1 = Color(hsl=(base_color.hue + hue_modifier, base_saturation - sat_modifier, base_luminance))
        base_color_variant_2 = Color(hsl=(base_color.hue - hue_modifier, base_saturation - sat_modifier, base_luminance))
        base_color_variant_3 = Color(hsl=(base_color.hue, base_saturation, base_luminance + lum_modifier))
        base_color_variant_4 = Color(hsl=(base_color.hue, base_saturation, base_luminance - lum_modifier))

        p = dict()
        p['time_value']           = time_value
        p['base_color']           = base_color
        p['base_color_variant_1'] = base_color_variant_1
        p['base_color_variant_2'] = base_color_variant_2
        p['base_color_variant_3'] = base_color_variant_3
        p['base_color_variant_4'] = base_color_variant_4
        p['contrast_color']       = contrast_color

        return p


def draw_circle(screen, time_value, canvas=0, width=0, height=0):
    color_b = fb.gen_palette(time_value)["base_color"]
    color_c = fb.gen_palette(time_value)["contrast_color"]

    i = 2 * math.pi * time_value / 3600.0

    r1 = 200
    r2 = 150
    x1 = 400 + r1 * math.cos(i)
    x2 = 400 + r2 * math.cos(i)
    y1 = 300 + r1 * math.sin(i)
    y2 = 300 + r2 * math.sin(i)

    x1_o = 400 + (r1 + 50) * math.cos(i)
    x2_o = 400 + (r2 + 50) * math.cos(i)
    y1_o = 300 + (r1 + 50) * math.sin(i)
    y2_o = 300 + (r2 + 50) * math.sin(i)

    pygame.draw.line(screen, (255 * color_b.red, 255 * color_b.green, 255 *
                              color_b.blue), (x1, y1), (x2, y2), 1)

    pygame.draw.line(screen, (255 * color_c.red, 255 * color_c.green, 255 *
                              color_c.blue), (x1_o, y1_o), (x2_o, y2_o), 1)

    pygame.display.update()

def setPixel(screen, x, y, color):
    pygame.draw.line(screen, \
      (255 * color.red, 255 * color.green, 255 * color.blue), (x, y), (x, y), 1)
    pygame.display.update()

def setLine(screen, x1, y1, x2, y2, color):
    pygame.draw.line(screen, \
                     (255 * color.red, 255 * color.green, 255 * color.blue), (x1, y1), (x2, y2), 1)
    pygame.display.update()

def circleSym8(screen, xCenter, yCenter, radius, color):
    dbgColor = Color("lime")

    radius_inner = radius * 0.75

    r1_2 = radius * radius
    r2_2 = radius_inner * radius_inner

    # outer
    setPixel(screen, xCenter, yCenter + radius, color)
    setPixel(screen, xCenter, yCenter - radius, color)
    setPixel(screen, xCenter + radius, yCenter, color)
    setPixel(screen, xCenter - radius, yCenter, color)

    # inner
    setPixel(screen, xCenter, yCenter + radius_inner, color)
    setPixel(screen, xCenter, yCenter - radius_inner, color)
    setPixel(screen, xCenter + radius_inner, yCenter, color)
    setPixel(screen, xCenter - radius_inner, yCenter, color)

    y = radius
    y_inner = radius_inner
    x = 1
    x_inner = 1
    x_inner_increment = radius_inner / radius
    y = int(math.sqrt(r1_2 - 1) + 0.5)
    y_inner = int(math.sqrt(r2_2 - 1) + 0.5)

    while (x < y):
        x1 = xCenter + x
        y1 = yCenter + y

        # pixels
        setPixel(screen, xCenter + x, yCenter + y, color)
        setPixel(screen, xCenter + x, yCenter - y, color)
        setPixel(screen, xCenter - x, yCenter + y, color)
        setPixel(screen, xCenter - x, yCenter - y, color)
        setPixel(screen, xCenter + y, yCenter + x, color)
        setPixel(screen, xCenter + y, yCenter - x, color)
        setPixel(screen, xCenter - y, yCenter + x, color)
        setPixel(screen, xCenter - y, yCenter - x, color)
        x += 1
        y = int(math.sqrt(r1_2 - x*x) + 0.5)

        x2 = xCenter + x
        y2 = yCenter + y

        x3 = xCenter + x_inner
        y3 = yCenter + y_inner

        setPixel(screen, xCenter + x_inner, yCenter + y_inner, color)
        setPixel(screen, xCenter + x_inner, yCenter - y_inner, color)
        setPixel(screen, xCenter - x_inner, yCenter + y_inner, color)
        setPixel(screen, xCenter - x_inner, yCenter - y_inner, color)
        setPixel(screen, xCenter + y_inner, yCenter + x_inner, color)
        setPixel(screen, xCenter + y_inner, yCenter - x_inner, color)
        setPixel(screen, xCenter - y_inner, yCenter + x_inner, color)
        setPixel(screen, xCenter - y_inner, yCenter - x_inner, color)
        x_inner += x_inner_increment
        y_inner = int(math.sqrt(r2_2 - x_inner * x_inner) + 0.5)

        x4 = xCenter + x_inner
        y4 = yCenter + y_inner

        pygame.draw.polygon(screen, (255, 0, 0), [[x1,y1], [x2,y2], [x3,y3], [x4,y4]], 0)

    if (x == y):
        setPixel(screen, xCenter + x, yCenter + y, color)
        setPixel(screen, xCenter + x, yCenter - y, color)
        setPixel(screen, xCenter - x, yCenter + y, color)
        setPixel(screen, xCenter - x, yCenter - y, color)

        setPixel(screen, xCenter + x_inner, yCenter + y_inner, color)
        setPixel(screen, xCenter + x_inner, yCenter - y_inner, color)
        setPixel(screen, xCenter - x_inner, yCenter + y_inner, color)
        setPixel(screen, xCenter - x_inner, yCenter - y_inner, color)

if __name__ == "__main__":
    canvas_width = 800
    canvas_height = 600
    screen = pygame.display.set_mode((canvas_width, canvas_height))

    fb = FarbgeberNew(Color("red"), Color("yellow"), Color("lime"), Color("cyan"), Color("blue"), Color("magenta"))
    time_value = 0.0

    while(time_value < 3600):
      draw_circle(screen, time_value, canvas_width, canvas_height)
      time_value += 1

    # circleSym8(screen, 400, 300, 200, Color("red"))

    clock = pygame.time.Clock()
    running = True

    while running:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False

        clock.tick(60)


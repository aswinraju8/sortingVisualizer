import pygame
import random
import math
pygame.init()
class DrawingInformation:
    #colors
    green = 0, 255, 0
    red = (255, 0, 0)
    white = 255, 255, 255
    black = 0, 0, 0
    back_ground = white
    blocks_gradients = [(160,160,160),(128,128,128),(100,100,100)] # different shades of grey for the blocks so that each block looks distinct
    font = pygame.font.SysFont('comicsans', 20)
    large_font = pygame.font.SysFont('comicsans', 30)

    #padding in the screen from x axis (left and right)
    padding_x = 100
    #padding in the screen from y axis (top)
    padding_y = 150
    def __init__(self,width,height,lst):
        #height and width of the screen
        self.width = width
        self.height = height
        #setting the display according to the preferred height and width
        self.window = pygame.display.set_mode((width, height))
        pygame.display.set_caption("Sorting Visualizer!!!")
        self.set_lst(lst)
    def set_lst(self, lst):
        self.lst = lst
        self.min_val = min(lst)
        self.max_val = max(lst)
        #range in which the blocks going to occupy(width)
        self.block_range_x = round((self.width - self.padding_x) / len(lst))
        #height of the maximum block based on the maximum and minimum element
        self.block_range_y = math.floor((self.height - self.padding_y)/(self.max_val - self.min_val))
        self.start_draw = self.padding_x//2 #50 on left and the remaining 50 on right

# Actual drawing of the blocks
def DrawScreen(draw_info, sorting_algo_name, ascending):
    #fills the screen with the background each time the window is refreshed
    draw_info.window.fill(draw_info.back_ground)
    title = draw_info.large_font.render(f"{sorting_algo_name} - {'Ascending' if ascending else 'Descending'}",1,draw_info.green)
    draw_info.window.blit(title, (draw_info.width / 2 - title.get_width() / 2, 5))
    #Title of the screen with controls and sorting algorithms
    controls = draw_info.font.render("R - Reset | S - Start Sorting | A - Ascending Sort | D - Descending Sort", 1, draw_info.black)
    draw_info.window.blit(controls, (draw_info.width / 2 - controls.get_width()/2, 45))
    sorting = draw_info.font.render("I - Insertion Sort | B - Bubble Sort | T - Selection Sort ",1,draw_info.black)
    #Put the controls and sorting description in the center using the formula for x axis and y axis as 5

    draw_info.window.blit(sorting, (draw_info.width/2 - sorting.get_width()/2, 85))
    DrawBlocks(draw_info)
    pygame.display.update()
def DrawBlocks(draw_info, color_positions={},clear_bg = False):
    lst = draw_info.lst
    if clear_bg:
        clear_rect = (draw_info.padding_x // 2, draw_info.padding_y,
                      draw_info.width - draw_info.padding_x, draw_info.height - draw_info.padding_y)
        pygame.draw.rect(draw_info.window, draw_info.back_ground, clear_rect)

    for i, val in enumerate(lst):
        x = draw_info.start_draw + i * draw_info.block_range_x
        y = draw_info.height - (val - draw_info.min_val) * draw_info.block_range_y

        color = draw_info.blocks_gradients[i % 3]

        if i in color_positions:
            color = color_positions[i]

        pygame.draw.rect(draw_info.window, color, (x, y, draw_info.block_range_x, draw_info.height))

    if clear_bg:
        pygame.display.update()
#Generating the list with random elements
def ListGenerator(n, min_val, max_val):
    lst = []
    for _ in range(n):
        val = random.randint(min_val, max_val)#outputs a value in the range of min_val to max_val
        lst.append(val)
    return lst
def bubble_sort(draw_info, ascending = True):
    lst = draw_info.lst
    for i in range(len(lst)-1):
        for j in range(len(lst)-1-i):
            if (lst[j]>lst[j+1] and ascending) or (lst[j]<lst[j+1] and not ascending):
                lst[j],lst[j+1]=lst[j+1],lst[j]
                DrawBlocks(draw_info, {j: draw_info.green,j+1: draw_info.red},True)
                #Making generator so that each swapping is displayed
                yield True
    return lst
def insertion_sort(draw_info,ascending = True):
    lst = draw_info.lst
    if ascending or not ascending:
        for i in range(0,len(lst)):
            j = i
            while j>0 and ((lst[j]<lst[j-1] and ascending) or(lst[j]>lst[j-1] and not ascending)):
                lst[j],lst[j-1]=lst[j-1],lst[j]
                DrawBlocks(draw_info,{j-1:draw_info.green,j:draw_info.red},True)
                j-=1
                yield True
    return lst
def selection_sort(draw_info, ascending):
    lst = draw_info.lst
    for i in range(len(lst)):
        temp = i
        for j in range(i,len(lst)):
            if (lst[j]<lst[temp] and ascending) or (lst[j]>lst[temp]and not ascending):
                temp = j
        lst[temp],lst[i] = lst[i], lst[temp]
        DrawBlocks(draw_info, {temp: draw_info.green, i: draw_info.red}, True)
        yield True
    return ls



def main():
    run = True
    clock = pygame.time.Clock()
    #Calling the class function for staring the window
    n = 50
    min_val = 0
    max_val = 100
    lst = ListGenerator(n, min_val, max_val)
    draw_info = DrawingInformation(800,600,lst)
    sorting = False
    ascending = True

    sorting_algo = bubble_sort
    sorting_algo_name = "Bubble Sort"
    generator_sort = None
    while run:
        clock.tick(60)
        if sorting:
            #yeilding the next swap
            try:
                next(generator_sort)
            except StopIteration:
                sorting = False
        else:
            DrawScreen(draw_info,sorting_algo_name,ascending)

        #DrawScreen(draw_info)
        #update the screen after a process is completed or when a new process is invoked
        pygame.display.update()

        for ev in pygame.event.get():
            if ev.type == pygame.QUIT:
                run = False
            # If no key is pressed then continue the loop
            if ev.type != pygame.KEYDOWN:
                continue
            # If r is pressed reset the list
            if ev.key == pygame.K_r:
                lst = ListGenerator(n, min_val, max_val)
                #updating the class list
                draw_info.set_lst(lst)
                sorting = False
            #If s is pressed then start sorting
            elif ev.key == pygame.K_s  and not sorting:
                sorting = True
                generator_sort = sorting_algo(draw_info, ascending)
            elif ev.key == pygame.K_b  and not sorting:
                sorting_algo = bubble_sort
                sorting_algo_name = "Bubble Sort"
                #generator_sort = sorting_algo(draw_info, ascending)
            elif ev.key == pygame.K_i  and not sorting:
                sorting_algo = insertion_sort
                sorting_algo_name = "Insertion Sort"
                #generator_sort = sorting_algo(draw_info, ascending)
            elif ev.key == pygame.K_t  and not sorting:
                sorting_algo = selection_sort
                sorting_algo_name = "Selection Sort"
            #If a is pressed sort in ascending order
            elif ev.key == pygame.K_a and not sorting:
                ascending = True
            #If d is pressed sort in descending order
            elif ev.key == pygame.K_d and not sorting:
                ascending = False



    pygame.quit()
if __name__ == "__main__":
    main()




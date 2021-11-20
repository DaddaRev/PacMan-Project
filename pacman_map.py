'''
@author Michele Tomaiuolo - http://www.ce.unipr.it/people/tomamic
@license This software is free - http://www.gnu.org/licenses/gpl.html


'''


board = ["#############################",  #29 '#'
         "#             #             #",
         "# ------------# ------------#",  #24 bisc
         "# -### -#### -# -#### -### -#",  #6 bisc
         "# +### -#### -# -#### -### +#",  #4 bisc
         "# -    -     -  -     -    -#",  #6 bisc
         "# --------------------------#",  #26 bisc
         "# -### -# -####### -# -### -#",  #6 bisc
         "# -    -# -   #    -# -    -#",  #6 bisc
         "# ------# ----# ----# ------#",  #20 bisc
         "###### -####  #  #### -######",  #2 bisc
         "###### -#           # -######",  #2 bisc
         "###### -#           # -######",  #2 bisc
         "###### -#  #######  # -######",  #2 bisc
         "       -   #######    -      ",  #2 bisc
         "       -   #######    -      ",  #2 bisc
         "###### -#  #######  # -######",  #2 bisc
         "###### -#           # -######",  #2 bisc
         "###### -#           # -######",  #2 bisc
         "###### -#  #######  # -######",  #2 bisc
         "#      -      #       -     #",  #2 bisc
         "# ------------# ------------#",  #24 bisc
         "# -### -#### -# -#### -### -#",  #6 bisc
         "# -  # -     -  -     -#   -#",  #6 bisc
         "# +--# -------  -------# --+#",  #18 bisc
         "### -# -# -####### -# -# -###",  #6 bisc
         "#   -  -# -   #    -# -  -  #",  #6 bisc
         "# ------# ----# ----# ------#",  #20 bisc
         "# -######### -# -######### -#",  #4 bisc
         "# -          -  -          -#",  #4 bisc
         "# --------------------------#",  #26 bisc
         "#############################"]  


def in_wall(x: int, y: int) -> bool:
    c, r, w, h = x//8, y//8, 3 if x%8 else 2, 3 if y%8 else 2
    return "#" in "".join(line[c:c+w] for line in board[r:r+h])
    ##for line in board[r:r+h]:
    ##    if "#" in line[c:c+w]: return True
    ##return False

def in_biscuit(x: int, y: int) -> bool:
    z = list(board[y])
    if z[x]=="-":
        return True
    else:
        return False
    
def in_special_biscuit(x: int, y: int) -> bool:
    z = list(board[y])
    if z[x]=="+":
        return True
    else:
        return False
    


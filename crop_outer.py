def corp_margin(img, thres = 765):
        img2=img.sum(axis=2)
        (row, col)=img2.shape
        row_top=0
        raw_down=0
        col_top=0
        col_down=0
        for r in range(0,row):
                if img2.sum(axis=1)[r]<thres*col:
                        row_top=r
                        break
 
        for r in range(row-1,0,-1):
                if img2.sum(axis=1)[r]<thres*col:
                        raw_down=r
                        break
 
        for c in range(0,col):
                if img2.sum(axis=0)[c]<thres*row:
                        col_top=c
                        break
 
        for c in range(col-1,0,-1):
                if img2.sum(axis=0)[c]<thres*row:
                        col_down=c
                        break
 
        new_img=img[row_top:raw_down+1,col_top:col_down+1,0:3]
        return new_img
  
  
  
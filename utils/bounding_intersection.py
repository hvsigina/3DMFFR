class Point: 
    def __init__(self, x, y): 
        self.x = x 
        self.y = y 
  
# Given three collinear points p, q, r, the function checks if  
# point q lies on line segment 'pr'  
def onSegment(p, q, r): 
    if ( (q.x <= max(p.x, r.x)) and (q.x >= min(p.x, r.x)) and 
           (q.y <= max(p.y, r.y)) and (q.y >= min(p.y, r.y))): 
        return True
    return False
  
def orientation(p, q, r): 
    # to find the orientation of an ordered triplet (p,q,r) 
    # function returns the following values: 
    # 0 : Collinear points 
    # 1 : Clockwise points 
    # 2 : Counterclockwise 
      
    # See https://www.geeksforgeeks.org/orientation-3-ordered-points/amp/  
    # for details of below formula.  
      
    val = (float(q.y - p.y) * (r.x - q.x)) - (float(q.x - p.x) * (r.y - q.y)) 
    if (val > 0): 
          
        # Clockwise orientation 
        return 1
    elif (val < 0): 
          
        # Counterclockwise orientation 
        return 2
    else: 
          
        # Collinear orientation 
        return 0
  
# The main function that returns true if  
# the line segment 'p1q1' and 'p2q2' intersect. 
def doIntersect(p1,q1,p2,q2): 
      
    # Find the 4 orientations required for  
    # the general and special cases 
    o1 = orientation(p1, q1, p2) 
    o2 = orientation(p1, q1, q2) 
    o3 = orientation(p2, q2, p1) 
    o4 = orientation(p2, q2, q1) 
  
    # General case 
    if ((o1 != o2) and (o3 != o4)): 
        return True
  
    # Special Cases 
  
    # p1 , q1 and p2 are collinear and p2 lies on segment p1q1 
    if ((o1 == 0) and onSegment(p1, p2, q1)): 
        return True
  
    # p1 , q1 and q2 are collinear and q2 lies on segment p1q1 
    if ((o2 == 0) and onSegment(p1, q2, q1)): 
        return True
  
    # p2 , q2 and p1 are collinear and p1 lies on segment p2q2 
    if ((o3 == 0) and onSegment(p2, p1, q2)): 
        return True
  
    # p2 , q2 and q1 are collinear and q1 lies on segment p2q2 
    if ((o4 == 0) and onSegment(p2, q1, q2)): 
        return True
  
    # If none of the cases 
    return False

def boxIntersect(b1x,b1y,b1w,b1h,b2x,b2y,b2w,b2h):
    flag = False
    if b1x == None or b1y == None or b1w == None or b1h == None or b2x == None or b2y == None or b2w == None or b2h == None:
        return True
    b1l1 = [Point(b1x,b1y),Point(b1x+b1w,b1y)]
    b1l2 = [Point(b1x,b1y),Point(b1x,b1y+b1h)]
    b1l3 = [Point(b1x+b1w,b1y),Point(b1x+b1w,b1y+b1h)]
    b1l4 = [Point(b1x,b1y+b1h),Point(b1x+b1w,b1y+b1h)]
    
    b2l1 = [Point(b2x,b2y),Point(b2x+b2w,b2y)]
    b2l2 = [Point(b2x,b2y),Point(b2x,b2y+b2h)]
    b2l3 = [Point(b2x+b2w,b2y),Point(b2x+b2w,b2y+b2h)]
    b2l4 = [Point(b2x,b2y+b2h),Point(b2x+b2w,b2y+b2h)]
    
    if b1x<=b2x and b1y<=b2y and b1x+b1w>=b2x+b2w and b1y+b1h>=b2y+b2h:
        return False
    if b2x<=b1x and b2y<=b1y and b2x+b2w>=b1x+b1w and b2y+b2h>=b1y+b1h:
        return False
    
    box1lines = [b1l1,b1l2 ,b1l3 ,b1l4]
    box2lines = [b2l1,b2l2 ,b2l3 ,b2l4]
    
    for b1line in box1lines:
        for b2line in box2lines:
            flag = doIntersect(b1line[0],b1line[1],b2line[0],b2line[1])
            if flag:
                return True

    return flag
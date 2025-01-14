import numpy as np

def fit_circle_through_3_points(ABC):# need rewrite
    ''' Mathematical background is provided in http://www.regentsprep.org/regents/math/geometry/gcg6/RCir.html
    Imput: 
    ABC is a [3 x 2n] array. Each two columns represent a set of three points which lie on
    a circle. Example: [-1 2;2 5;1 1] represents the set of points (-1,2), (2,5) and (1,1) in Cartesian
    (x,y) coordinates.

    utputs:  
    R       is a [1 x n] array of circle radii corresponding to each set of three points.
    xcyc    is an [2 x n] array of of the centers of the circles, where each column is [[xc_i][yc_i]] 
    where i corresponds to the {A,B,C} set of points in the block [3 x 2i-1:2i] of ABC  
    Author: Danylo Malyuta.
    Transfer: Yicheng Zang
    Version: v1.0 (June 2016)
    Transfer Version: v1.0 (Nov. 2022)
    ----------------------------------------------------------------------------------------------------------
    Each set of points {A,B,C} lies on a circle. Question: what is the circles radius and center?
    A: point with coordinates (x1,y1)
    B: point with coordinates (x2,y2)
    C: point with coordinates (x3,y3)
    ============= Find the slopes of the chord A<-->B (mr) and of the chord B<-->C (mt)
      mt = (y3-y2)/(x3-x2)
      mr = (y2-y1)/(x2-x1)

    '''


    #Begin by generalizing xi and yi to arrays of individual xi and yi for each {A,B,C} set of points provided in ABC array   
    x1=ABC[0,0:-1]
    x2=ABC[1,0]
    x3=ABC[2,0]
    y1=ABC[0,1]
    y2=ABC[1,1]
    y3=ABC[2,1]
    #Now carry out operations as usual, using array operations
    mr=(y2-y1)/(x2-x1)
    mt=(y3-y2)/(x3-x2)

    #A couple of failure modes exist:
    #(1) First chord is vertical  ==>mr==Inf
    #(2) Second chord is vertical      ==> mt==Inf
    #(3) Points are collinear          ==> mt==mr (NB: NaN==NaN here)
    #(4) Two or more points coincident ==> mr==NaN || mt==NaN
    #Resolve these failure modes case-by-case.
    idf1 = np.isinf(mr)
    idf2 = np.isinf(mt)
    idf34 = mr==mt or np.isnan(mr) or np.isnan(mt)

    # ============= Compute xc, the circle center x-coordinate
    xc= (mr*mt*(y3-y1)+mr*(x2+x3)-mt*(x1+x2))/(2*(mr-mt))
    if idf1==1: #Failure mode (1) ==> use limit case of mr==Inf
        xc=(mt*(y3-y1)+(x2+x3))/2 
    if idf2==1: #Failure mode (2) ==> use limit case of mt==Inf
        xc = ((x1+x2)-mr*(y3-y1))/2; 
    if idf34==1: #Failure mode (3) or (4) ==> cannot determine center point, return None
        xc = None
    # ============= Compute yc, the circle center y-coordinate
    yc=-1./mr*(xc-(x1+x2)/2)+(y1+y2)/2
    idmr0 = mr==0
    if idmr0==1: 
        yc = -1./mt*(xc-(x2+x3)/2)+(y2+y3)/2 
    if idf34==1: #Failure mode (3) or (4) ==> cannot determine center point, return None
        yc = None
    # ============= Compute the circle radius
    R=np.sqrt((xc-x1)**2+(yc-y1)**2)
    if idf34==1:
        R=float("inf")
    xcyc=np.array([xc,yc]).reshape(2,1)

    return R, xcyc
import bpy
bl_info = {"name": "Bezier2NurbsConverter", "category": "Object"}
    
# print out the weights of NURBS Vertices 
def printWeights( pCurve ):
    Splines = pCurve.data.splines    
    for spline in Splines:    
        for point in spline.points:
            print ( point.co[3] )


# this function takes a bezier curve as an input creates an equivalent NURBS Curve. meaning the trajectory of the NURBS is the same as the bezier
# it simply copies the vertex and its control points  of a bezier as vertices into a newly created NURB and sets it up accordingly 
def BezierToNurbs( pCurve ):
    # add if statement here like "if of type "Curve" => run this script, else dont
    print ("#######")
    
    curve = bpy.data.curves.new( 'BSpline_'  + pCurve.data.name , 'SURFACE' )
    
    Splines = pCurve.data.splines
    for spline in Splines:
        
        nurbsSpline = curve.splines.new('NURBS')
        NURBSPoints = nurbsSpline.points
        BezierPoints = spline.bezier_points 
        BezierPointsCount = len(BezierPoints)
        NURBSPoints.add(BezierPointsCount*3)
        for bezierPointIndex in range(0,BezierPointsCount):
            point = BezierPoints[bezierPointIndex]
            #REFACTOR: rename valueIndex to vectorComponentIndex
            
            for valueIndex in range (0,3):
                NURBSPoints[bezierPointIndex*3].co[valueIndex] = point.handle_left[valueIndex]
                # set the "weight" of the control point
                NURBSPoints[bezierPointIndex*3].co[3]=1.0 #REFACTOR: make somekind of "default weight" variable
            for valueIndex in range (0,3):
                NURBSPoints[bezierPointIndex*3+1].co[valueIndex] = point.co[valueIndex]
                NURBSPoints[bezierPointIndex*3+1].co[3]=1.0
            for valueIndex in range (0,3):
                NURBSPoints[bezierPointIndex*3+2].co[valueIndex] = point.handle_right[valueIndex]
                NURBSPoints[bezierPointIndex*3+2].co[3]=1.0
            print("Handle Left" ,point.handle_left)
            print("Coords" ,point.co)
            print("Handle Right" ,point.handle_right)
            
        # REFACTOR this into some function "setup defaults"
        nurbsSpline.use_cyclic_u = spline.use_cyclic_u
        nurbsSpline.use_cyclic_v = False
        nurbsSpline.use_bezier_u = True
        nurbsSpline.use_bezier_v = False
        nurbsSpline.use_endpoint_u = False
        nurbsSpline.use_endpoint_v = False              
        nurbsSpline.order_u = 4
        nurbsSpline.order_v = 2
        nurbsSpline.resolution_u = 4
        nurbsSpline.resolution_v = 4
        nurbsSpline.use_smooth = True

    ^# create actual object, put it to scene, select it
    object = bpy.data.objects.new( 'BSpline'  + pCurve.data.name , curve)
    scene = bpy.context.scene
    scene.objects.link(object)
    scene.objects.active = object


#printWeights(bpy.context.active_object)
    
BezierToNurbs( bpy.context.active_object )

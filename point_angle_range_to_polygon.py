'''
Script tool to create coverage polygons for radio towers.
'''
import arcpy, os, time

def createPointAngleRangePolygons(points, outputPolygons, azimuthField, rangeField, beamWidthField):
    """azimuth: angle central to the coverage polygon.
       range: radius of the coverage polygon. Must be in meters.
       beamwidth: full arc of coverage. It is centered on the azimuth.
       Output polygons will have the same spatial reference as the input point features"""
    pointFeatures = points
    azimuthField = azimuthField
    rangeField = rangeField
    beamWidthField = beamWidthField
    #Polygon feature class will created by the tool. 
    outputPolygonFeatures = outputPolygons
    polygons = []
    
    cursorFields = ["SHAPE@", "*"]
    with arcpy.da.SearchCursor(pointFeatures, cursorFields) as cursor:
        for row in cursor:
            centerPoint = row[0]
            azimuth = row[cursor.fields.index(azimuthField)]
            rangeDist = row[cursor.fields.index(rangeField)]
            beamWidth = row[cursor.fields.index(beamWidthField)]
            
            startAngle = (azimuth + (360 - (beamWidth / 2.0))) % 360
            print startAngle
            radiusPoints = [centerPoint.centroid]
            #Create a point every 1 degree around the arc
            for i in range(int(beamWidth) + 1):
                angle = (startAngle + i) % 360
                print angle
                radPoint = centerPoint.pointFromAngleAndDistance(angle, rangeDist)
                radiusPoints.append(radPoint.centroid)
                
            polygons.append(
                arcpy.Polygon(
                    arcpy.Array(radiusPoints), 
                    centerPoint.spatialReference))
            print 
            
    arcpy.CopyFeatures_management(polygons, outputPolygonFeatures)

if __name__ == "__main__":
    testing = True
    if testing:
        points = r"C:\Users\Administrator\My Documents\Aptana Studio 3 Workspace\tower-circle-sectors\data\Temp.gdb\point_angle"
        azimuthField = "azimuth"
        rangeField = "range"
        beamWidthField = "beamwidth"
        outputDirectory = r"C:\Users\Administrator\My Documents\Aptana Studio 3 Workspace\tower-circle-sectors\data\Temp.gdb"
        uniqueString = time.strftime("%Y%m%d%H%M%S")
        outputPolygons = os.path.join(outputDirectory, "CircleSectors_" + uniqueString)
        arcpy.SetParameter(5, outputPolygons) 
    else:
        points = arcpy.GetParameterAsText(0)
        azimuthField = arcpy.GetParameterAsText(1)
        rangeField = arcpy.GetParameterAsText(2)
        beamWidthField = arcpy.GetParameterAsText(3)
        outputDirectory = arcpy.GetParameterAsText(4)
        uniqueString = time.strftime("%Y%m%d%H%M%S")
        outputPolygons = os.path.join(outputDirectory, "CircleSectors_" + uniqueString)
        arcpy.SetParameter(5, outputPolygons)
    
    arcpy.AddMessage("Version 1.0")
    
    field_names = [f.name for f in arcpy.ListFields(points)]
    print field_names
    c = arcpy.da.SearchCursor(points, field_names)
    print c.fields
#     print arcpy.CreateFeatureclass_management (outputDirectory, "CircleSectors_" + uniqueString + "c", 
#                                          "POLYGON", points)
    #createPointAngleRangePolygons(points, outputPolygons, azimuthField, rangeField, beamWidthField)
    arcpy.AddMessage("completed")
    
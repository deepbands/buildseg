from qgis import processing

# infile = 'C:/Users/Youss/Documents/pp/New folder/split-rs-data/DataSet/rasterized/02/yyy.shp'
# outfile = 'C:/Users/Youss/Desktop/best_model_4-12-2-21/01/New folder/vgen/simp-final.shp'
def simplifyPolyg(infile, outfile, threshold):
    processing.run("native:simplifygeometries", \
        {'INPUT':infile, \
        'METHOD':0, \
        'TOLERANCE':threshold, \
        'OUTPUT':outfile})

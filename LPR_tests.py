import simplelpr

setupP = simplelpr.EngineSetupParms()
eng = simplelpr.SimpleLPR(setupP)

# Lists all available countries.
def list_countries(eng):
    print('List of available countries:')

    for i in range(0, eng.numSupportedCountries):
        print(f"{i}: {eng.get_countryCode(i)}")

def analyze_file(eng, country_id, img_path, key_path):
    # Enables syntax verification with the selected country.
    eng.set_countryWeight(country_id, 1)
    eng.realizeCountryWeights()

    # If provided, supplies the product key as a file.
    if key_path is not None:
        eng.set_productKey(key_path)

    # Alternatively, it could also be supplied from a buffer in memory:
    #
    # with open(key_path, mode='rb') as file:
    #     key_content = file.read()
    # eng.set_productKey( key_content )

    # Create a Processor object. Every working thread should use its own processor.
    proc = eng.createProcessor()

    # Enable the plate region detection and crop to plate region features.
    proc.plateRegionDetectionEnabled = True
    proc.cropToPlateRegionEnabled = True

    # Looks for license plate candidates in an image in the file system.
    cds = proc.analyze(img_path)

    # Alternatively, the input image can be supplied through an object supporting the buffer protocol:
    #
    # fh = open(img_path, 'rb')
    # try:
    #     ba = bytearray(fh.read())
    # finally:
    #     fh.close()
    # cds = proc.analyze(ba)
    #
    # or
    #
    # import numpy as np
    # from PIL import Image
    #
    # im = Image.open(img_path)
    # npi = np.asarray(im)
    # cds = proc.analyze(npi)
    #
    # or
    #
    # import cv2
    #
    # im = cv2.imread(img_path)
    # cds = proc.analyze(im)

    # Show the detection results.
    print('Number of detected candidates:', len(cds))

    for cand in cds:
        print('-----------------------------')
        print('darkOnLight:', cand.darkOnLight, ', plateDetectionConfidence:', cand.plateDetectionConfidence)
        print('boundingBox:', cand.boundingBox)
        print('plateRegionVertices:', cand.plateRegionVertices)

        for cm in cand.matches:
            print('\tcountry:', "'{:}'".format(cm.country), ', countryISO:', "'{:}'".format(cm.countryISO),
                  ', text:', "'{:}'".format(cm.text), ', confidence:', '{:.3f}'.format(cm.confidence))

            for e in cm.elements:
                print('\t\tglyph:', "'{:}'".format(e.glyph), ', confidence:', '{:.3f}'.format(e.confidence),
                      ', boundingBox:', e.boundingBox)

list_countries(eng)

analyze_file(eng,
             '81',
             r"C:\Users\ssolwa001\Pictures\evan12.jpg",
             key_path=None)
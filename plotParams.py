from cmcrameri import cm #colormaps
from numpy import floor
import numpy as np
import matplotlib
import matplotlib.pyplot as plt
import matplotlib.font_manager as font_manager
import os.path

batlow = cm.vik(range(255))
batlow = batlow[0:255:int(floor(255/8)),:]

def applyPlotStyle(plotStyleString):
    if plotStyleString=='Dark':
        # dark background
        params = {"ytick.color" : "w",
                  "xtick.color" : "w",
                  "axes.labelcolor" : "w",
                  "axes.edgecolor" : "w",
                 "axes.linewidth" : 3,
                 "xtick.major.width" : 3,
                 "ytick.major.width" : 3,
                 "xtick.major.size" : 8,
                 "ytick.major.size" : 8,
                 "text.color" : "w"}
        plt.rcParams.update(params)
        plt.style.use('dark_background')
        baseColor = '#ffffff'
    elif plotStyleString=='Light':
        # white background
        params = {"ytick.color" : "k",
                  "xtick.color" : "k",
                  "axes.labelcolor" : "k",
                  "axes.edgecolor" : "k",
                 "axes.linewidth" : 2,
                 "xtick.major.width" : 2,
                 "ytick.major.width" : 2,
                 "xtick.major.size" : 8,
                 "ytick.major.size" : 8,
                 "text.color" : "k"}
        baseColor = '#000000'
    plt.rcParams.update(params)
    # font_prop = font_manager.FontProperties(fname='/System/Library/Fonts/Avenir.ttc')
    font_prop = font_manager.FontProperties(fname='C:/Users/Carin/pythonCode/Avenir.ttc')
    matplotlib.rcParams['axes.prop_cycle'] = matplotlib.cycler(color=batlow)
    print('Plotting style is ' + plotStyleString)
    return baseColor

#gene Colors
zfC = {
    'R' : '#7d7d7d',
    'U' : '#B73AB9',
    'S' : '#4364F6',
    'M' : '#59CB3B',
    'L' : '#CE2A22',
    'H' : '#FFAF00',
    'H1' : '#FFAF00',
    'rho'  : '#7d7d7d',
    'sws1' : '#B73AB9',
    'sws2' : '#4364F6',
    'mws1' : '#59CB3B',
    'mws2' : '#59CB3B',
    'mws3' : '#59CB3B',
    'mws4' : '#59CB3B',
    'lws1' : '#CE2A22',
    'lws2' : '#CE2A22',
    'actb2': '#926645',
    'tbx2a': '#c92675',
    'tbx2b': '#7526c9',
    'six7' : '#d6ab00',
}

zfG = {
    'wt' : '#000000',
    'tbx2a' : '#ab266b',
    'tbx2b' : '#421f8e',
    'foxq2' : '#001dd6',
    'nr2e3' : '#7d7d7d',
    'lrrfip1a' : '#00CC6A',
    'xbp1' : '#B73AB9',
    'sall1a' : '#B89504',
    'lhx1a' : '#FFAF00'
}

zfGm = {
    'wt' : 'o',
    'tbx2a' : 'P',
    'tbx2b' : 'X',
    'foxq2' : '^',
    'nr2e3' : '+',
    'lrrfip1a' : 'D',
}

prLabel = {
    'R'  : 'Rods',
    'U' : 'UV',
    'S' : 'S',
    'M' : 'M',
    'L' : 'L',
}

def ansiText(inputText,ansiKey):
    # https://tforgione.fr/posts/ansi-escape-codes/
    ansiKVP = {
        'bold': '\x1B[1m',
        'faint': '\x1B[2m',
        'italic': '\x1B[3m',
        'underlined': '\x1B[4m',
        'inverse': '\x1B[7m',
        'strikethrough': '\x1B[9m',
        'black': '\x1B[30m'	,
        'red': '\x1B[31m'	,
        'green': '\x1B[32m'	,
        'yellow': '\x1B[33m'	,
        'blue': '\x1B[34m'	,
        'magenta': '\x1B[35m'	,
        'cyan': '\x1B[36m'	,
        'white': '\x1B[37m'	,
        'blackBG': '\x1B[40m',
        'redBG': '\x1B[41m',
        'greenBG': '\x1B[42m',
        'yellowBG': '\x1B[43m',
        'blueBG': '\x1B[44m',
        'magentaBG': '\x1B[45m',
        'cyanBG': '\x1B[46m',
        'whiteBG': '\x1B[47m',
        'exit': '\x1b[0m'
    }
    return ('{0}{1}{2}'.format(ansiKVP.get(ansiKey),inputText,ansiKVP.get('exit')))

def ansiRGB(inputText,rgbKey = '122;122;122'):
    # https://tforgione.fr/posts/ansi-escape-codes/
    # rgbKey format = '0-255;0-255;0-255'
    return ('\x1B[38;2;{0}m{1}{2}'.format(rgbKey,inputText,'\x1b[0m'))

def ansiKeyColors(inputText,ansiKey = 'exit'):
    ansiKVP = {
        'R': '125;125;125',
        'U': '183;58;185',
        'S': '67;100;248',
        'M': '89;203;59',
        'L': '206;42;34',
        'exit': '\x1b[0m'
    }
    return ansiRGB(inputText,ansiKVP.get(ansiKey))

# --------
# save image from napari
def savePNGfromNapari (viewer, savePath):
    from skimage.io import imsave
    from skimage import img_as_ubyte, img_as_uint, img_as_float, img_as_int
    
    outPNG = blended_img(viewer)
    outPNG = img_as_ubyte(outPNG/np.max(outPNG)) # output from blended image is float64 with weird range
    imsave(savePath + '.png', outPNG)
    
def blended_img(viewer):
    blended = np.zeros(viewer.layers[0].data.shape + (4,))
    for layer in viewer.layers:
        # normalize data by clims
        normalized_data = (layer.data - layer.contrast_limits[0]) / (layer.contrast_limits[1] - layer.contrast_limits[0])
        colormapped_data = layer.colormap.map(normalized_data.flatten())
        colormapped_data = colormapped_data.reshape(normalized_data.shape + (4,))

        blended = blended + colormapped_data
    
    # blended[..., 3] = 1 # set alpha channel to 1

    return blended
# ----------
def formatFigureMain(figH, axH, plotH):
    font_path = 'C:/Users/Carin/pythonCode/Avenir.ttc'
    fontTicks = font_manager.FontProperties(fname=font_path, size=30)
    fontLabels = font_manager.FontProperties(fname=font_path, size=36)
    fontTitle = font_manager.FontProperties(fname=font_path, size=32)
    axH.set_xscale('linear')
    axH.spines['top'].set_visible(False)
    axH.spines['right'].set_visible(False)
    
    for label in (axH.get_xticklabels() + axH.get_yticklabels()):
        label.set_fontproperties(fontTicks)
    axH.set_xlabel(axH.get_xlabel(), fontproperties = fontTicks)
    axH.set_ylabel(axH.get_ylabel(), fontproperties = fontTicks)
    return fontLabels

def lighten_color(color, amount=0.5):
    """
    Lightens the given color by multiplying (1-luminosity) by the given amount.
    Input can be matplotlib color string, hex string, or RGB tuple.

    Examples:
    >> lighten_color('g', 0.3)
    >> lighten_color('#F034A3', 0.6)
    >> lighten_color((.3,.55,.1), 0.5)
    """
    import colorsys
    try:
        c = matplotlib.colors.cnames[color]
    except:
        c = color
    c = colorsys.rgb_to_hls(*matplotlib.colors.to_rgb(c))
    return matplotlib.colors.rgb2hex(colorsys.hls_to_rgb(c[0], 1 - amount * (1 - c[1]), c[2]))

def estimateJitter(dataArray):
    """ creates random jitter scaled by local density of points"""
    from scipy.stats import gaussian_kde
    kde = gaussian_kde(dataArray)
    density = kde(dataArray)
    jitter = np.random.randn(len(dataArray))*density
    return jitter

def formatFigure(figH, axH, plotH):
    fontLabels = formatFigureMain(figH, axH, plotH)
#     axH.set_xlabel('wt vs. cr', fontproperties=fontLabels)
    axH.set_ylabel('cells per 64 x 64 $\mu$m$^2$', fontproperties=fontLabels)
    axH.xaxis.set_tick_params(rotation=45)

def formatFigureRvU(figH, axH, plotH):
    fontLabels = formatFigureMain(figH, axH, plotH)
    axH.set_xlabel('Rods per 64 x 64 $\mu$m$^2$', fontproperties=fontLabels)
    axH.set_ylabel('UV cones per 64 x 64 $\mu$m$^2$', fontproperties=fontLabels)
    axH.xaxis.set_tick_params(rotation=45)
    
def formatFigureMvS(figH, axH, plotH):
    fontLabels = formatFigureMain(figH, axH, plotH)
    axH.set_xlabel('M cones per 64 x 64 $\mu$m$^2$', fontproperties=fontLabels)
    axH.set_ylabel('S cones per 64 x 64 $\mu$m$^2$', fontproperties=fontLabels)
    axH.xaxis.set_tick_params(rotation=45)
    
def cellCounter(viewer,dirAnalysis,gene,filePath,photoLabels):
    # to check that cell counts in csv file are correct
    import os.path
    # clear viewer
    for l in viewer.layers:
        viewer.layers.remove(l)
    viewer.layers.select_all()
    viewer.layers.remove_selected()
    dirOut = dirAnalysis + gene + '/' + filePath + '/'
    print('{0}:'.format(filePath))
    for photoLabel in photoLabels:
        # try to load segmentation first, if not try to load points
        segPath = dirOut + photoLabel + "_seg_curated.tiff"
        pointPath = dirOut + photoLabel + "_points.csv"
        if os.path.isfile(segPath):
            lName = photoLabel + '_seg'
            viewer.open(segPath, name=lName, plugin='napari', blending='additive');
            nCells = np.unique(viewer.layers[lName].data).shape[0]
            photoUnit = 'segmented cells'
        elif os.path.isfile(pointPath):
            lName = photoLabel + '_points'
            viewer.open(pointPath, name=lName, plugin='napari',symbol='disc', size=10, face_color=zfC[photoLabel]);
            nCells = len(viewer.layers[lName].data)
            photoUnit = 'pointed nuclei'
        else:
            nCells = float("nan")
            photoUnit = ''
        print(ansiKeyColors('\tn{0} = {1} {2}'.format(photoLabel,str(nCells),photoUnit),photoLabel))
        
def getFileList(dirData,gene,fileNameMatch,addDetails=''):
    fileList = sorted([f for f in os.listdir(dirData) if not f.startswith('.')]) # get all the files in the data directory (excluding system files) and sort them alphabatically
    fileList = ([f for f in fileList if gene in f]) # select files that match the gene of interest
    fileList = ([f for f in fileList if any([s in f for s in fileNameMatch])]) # only keep relevant files
    if (addDetails=='path'):
        fileList = (['# filePath = \'' + f for f in fileList]) # add text before each file
        fileList = list(map(lambda st: str.replace(st, '.nd2', '\'; gene = \'' + gene + '\'; '), fileList)) #remove file extension (.nd2) and add text after each file
    elif (addDetails=='list'):
        fileList = (['\'' + f for f in fileList]) # add text before each file
        fileList = list(map(lambda st: str.replace(st, '.nd2', '\','), fileList)) #remove file extension (.nd2) and add text after each file
    else:
        fileList = list(map(lambda st: str.replace(st, '.nd2', ''), fileList)) #remove file extension (.nd2) and add text after each file
    return fileList


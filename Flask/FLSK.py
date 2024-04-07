from flask import Flask, render_template, request
import random

import matplotlib
matplotlib.use('Agg')
import numpy as np

import matplotlib.pyplot as plt
from matplotlib import animation
from matplotlib import colors
from IPython import display

def dot(vec1,vec2):
    return vec1[0]*vec2[0] +vec1[1]*vec2[1]


def norm(vec):
    mag = np.sqrt((vec[0]*vec[0])+(vec[1]*vec[1]))

    vec[0] /= mag
    vec[1] /= mag

    return vec


winddir = [1,1]
nuwind = norm(winddir)



resx, resy = 100 , 100
humidity = 0.2
tallTreeDensity = 0.5
tallTreeMod = 0.01

rang = random.uniform(5,20)

startex = random.uniform(1,resx-rang)
endex = startex +rang
startey = random.uniform(1,resx-rang)
endey = startey +rang

elevationModifier = 0.1

def iterate(X):
    """Iterate the forest according to the forest-fire rules."""

    # The boundary of the forest is always empty, so only consider cells
    # indexed from 1 to nx-2, 1 to ny-2
    X1 = np.zeros((resy, resx))
    for ix in range(1,resx-1):
        for iy in range(1,resy-1):

            if X[iy,ix] == TREE or X[iy,ix] == TALLTREE or X[iy,ix] == ETREE or X[iy,ix] == ETALLTREE:
                mod = 0
                if X[iy,ix] == TALLTREE:
                    mod = tallTreeMod
                elif X[iy,ix] == ETREE:
                    mod = elevationModifier
                elif X[iy,ix] == ETALLTREE:
                    mod = elevationModifier+tallTreeMod

                nuvec = [ix-fireStart[0],iy-fireStart[1]]
                mod += ((dot(norm(nuvec),winddir)+0.1))*0.4
              #  print(((dot(norm(nuvec),winddir)+0.1)))*0.1


                X1[iy,ix] = X[iy,ix]
                for dx,dy in neighbourhood:

                    if abs(dx) == abs(dy) and np.random.random() < 0.573:
                        continue
                    if X[iy+dy,ix+dx] == FIRE and (random.uniform(0, 1) > humidity+mod):
                        X1[iy,ix] = FIRE
                        break

            elif ix > startex and ix < endex and iy > startey and iy < endey:

                X1[iy, ix] = EEMPTY

              #  else:
                  #  if np.random.random() <= 0.001:
                    #    X1[iy,ix] = FIRE
    return X1






neighbourhood = ((-1,-1), (-1,0), (-1,1), (0,-1), (0, 1), (1,-1), (1,0), (1,1))

forestDenssity = 0.7;
fireStart = [50,50]

cols =[(0.2,0,0), (0,0.7,0), (0.9,0,0), (0,0.4,0),  (0.4,0.2, 0.1) , (0.21,0.87,0.21) , (0.11,0.77,0.11)  ]
EMPTY, TREE, FIRE, TALLTREE, EEMPTY, ETREE, ETALLTREE  = 0, 1, 2, 3,4,5,6
colmap = colors.ListedColormap(cols)
bounds = [0,1,2,3,4,5,6,7]
n = colors.BoundaryNorm(bounds, colmap.N)


x = np.zeros((resx, resy))






for i in range(1,resy-1,1):
    for j in range(1, resx - 1, 1):
        if(j > startex and j < endex and i > startey and i < endey ):
            x[i,j] = EEMPTY
            if(random.uniform(0, 1) < forestDenssity):
                x[i, j] = ETREE

            if x[i, j] == ETREE and random.uniform(0, 1) > tallTreeDensity:
                x[i, j] = ETALLTREE

        else:
            x[i, j] = random.uniform(0, 1) < forestDenssity
            if x[i, j] == TREE and  random.uniform(0, 1) > tallTreeDensity:
                x[i, j] = TALLTREE



x[fireStart[0], fireStart[1]] = FIRE

fig = plt.figure(figsize=(10,10))
a = fig.add_subplot(111)
a.set_axis_off()

im = a.imshow(x,colmap,n)




app = Flask(__name__, static_folder='static')


@app.route('/sim', methods=['GET', 'POST'])
def simu( ):
    if request.method == "POST":
        print("Here")
        global humidity
        humidity = float(request.form['Humidity'])
        global tallTreeMod
        tallTreeMod = float(request.form['Tall'])
      #  global tallTreeDensity
      #  tallTreeDensity = float(request.form['TDensity'])
        print(float(request.form['Tiny']))
        global forestDenssity
        forestDenssity = float(request.form['Density'])
        global elevationModifier
        elevationModifier = float(request.form['Modifier'])
        global winddir
        global nuwind
        winddir[0] = int(request.form['wind1'])
        winddir[1] = int(request.form['wind2'])
        nuwind = norm(winddir)

        def animate(i):
            im.set_data(animate.X)
            animate.X = iterate(animate.X)

        animate.X = x
        plt.rcParams[
            'animation.ffmpeg_path'] = 'C:\\Users\\marti\\Documents\\ffmpeg-7.0-essentials_build\\bin\\ffmpeg.exe'
        interval = 50
        anim = animation.FuncAnimation(fig, animate, interval=interval, frames=200)
        # plt.show()

        video = anim.to_html5_video()

        # print(video)
        # embedding for the video
        html = display.HTML(video)

        # print( html.data)
        # draw the animation
        display.display(html)
        plt.close()
        # return
        return render_template('index3.html', name=video)
    return render_template('index3.html')

@app.route('/home', methods=['GET', 'POST'])
def hello1( ):
    return render_template('index2.html')


@app.route('/', methods=['GET', 'POST'])
def hello():

    return render_template('index.html')



if __name__ == '__main__':
    app.run('127.0.0.1', 5000, debug=True, threaded=False)
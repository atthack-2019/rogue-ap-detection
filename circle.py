import matplotlib.pyplot as plt
import my_trilateration

c1 = my_trilateration.Circle(407,222,152.0182738030424)
c2 = my_trilateration.Circle(546,395,78.7322553235653)
c3 = my_trilateration.Circle(83,110,259.53757108554686)
c4 = my_trilateration.Circle(631,312,10.253201506510855)
#c5 = my_trilateration.Circle(200,371,805.1857368246614)
c6 = my_trilateration.Circle(206,877,756.4734324616041)
circle_ls = [c1, c2, c3, c4, c6]
colors = ['b', 'g', 'r', 'c', 'm', 'y', 'k', 'w']
def print_circles(circles_ls):
    plt_circles = []
    for i in range (len(circles_ls)):
        circle = circles_ls[i]
        plt_circles.append(plt.Circle((circle.x, circle.y), circle.radius, color = colors[i], alpha=0.5))
    fig, ax = plt.subplots()
    plt.grid(linestyle='--')
    ax.set_xlim((-1000, 1000))
    ax.set_ylim((-1000, 1000))
    for c in plt_circles:
        ax.add_artist(c)
    fig.savefig('plotcircles.png')

print_circles(circle_ls)
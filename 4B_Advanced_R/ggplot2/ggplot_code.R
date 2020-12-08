library(ggplot2)

mpg <- ggplot2::mpg   #import data

ggplot(data=mpg)  #assign data to ggplot object

#Scatter plots and basic aesthetics

ggplot(data=mpg) +
  geom_point(mapping=aes(x=displ,y=hwy))  #displ is engine displacement, hwy is engine fuel efficency

ggplot(data=mpg) +
  geom_point(mapping=aes(x=displ,y=hwy, color=class))  #displ is engine displacement, hwy is engine fuel efficency

ggplot(data=mpg) +
  geom_point(mapping=aes(x=displ,y=hwy, size=class))  #displ is engine displacement, hwy is engine fuel efficency

ggplot(data=mpg) +
  geom_point(mapping=aes(x=displ,y=hwy, alpha=class))  #displ is engine displacement, hwy is engine fuel efficency

ggplot(data=mpg) +
  geom_point(mapping=aes(x=displ,y=hwy, shape=class))  #displ is engine displacement, hwy is engine fuel efficency

ggplot(data = mpg) + 
  geom_point(mapping = aes(x = displ, y = hwy), color = "blue") #manual setting of point color 

ggplot(data=mpg) + 
  geom_point(mapping=aes(x=displ, y=hwy),
             color="blue") +
  labs(title="Example scatterplot",
       x="Displacement", y="Highway efficency")

#Facet wrap
ggplot(data = mpg) + 
  geom_point(mapping = aes(x = displ, y = hwy)) + 
  facet_wrap(~ class, nrow = 2)         #separate into individual plots by class and arrange in 2 rows

ggplot(data = mpg) + 
  geom_point(mapping = aes(x = displ, y = hwy)) + 
  facet_grid(drv ~ cyl)           #separate into individual plots by drive type and number of cylinders arranged as a grid

#Multiple geometry layers

ggplot(data = mpg) + 
  geom_smooth(mapping = aes(x = displ, y = hwy))

ggplot(data = mpg) + 
  geom_smooth(mapping = aes(x = displ, y = hwy, linetype = drv))

ggplot(data = mpg) + 
  geom_point(mapping=aes(x=displ,y=hwy, color=drv)) +
  geom_smooth(mapping = aes(x = displ, y = hwy, linetype = drv))

#global mapping
ggplot(data = mpg, mapping = aes(x = displ, y = hwy)) + 
  geom_point(mapping=aes(color=drv)) +
  geom_smooth(mapping=aes(linetype=drv))

#bar plot

ggplot(data=mpg) +
  geom_bar(mapping=aes(x=class))

#stat transformations
ggplot(data=mpg) +
  stat_count(mapping=aes(x=class))

#coordinates
ggplot(data = mpg, mapping = aes(x = class, y = hwy)) + 
  geom_boxplot()
ggplot(data = mpg, mapping = aes(x = class, y = hwy)) + 
  geom_boxplot() +
  coord_flip()

bar <- ggplot(data = mpg) + 
  geom_bar(
    mapping = aes(x = class, fill = class), 
    show.legend = FALSE,
    width = 1
  ) + 
  theme(aspect.ratio = 1) +
  labs(x = NULL, y = NULL)

bar + coord_flip()
bar + coord_polar()

ggsave("my_plot.png", plot=bar)

ggplot(data=mpg) +
  geom_histogram(mapping=aes(x=hwy),
                 col="black",
                 fill="grey")
                             
mid <- ggplot2::midwest

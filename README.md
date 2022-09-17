# [Smartographer](http://smartographer.fly.dev)

## About

Smartographer is a map generation web app, by James Maphis.<br>
You currently can make dungeon, cave and world maps by pressing their respective buttons. <br>
To get a new map of the chosen type, press the refresh button.<br>
If you find a map you would like to save, you can create an account and sign in. then simply give the map a name, and hit save!<br>
(Currently Smartographer is just a proof of concept.  We cannot guarantee that user accounts and maps will not be deleted.)<br>
<br>
There is currently a rare bug which will cause the site to crash while trying to view a specific map type. <br>
To fix this, you can reset that map type by clicking the corresponding link below:<br>
[Cave](http://smartographer.fly.dev/maps/refresh_cave)<br>
[Dungeon](http://smartographer.fly.dev/maps/refresh_dungeon)<br>
[World](http://smartographer.fly.dev/maps/refresh_world)<br>

## How it Works

Smartographer is powered by 3 separate procedural generation algorithms, which serve as the back end. <br>
They are connected to the front end by a Map Manager object, which fetches a map of the appropriate type.<br>
These maps are represented by two dimensional arrays of binary integers, which the Map Manager converts /<div/> tags.<br>
These underlying algorithms are as follows:<br>

### [Cave](https://smartographer.fly.dev/maps/gen/cave)

  The cave maps are generated using a technique called [Random Walk](https://en.wikipedia.org/wiki/Random_walk). 

### [Dungeon](https://smartographer.fly.dev/maps/gen/dungeon)

### [World](https://smartographer.fly.dev/maps/gen/world)

Check out the syntax reference foulder and read the README document. We should finish that up before we start working on
a project.  

The attributes of good project candadates are: Possible
to finish at least the first itteration within a week, easy to collaborate independently on (this means it would be nice if 
there were seperate features that don't really over ap for us to each work on side by side), within our mathmatical capabilites.

My ideas for projects we could attempt are the following (add your own ideas and we can decide on one):

2d physics engine
This can be very simple or very complex, we could start by setting up some basic graity and collision rules for simple objects.
Could add friction and more complicated torqe calculations to allow things to rotate when they hit each other

3d graphics engine
this is a lot of trig but i think it could be cool to write our own library that allows us to position simple 3d objects like
rectangles in 3d space, if we wanted to go ham we could add the ability to rotate the objects and shade the sides based on placement
of the light source

Try to make a better version of Coos's errosian simulator
He is constrained to a really shity graphics engine, we could find a better one or build our own.

Simulate some kind of evolution (huge number of videos on youtube about this)
I honesty don't know where to begin with this bc i don't know that much about the specifics of how evolution works but I'm sure 
we could figure it out. Seems like it might be more research than coding though and it may take a lot more than a week

Unique game idea I had involving sphere collisions
We would probably only have time to code the basic structure of the game and probably not have time to add competative functionality
but hear me out: there are a bunch of circles in 2d space floating around with random velicies and sizes. Your character 
is stuck to the peremeter of spheres and can walk counter clock wize or clock wize around the spere. The character can also jump
from the sphere he is currently on, to another sphere. We could code the physics so that when the spheres ran into eachother
they would conserve momentum and rebound off eachother accordingly. Also the character has mass so when he jumps, the sphere he was
on gets an impulse, and the sphere he lands on also expereinces an impulse. You die if you are smashed between two spheres.

^^ above is all we would realistically have time to build, but below i have outlined what gameplay would actually be like if 
we decided to continue the project

This would be a multi player mobile game. The character would have a gun of sorts and the ability to plant explosives. 
bullets would follow real physics, adding the initial momentum of the bullet to the momentum imparted by the gun. This means
if you were on a planet that was rotating and translating, the bullet would move off in a tangental path from the sphere
but keep its translational initial momentum. I've not seen a game like this before and i think it could be lit if done right.
would involve a lot of tweaking of physics to get it to feel just right.


# What is Grafana
Grafana is a visualization tool that can fetch data from data sources and visualize them.

# Why Grafana
Good question. The only thing Grafana can do easily is look pretty. Configuring Grafana, using dynamic values as thresholds are any other basic functionality is at least a 10 hour journey to implement. The chances are high it won't work. Either that or I am just very incompetent. Considering I tried about every solution I could find I come to the conclusion that the problem lies within Grafanas way of doing things.

# Problems/TO-DOs
Grafana.ini is not correctly overridden. I do not know why. It should work. It just doesn't
Setting Tresholds for the plant data dynamically doesn't work, since Grafan is not able to parse a variable when trying to use it. The next best approach is probably to set up a Server that serves a json-file. Which then would be needed to be implemented in Grafana using some third-party plugin. I could not get this to work
Using Data Transformation to set thresholds dynmically after wrtiting data to Influx also didn't work. Again, I do not know why. It kinda worked but then broke immediately after. This could be due to storing the data in Influxx and the timestamp changing. This is in itself probably not a very good approach and it would be way smarter just to use a json file for configuring this. Which Grafana does not support.
Alerts do work, however they are not very recognizable in my humble opinion.

# Recommendations
Using HTML, CSS and JS (in combination with any library or framework) would probably look not as pretty. That being said I wholeheartedly believe that it would've been faster, more fun and overall the better experience. Should there be time left this is what I would focus on.
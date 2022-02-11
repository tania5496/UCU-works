# Main
Main is a Python-written program that takes as arguments the year, longitude, and latitude of a user's location and the path to the file where the movie database and information are located. The program returns a html file containing a map showing the 10 nearest filming locations of the specified year.
## Сmponents of the program
The program consists of three functions. 

The first function is line_processing. It processes the line from the file and returns list of film's name and place. 

The second function is distance_calculator. It returns distance between location of user and location of film.

The last function main contains the rest of the code and the calls of the two previous functions.

## The results of the program
The result of this program is a html file, opening which you can see the map. It has two themes - light and dark. This map contains three layers.

The first layer has a marker of location of user.

On the second layer there are the 10 closest to the user's location filming locations of the specific year.

On the third the same markers as on the second layer, but markers are in the form of circles

## An example of how this program works
Рік - 2000
Локація - УКУ
>>> python main.py 2000 49.83826 24.02324 C:\Users\tetia\.vscode\projects\locations1.list
![photo5202052037045500581](https://user-images.githubusercontent.com/87234112/153662113-261f759b-abae-4f96-9d1d-e992f824ed57.jpg)


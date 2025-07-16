# Bear-Scrap
## Presentation
Bearstech, a company specializing in hosting and IT management, publishes a post on LinkedIn every day throughout the summer to showcase free software. The initiative is really cool, but it's not always easy to find these posts on LinkedIn and keep track of them. Being a free software enthusiast, transitioning into IT, and having "OursBlanc" as my nickname, I had to do something about it!

## Idea
Create a scraping system to retrieve each software presented in these posts and display them statically on a web page to keep a record and find them easily.

I have just completed a year of retraining in IT, so please forgive any minor deviations from best practices as I may not yet have all the instincts and still have much to learn.

## How it works?
I wanted to use an API to scrape posts from the Bearstech page, but it seems it's not possible to scrape company pages that way. So, I used Selenium to scrape the page "like a human."

The operation is quite simple:
There is a CSV file that records the posts from the Bearstech page. (Given that there normally won't be a huge number of entries, I preferred using a .csv over a real database.)

We log in to LinkedIn using the credentials contained in the config file, then we go to the Bearstech page, scroll through the posts, and when we come across a post titled "Les logiciels libres de l'été," we expand the post, scrape it using a regex, and set it aside (unless that post is already in the .csv). Once we reach the "Logiciel de l'été jour 1" (the first one), we stop there and save everything in the .csv.

## Installation
Download the repository
setup the env
launch the script
wait approx 2 minutes

then launch the index.html and "voila" you have a webpage with nice formating

### Deployment
I've self hosted the project here, with a cron task, i schedule each day at 1:00 the scan of linkedin to continuously populate the page


## Disclaimer
Apparently, linkedin n'aime pas trop qu'on fasse plein de requete comme ça, donc il faut utiliser ça avec parcimonie. Vu que l'on se log avec un compte utilisateur je pense qu'il y a un risque de se faire perma-ban.



## Improvement
La logique algorithmique peut certainement être amélioré (j'ai essayé d'optimiser ça mais j'ai pas réussi à trouver un moyen de limiter le nombre de boucle avec Selenium qui rescan tous les posts à chaque fois... Dans l'idéal il faudrait scanner que les nouveaux poste une fois qu'on a scrollé et afficher de nouvelles publications

## License
[![License: CC BY-NC-SA 4.0](https://img.shields.io/badge/License-CC%20BY--NC--SA%204.0-lightgrey.svg)](https://creativecommons.org/licenses/by-nc-sa/4.0/)

## Made with love
I made this myself with my bear paws. It's a small personal project to populate my GitHub and help in my job search.

## Remerciements
https://codepen.io/uchardon/pen/bxbqoG/ pour le footer "vague" que j'ai repimpé à ma sauce derriere


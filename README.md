# Tube Ratings

Milestone Project Three: Data Centric Development - Code Institute

This site lets users vote for their favourite TV shows and movies, and see what other people think as well. As I currently work in a cinema, I have a huge affinity for movies and tv shows, and would like to gauge other peoples opinions on these.

A live version can be found on [Heroku](https://tuberatings.herokuapp.com/).

## UX

When I was laying out this project, I chose to make it as simple looking as possible to allow for the best user experience.

As a user, I want the following:

- See what movies people are voting for.

- Be able to add my own TV shows and vote for them

- See which actor/actress was in a particular movie

- Get a glimpse of the poster used to advertise the show

- Watch a trailer to see if I might be interested in a movie

I mocked up an early desktop-first layout using Balsamiq
![mockup](https://i.imgur.com/2Yh9wiq.png)

I tested for responsiveness using the site, [Am I Responsive?](http://ami.responsivedesign.is/)
![responsiveness](https://i.imgur.com/dmfWOyW.png)

## Features

### Existing Features

- Cards - gives a quick glimpse at the poster and synopsis for the entry
- Voting - lets users vote up or down their favourite entries
- Edit - Users can change why an entry is included in the list
- View All - Allows users to browse through all entries in a category
- Delete - Remove an entry from the listing, if you don't think it should be there
- Modals - provide a warning before deleting an entry
- Forms - used to input info about an entry

### Features Left to Implement

- User accounts - currently anyone can edit or delete anyone elses entry. With user accounts, I could limit this to only the person who first added an entry. It would allow me to limit voting to once per user.
- Comments section - Allow users to not only vote, but leave a comment on why they like (or dislike) a particular title. This would have to be moderated however to prevent unwanted speech on the site.

## Technologies Used

- HTML
  - Used for the structural elements of the site
- CSS
  - Used to style the HTML elements
- [Materialize CSS](https://materializecss.com/)
  - Used to give access to a multitude of helper classes for CSS
- [jQuery](https://jquery.com/)
  - Used for DOM manipulation
- [OMDb](http://www.omdbapi.com/)
  - Used to retrieve movie and tv show info
- [Google Python Library](https://github.com/googleapis/google-api-python-client)
  - Used to retrieve trailers from Youtube
- [Am I Responsive](http://ami.responsivedesign.is/)
  - Used to test for responsiveness across different device sizes
- [Waitress](https://docs.pylonsproject.org/projects/waitress/en/stable/)
  - Used as a production level server for Heroku

## Testing

- Validation

  - The code was ran through the HTML and CSS validators provided by the W3C, available [here](https://validator.w3.org/). IDs were added to certain elements, to get around some of Materialize's high specificity selectors. All code came back with no issues from the validators.

- Unit Tests

  - I wrote some unit tests using Flasks built in testing suite. I added 2 tests for each of my views, one valid test, designed to pass, and one invalid test, designed to throw an error and be caught by the view. All tests passed successfully. As I added new code, I followed test driven development, and wrote a test first, then made the function as basic as possible to fail on first run. I proceeded to write code to make the test pass.

- Visual Testing

  - While developing, I loaded the site in Firefox mainly, while also checking Chrome on desktop, and Safari on mobile, to ensure the most used browsers could use the site without any issues.

## Deployment

This site was coded using Visual Studio Code. Code was tested using by using the WSGI app built into Flask, but on deployment to Heroku, will use Waitress.

This site is hosted on Heroku, deployed from the master branch of the GitHub repository. There are no differences between the development and deployed version.

To clone this repository to run locally, you can do the following:

- Create a new repository on Github
- Clone my repository with the following commands on your local machine:

  ```
  git clone https://github.com/Prejudice182/prej-milestone-three.git
  git remote rename origin upstream
  git remote add origin *URL TO NEW GITHUB REPO*
  git push origin master
  ```

- Deploy to Heroku by completing the following:
  - Create a new application, in whichever region suits you best
  - Click the "Connect to Github" link displayed in the Deploy section of your app
  - Pick the repository from your list of available repositories
  - You can set this to deploy automatically whenever a new push to Github is made, or manually when feel your code is ready

## Credits

### Content

- All posters and trailers are copyright content belonging to their respective distribution companies, and are used here under Fair Use.

### Media

- The posters are hosted by Amazon, retrieved from the OMDB API
- Youtube videos are hosted by Google, retrieved from the Youtube API

### Acknowledgements

- I received inspiration for this site from visiting various streaming sites.
- Thanks to my mentor, [Oluwaseun Owonikoko](https://github.com/seunkoko)
- Thanks to all members of the Code Institute Slack workspace

import React from 'react';
import './Main.css';
import Navbar from './Navbar';
import './About.css';
import Iframe from 'react-iframe';

const About = () => {
  return(
    <div className="about-container">
      <Navbar />
      <div className="about-intro">
        Hello! This is ECS 171 Group 9.
      </div>
      <div className="about-body-container">
        <div className="about-body">
          This is our long quarter project with inspiration from machine learning! 
          We decided to go with the route of music since music is all around the world and evokes emotion and discourse.
          At the bottom of the page, you can find our video demo presentation. 
          On the home page, you can click on the "Generate" Button! to start generating your music. 
          On the library page, you can find a list of songs that were previous generated that redirects you to the music player page after clicking "Play" on a specific song.
        </div>
        <Iframe url="https://www.youtube.com/embed/GZ77Jkfwa8o"
          width="1120px"
          height="630px"
          frameborder="0"
          className="about-yt-video"
          position="relative"/>
      </div>
    </div>
  )
}

export default About;
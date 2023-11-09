# TimeAware
### Video Demo: #TODO
### Description:
### **Empowering Self-Improvement through Mindful Habit Tracking**
The idea of TimeAware has been with me for years, but it was the challenge during CS50's Introduction to Computer Programming that motivated me to bring it to life. The result? A simple and minimalistic app designed to help you track your habits without any fuss.  
We all have our mix of 'good' and 'bad' habits - some we cherish and want to cultivate further, while others we'd rather keep in check. Yet, it's easy to lose track of time when these habits become second nature. I've been there myself, guilty as charged.  
TimeAware was born out of my desire for self-improvement - a tool to effortlessly identify and monitor daily activities, empowering me to nurture the positive and free up space for what truly matters.
With TimeAware, I've kept things clean and straightforward. No distractions, no complications. Just an app that gives you the power to make mindful choices about your habits.  
Join me on this journey of growth and self-discovery. Let TimeAware be your trusted companion, helping you embrace positive change and make the most of every moment.  
### **Technologies Used**
**Back end**: For the back end of the app, I've used Python with Flask Framework. I loved how lightweight and simple it is. Interesting problems I learned to solve were for example: handling multiple different POST requests no the same .html pages or basic user uthentication on the back end - both using vanilla Python and libraries (for example for email validation)  
**Database**: Connecting to the database, creating new records and displaying data was certainly the most challenging aspect for me. I've used SQLAlchemy library and sometimes GUI database viewer to "control" what happens in my database.  
**Front end**: Front end of the app was built with plain Javascript, Bootstrap for the UI and a bit of custom CSS to make the website a bit less 'generic'. I could probably have done a bit more to make the app look more modern, but I like the current look and trying to tweak alignment and little pixels is not my cup of tea really.  
I've also used Chart.js library for data visualisation in my 'Statistics' subpage, which was by far the biggest challenge. It entailed, for example properly structuring the data on the back end for the chart to work for multiple activities or getting the chart to display those activities simultaneously.  
**Deployment**: I've used Docker to "containerize" my project and deployed it eventually on fly.io. It was a total nightmare and felt incredibly overwhelming. After so many errors and frustration, it's eventually up-and-running.

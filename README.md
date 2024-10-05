<a href="https://manikantapuppala.pythonanywhere.com/"><h1 align="center">Blog-Lite Application</h1></a>

## Roadmap of the Project

1. Set up authentication system with email OTP (SMTP).
2. Develop user profile features, including account info, post history, and follow/follower stats.
3. Create a feed system displaying user-specific content and top posts.
4. Implement functionalities for creating, editing, and deleting posts.
5. Introduce community features allowing users to follow/unfollow others and interact with posts (likes, comments, shares).
6. Add admin panel for managing users and their posts.
7. Ensure smooth deployment on local systems and REPLIT.

## Project Description

The **Blog-Lite Application** is a multi-user platform designed for users to create, interact with, and share blog posts. It includes both user and admin roles. Below are the features of the application:

### User Features:
- **Authentication**: Users can register using their email, receive OTPs via SMTP, and authenticate their accounts.
  - Account creation, password reset, and OTP validation are done through email.
- **Profile Management**: Users can view and edit their account information easily.
  - Profile includes name, email, profile picture, follower/following counts, and recent posts.
- **Search**: Users can search posts using the title or description.
- **Home Feed**: The home feed shows posts from followed users and top-ranked posts based on likes and comments.
  - Users can interact with posts by liking, commenting, and sharing.
  - Time stamps and profile pictures of the post authors are visible.
- **Post Creation**: Users can create posts with a title, content, and image, and edit them later if needed.
- **Community Interaction**: Users can follow/unfollow others and see their posts in their feed.

### Admin Features:
- **User Management**: Admins can view all user details and delete users as needed.
- **Post Moderation**: Admins can review posts and manage content to maintain community standards.

---

## Project Design Flow

1. **Authentication Flow**: User registration with email OTP, password management, and login functionality.
2. **Profile Flow**: User details displayed and editable in the profile section.
3. **Feed Flow**: Feed is dynamically generated based on users followed and top posts.
4. **Post Flow**: CRUD (Create, Read, Update, Delete) functionality for user posts.
5. **Admin Flow**: Admins handle moderation tasks for both users and posts.

---

## Project Requirements/Features

- Email-based OTP Authentication
- User Profiles
- Real-time Feeds
- Post Interactions (Likes, Comments, Shares)
- Admin Controls
- Follower/Following System

---

## Admin

- **View All Users**: Admins can view a list of all users in the system.
- **Delete Users**: Admins can remove users and their details if needed.
- **Post Moderation**: Admins can monitor and manage user posts for quality control.

---

## User

- **Registration and Login**: Users register using an email address and password (OTP-based authentication).
- **Profile Page**: Users can view and update their profile information.
- **Posts**: Users can create, edit, delete, and interact with posts.
- **Community Interaction**: Users can follow/unfollow others and engage with their posts.

---

## Other Features

- **Email Notifications**: OTPs for authentication and password recovery.
- **Responsive Design**: The application is designed to work seamlessly on various devices.
- **Search Functionality**: Users can search for posts based on keywords in titles or descriptions.

---

## Software Specifications

- **Backend**: Python (Flask Framework)
- **Frontend**: HTML, CSS, JavaScript (Bootstrap for UI components)
- **Database**: SQLite3
- **Authentication**: Email OTP via SMTP
- **Deployment**: PythonAnywhere for online hosting

---

## Non-Functional Requirements

- **Scalability**: The application can scale to handle multiple users and posts with ease.
- **Security**: Secure password storage, OTP-based login, and admin-controlled content management.
- **Performance**: Efficient querying for posts and users.
- **Usability**: Simple and intuitive UI/UX for users and admins alike.

---

## Hardware Requirements

- **Processor**: Intel i3 or higher
- **RAM**: 4GB minimum (8GB recommended)
- **Storage**: At least 500MB for installing dependencies

---

## Links and Documents

- **Live Application**: [Blog-Lite Application](https://manikantapuppala.pythonanywhere.com/)
- **Project Repository**: [GitHub](https://github.com/your-repo-url)
- **Technical Documentation**: [Link to documentation]

---

## How to Run Locally in Linux

1. **Download** all the files from the repository.
2. Run the `run.sh` script to install the necessary packages and libraries.
3. Execute `main.py` to trigger the application and start the Python server.
4. Open the local link address displayed by the terminal.
5. Start using the application.

---

## How to Onboard the Platform

1. **Create an Account**: Validate your email with OTP for registration.
2. **Login**: Enter your email and password to access your account.
3. **Password Recovery**: Use OTP to reset your password in case you forget it.
4. **Explore**: After logging in, you can create, edit, or delete posts, modify your profile, follow others, and engage with posts.
5. **Follow Top Posts**: Check out top-ranked posts based on likes and comments.

---

## Why is it Useful?

This application is a **public blog platform** where users can share their posts and interact with content from others. It can be used for educational purposes, community discussions, and knowledge sharing across various domains.

# Setting up React Project using create-react-app

## Table of Contents

- [Introduction](#introduction)
- [Prerequisites](#prerequisites)
- [Setting up a new project](#setting-up-a-new-project)
- [Exploring the File Structure](#exploring-the-file-structure)
- [Running the App](#running-the-app)
- [Conclusion](#conclusion)
- [References](#references)

## Introduction

Welcome to a brief guide on setting up your very first project using Create-React-App! Create-React-App is a robust tool developed to simplify the process of setting up a React project, alleviating the complexity of webpack configurations and the likes.

## Prerequisites

Before diving in, ensure that you have:
- A basic understanding of terminal or command prompt
- Node.js installed on your system

## Setting up a new project

### 1. Opening the Terminal:

- Windows users: Open Command Prompt.
- Mac users: Open Terminal.

### 2. Navigate to Desired Directory:

Using the `cd` command, navigate to the folder where you'd like to set up your project.

### 3. Create a New Project:

To initiate a new project, type:

```bash
npx create-react-app@5 my-react-app
```

**Note**: The "@5" ensures you're using version 5 of `Create-React-App`. Adjustments to tools may occur in future versions, so this ensures consistency.

After running the above command, the tool will begin downloading necessary packages and set up a directory named "my-react-app". This process might take a few minutes.

## Exploring the File Structure

Upon successful installation, you'll notice a set of folders and files have been created. The important ones to note are:

1. **src folder**: This is where the majority of your development will take place. It contains the main JavaScript and CSS files for your application.

2. **public folder**: This houses assets like images, favicons, and the crucial `index.html`. The `index.html` will contain a `div` with an id of "root", which will act as the root element for your React application.

```js
<div id="root"></div>
```

3. **package.json**: A file that holds metadata relevant to the project and lists its dependencies.

Remember, React doesn’t strictly dictate how you structure your projects. `Create-React-App` provides a recommended structure which you can adjust based on your preferences.

Here's the updated set of instructions with an added step to change the directory to `my-react-app`:

## Running the App

To start your app:

1. Open the terminal in VS Code.

2. Change to the project directory by running the command:

```bash
cd my-react-app
```

3. Use the command:

```bash
npm start
```

Your app should now open in a new browser tab, running on `localhost:3000`.

## Conclusion

Congratulations! You've set up and started your first Create-React-App project. As you progress, you can delve deeper into the file structure, making necessary adjustments as per your project requirements. Happy coding! 🌱

## References

- [Create React App Official Documentation](https://reactjs.org/docs/create-a-new-react-app.html#create-react-app)
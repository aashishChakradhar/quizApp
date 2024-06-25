<h1>Quiz Website</h1>
Welcome to the Quiz Website project! This repository contains a web application built using Django, designed to facilitate quizzes for different types of users: students, teachers, and admins. Below, you will find instructions on how to set up, run, and contribute to the project.

<h2> Features</h2>
<ul>
  <li>User Authentication and Authorization</li>
  <li>Role-based access control (Student, Teacher, Admin)</li>
  <li>Create, edit, and delete quizzes (Teacher, Admin)</li>
  <li>Take quizzes and view results (Student)</li>
  <li>Manage users and quizzes (Admin)</li>
</ul>

<h2>User Roles</h2>
<ul>
  <li>Student</li>
  <ul>
    <li>Register and log in</li>
    <li>Take available quizzes</li>
    <li>View their quiz results</li>
  </ul>
  
  <li>Teacher</li>
  <ul>
    <li>Register and log in</li>
    <li>Create, edit, and delete quizzes</li>
    <li>View student results for quizzes they created</li>
  </ul>

  <li>Admin</li>
  <ul>
    <li>Full access to manage quizzes and users</li>
    <li>Perform administrative tasks such as creating new teachers, deleting users, and overseeing the entire platform</li>
  </ul>
</ul>
<h2>Adding a New Quiz (For Teachers and Admins)</h2>
<ol>
  <li>Log in to your account.</li>
  <li>Navigate to the 'Quiz Opeartion' section.</li>
  <li>Fill in the details of the quiz, such as topic, questions and answers.</li>
  <li>Save the quiz.</li>
</ol>

<h2>Taking a Quiz (For Students)</h2>
<ol>
  <li>Log in to your account.</li>
  <li>Browse available quizzes.</li>
  <li>Select a quiz to take.</li>
  <li>Answer the questions and submit the quiz.</li>
  <li>View your results once submitted.</li>
</ol>

<h2>License</h2>
This project is licensed under the MIT License. See the <a href="LICENSE.md">LICENSE</a> file for more details.

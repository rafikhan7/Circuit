importScripts('https://www.gstatic.com/firebasejs/7.13.2/firebase-app.js');
importScripts('https://www.gstatic.com/firebasejs/7.13.2/firebase-messaging.js');
importScripts('https://www.gstatic.com/firebasejs/7.13.2/firebase-analytics.js');
var firebaseConfig = {
        apiKey: "AIzaSyAbJEjFBLObWFbUMSwZFcH8xkTJgZ5ZHww",
        authDomain: "circute-b601d.firebaseapp.com",
        databaseURL: "https://circute-b601d.firebaseio.com",
        projectId: "circute-b601d",
        storageBucket: "circute-b601d.appspot.com",
        messagingSenderId: "404403249494",
        appId: "1:404403249494:web:687d4e5d5dd65ce5f736f7",
        measurementId: "G-6QVPQY4XXM"
    };
      firebase.initializeApp(firebaseConfig);
      const messaging = firebase.messaging();
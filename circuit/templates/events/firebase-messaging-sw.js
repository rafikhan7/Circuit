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
messaging.setBackgroundMessageHandler(function(payload) {
  console.log('[firebase-messaging-sw.js] Received background message ', payload);
  // Customize notification here
  const notificationTitle = 'Background Message Title';
  const notificationOptions = {
    body: 'Background Message body.',
    icon: '/firebase-logo.png'
  };
  send_message_to_all_clients('sound');
  return self.registration.showNotification(notificationTitle,
    notificationOptions);
});

function send_message_to_all_clients(msg) {
    clients.matchAll().then(clients => {
        clients.forEach(client => {
            send_message_to_client(client, msg).then(m => console.log("SW Received Message: " + m));
        })
    })
}

function send_message_to_client(client, msg) {
    return new Promise(function (resolve, reject) {
        var msg_chan = new MessageChannel();

        msg_chan.port1.onmessage = function (event) {
            if (event.data.error) {
                reject(event.data.error);
            } else {
                resolve(event.data);
            }
        };

        client.postMessage("SW Says: '" + msg + "'", [msg_chan.port2]);
    });
}
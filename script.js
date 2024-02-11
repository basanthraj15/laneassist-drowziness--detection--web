import { initializeApp } from "https://www.gstatic.com/firebasejs/10.8.0/firebase-app.js";
import { getDatabase, ref, set, get, child } from "https://www.gstatic.com/firebasejs/10.8.0/firebase-database.js";
import { getAnalytics } from "https://www.gstatic.com/firebasejs/10.8.0/firebase-analytics.js";
import { getAuth, createUserWithEmailAndPassword, signInWithEmailAndPassword, signOut } from  "https://www.gstatic.com/firebasejs/10.8.0/firebase-auth.js";

const firebaseConfig = {
    apiKey: "AIzaSyAaYEj9TDlsx1iHEujKvyl1FOjHi9UDxk4",
    authDomain: "car-connect-c6232.firebaseapp.com",
    projectId: "car-connect-c6232",
    storageBucket: "car-connect-c6232.appspot.com",
    messagingSenderId: "8187568957",
    appId: "1:8187568957:web:d83fc2741b227f23c29b54",
    measurementId: "G-K644JM5TFS"
};

const app = initializeApp(firebaseConfig);
const analytics = getAnalytics(app);
const auth = getAuth();




//logout 
document.getElementById("logout").addEventListener("click", function() {
    signOut(auth).then(() => {
        // Sign-out successful.
        console.log('Sign-out successful.');
        alert('Sign-out successful.');
        window.location.assign("index1.html");
        document.getElementById('logout').style.display = 'none';
      }).catch((error) => {
        // An error happened.
        console.log('An error happened.');
      });		  		  
});
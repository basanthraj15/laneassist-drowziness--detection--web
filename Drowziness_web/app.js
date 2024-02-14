const db = firebase.firestore();
db.collection("Drowzinessdata").get().then((querySnapshot) => {
    querySnapshot.forEach((doc) => {
        const data = doc.data();
        const alertMessage = `Drowziness Detected\nDocument ID: ${doc.id}\nData: ${JSON.stringify(data)}`;
        window.alert(alertMessage);
    });
});

const { initializeApp } = require("firebase/app");
const { firebaseConfig } = require("./config.js");
const {
  getFirestore,
  doc,
  collection,
  listCollections,
  addDoc,
  getDocs,
  setDoc,
} = require("firebase/firestore");
const express = require("express");
const cors = require("cors");

const expressApp = express();
expressApp.use(express.json());
expressApp.use(cors());

const app = initializeApp(firebaseConfig);
const db = getFirestore(app);

const mainDocRef = doc(db, "User", "user1");

// const subDocData = {
//   field1: "value1",
//   field2: "value2",
// };

const addSubDoc = async (body) => {
  try {
    const timestamp = new Date().toISOString();

    const subCollectionRef = collection(mainDocRef, body.iot);
    const subDocRef = doc(subCollectionRef, timestamp);
    await setDoc(subDocRef, { ...body, timestamp });
    console.log("Subkoleksi berhasil ditambahkan dengan ID:", subDocRef.id);
  } catch (error) {
    console.error("Error menambahkan dokumen ke subkoleksi: ", error);
  }
};

// addSubDoc();
expressApp.post("/iotdata", async (req, res) => {
  try {
    const docRef = await addSubDoc(req.body);
    res.status(200).send(`Document added with ID: ${docRef.id}`);
  } catch (e) {
    res.status(500).send("Error adding document: " + e);
  }
});

// get all data from iot1 collection

expressApp.get("/iotdata/:id", async (req, res) => {
  try {
    const querySnapshot = await getDocs(collection(mainDocRef, req.params.id));
    const users = querySnapshot.docs.map((doc) => ({
      id: doc.id,
      ...doc.data(),
    }));
    res.status(200).json(users);
  } catch (e) {
    res.status(500).send("Error getting documents: " + e);
  }
});

// get all data from user collection
// expressApp.get("/iotdata", async (req, res) => {
//   try {
//     const mainCollections = collection(db, "User");
//     const subcollections = await getDocs(mainCollections);

//     const iotCollections = subcollections.filter((collection) =>
//       collection.id.startsWith("iot")
//     );

//     const allDocuments = {};
//     for (const iotCollection of iotCollections) {
//       const collectionRef = collection(db, `mainCollection/${iotCollection}`);
//       const querySnapshot = await getDocs(collectionRef);
//       const docs = querySnapshot.docs.map((doc) => ({
//         id: doc.id,
//         ...doc.data(),
//       }));
//       allDocuments[iotCollection] = docs;
//     }

//     res.status(200).json({
//       message: "IoT Collections fetched successfully",
//       iotCollections: iotCollections,
//     });
//   } catch (error) {
//     console.error("Error fetching IoT collections:", error);
//     res.status(500).json({
//       message: "Error fetching IoT collections",
//       error: error.message,
//     });
//   }
// });

// Dapatkan semua dokumen dari koleksi
// expressApp.get("/users", async (req, res) => {
//   try {
//     const querySnapshot = await getDocs(usersCollection);
//     const users = querySnapshot.docs.map((doc) => ({ id: doc.id, ...doc.data() }));
//     res.status(200).json(users);
//   } catch (e) {
//     res.status(500).send("Error getting documents: " + e);
//   }
// });

// Jalankan server
const PORT = process.env.PORT || 3000;
expressApp.listen(PORT, () => {
  console.log(`Server berjalan pada port ${PORT}`);
});

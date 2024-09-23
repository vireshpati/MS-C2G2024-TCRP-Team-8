import { initializeApp } from "firebase/app";
import { getAuth } from "firebase/auth";

const firebaseConfig = {
  // secrets
};

const app = initializeApp(firebaseConfig);
const auth = getAuth(app);

export { auth };
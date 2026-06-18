// import axios from "axios";

// export default axios.create({
//   baseURL: "http://127.0.0.1:8000"
// });

import axios from "axios";

const api = axios.create({
  baseURL: "https://sml-backend-agdr.onrender.com"
});

export default api;

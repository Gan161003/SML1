// // import axios from "axios";

// // const API = axios.create({
// //   baseURL: "http://127.0.0.1:8000",
// // });

// // export const getSummary = async () => {
// //   const res = await API.get("/dashboard/summary");
// //   return res.data;
// // };

// // export const getPlatforms = async () => {
// //   const res = await API.get("/dashboard/platforms");
// //   return res.data;
// // };

// // export const getSentiment = async () => {
// //   const res = await API.get("/dashboard/sentiment");
// //   return res.data;
// // };

// // export const getLatest = async () => {
// //   const res = await API.get("/dashboard/latest");
// //   return res.data;
// // };









// import axios from "axios";

// const API = axios.create({
//   baseURL: "http://127.0.0.1:8000",
// });

// export const getSummary = async () => {
//   const res = await API.get("/dashboard/summary");
//   return res.data;
// };

// export const getPlatforms = async () => {
//   const res = await API.get("/dashboard/platforms");
//   return res.data;
// };

// export const getSentiment = async () => {
//   const res = await API.get("/dashboard/sentiment");
//   return res.data;
// };

// export const getLatest = async () => {
//   const res = await API.get("/dashboard/latest");
//   return res.data;
// };

// export const getBrands = async () => {
//   const res = await API.get("/dashboard/brands");
//   return res.data;
// };

// export const getHashtags = async () => {
//   const res = await API.get("/dashboard/hashtags");
//   return res.data;
// };

// export const getKeywords = async () => {
//   const res = await API.get("/dashboard/keywords");
//   return res.data;
// };

// export const getTopYoutube = async () => {
//   const res = await API.get("/dashboard/top-youtube");
//   return res.data;
// };

// export const getTopInstagram = async () => {
//   const res = await API.get("/dashboard/top-instagram");
//   return res.data;
// };

// export const getTopPositive = async () => {
//   const res = await API.get("/dashboard/top-positive");
//   return res.data;
// };

// export const getTopNegative = async () => {
//   const res = await API.get("/dashboard/top-negative");
//   return res.data;
// };










import axios from "axios";

const API_URL = "http://127.0.0.1:8000";

export const getDashboardOverview = async () => {
  const response = await axios.get(
    `${API_URL}/dashboard/overview`
  );

  return response.data;
};
// // import React from "react";

// // export default function DummyUI() {
// //   const imageUrl = "https://media.sproutsocial.com/uploads/2023/01/Sprout-listening-pie-chart.png";

// //   return (
// //     <div
// //       style={{
// //         width: "100%",
// //         minHeight: "100vh",
// //         display: "flex",
// //         justifyContent: "center",
// //         alignItems: "center",
// //         backgroundColor: "#f5f5f5",
// //       }}
// //     >
// //       <img
// //         src={imageUrl}
// //         alt="UI Mockup"
// //         style={{
// //           maxWidth: "100%",
// //           maxHeight: "100vh",
// //           objectFit: "contain",
// //         }}
// //       />
// //     </div>
// //   );
// // }








// import { useEffect, useState } from "react";

// import {
//   getSummary,
//   getPlatforms,
//   getSentiment,
//   getLatest,
// } from "../services/dashboardApi";

// import {
//   PieChart,
//   Pie,
//   Cell,
//   Tooltip,
//   ResponsiveContainer,
//   BarChart,
//   Bar,
//   XAxis,
//   YAxis,
//   CartesianGrid,
// } from "recharts";

// import {
//   Database,
//   Globe,
//   Smile,
//   Frown,
//   MinusCircle,
// } from "lucide-react";

// export default function Dashboard() {
//   const [summary, setSummary] = useState({});
//   const [platforms, setPlatforms] = useState([]);
//   const [sentiment, setSentiment] = useState([]);
//   const [latest, setLatest] = useState([]);

//   const [loading, setLoading] = useState(true);
//   const [error, setError] = useState("");

//   const COLORS = [
//     "#3b82f6",
//     "#22c55e",
//     "#f59e0b",
//     "#ef4444",
//     "#8b5cf6",
//     "#06b6d4",
//   ];

//   useEffect(() => {
//     loadData();
//   }, []);

//   const loadData = async () => {
//     try {
//       setLoading(true);

//       const summaryData = await getSummary();
//       const platformData = await getPlatforms();
//       const sentimentData = await getSentiment();
//       const latestData = await getLatest();

//       console.log(summaryData);
//       console.log(platformData);
//       console.log(sentimentData);
//       console.log(latestData);

//       setSummary(summaryData);
//       setPlatforms(platformData);
//       setSentiment(sentimentData);
//       setLatest(latestData);
//     } catch (err) {
//       console.error(err);
//       setError("Failed to load dashboard data");
//     } finally {
//       setLoading(false);
//     }
//   };

//   if (loading) {
//     return (
//       <div className="p-10 text-center text-xl">
//         Loading Dashboard...
//       </div>
//     );
//   }

//   if (error) {
//     return (
//       <div className="p-10 text-red-500 text-center">
//         {error}
//       </div>
//     );
//   }

//   return (
//     <div className="bg-gray-100 min-h-screen p-6">

//       {/* Header */}

//       <div className="mb-8">
//         <h1 className="text-4xl font-bold">
//           Social Media Listening Dashboard
//         </h1>

//         <p className="text-gray-500 mt-2">
//           Unified view of News, Reviews, Instagram and YouTube
//         </p>
//       </div>

//       {/* KPI Cards */}

//       <div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-5 gap-4 mb-8">

//         <div className="bg-white rounded-xl shadow p-5">
//           <Database size={30} />
//           <p className="text-gray-500 mt-2">
//             Total Records
//           </p>
//           <h2 className="text-3xl font-bold">
//             {summary.total_records || 0}
//           </h2>
//         </div>

//         <div className="bg-white rounded-xl shadow p-5">
//           <Globe size={30} />
//           <p className="text-gray-500 mt-2">
//             Platforms
//           </p>
//           <h2 className="text-3xl font-bold">
//             {summary.total_platforms || 0}
//           </h2>
//         </div>

//         <div className="bg-white rounded-xl shadow p-5">
//           <Smile size={30} />
//           <p className="text-gray-500 mt-2">
//             Positive
//           </p>
//           <h2 className="text-3xl font-bold text-green-600">
//             {summary.positive || 0}
//           </h2>
//         </div>

//         <div className="bg-white rounded-xl shadow p-5">
//           <Frown size={30} />
//           <p className="text-gray-500 mt-2">
//             Negative
//           </p>
//           <h2 className="text-3xl font-bold text-red-600">
//             {summary.negative || 0}
//           </h2>
//         </div>

//         <div className="bg-white rounded-xl shadow p-5">
//           <MinusCircle size={30} />
//           <p className="text-gray-500 mt-2">
//             Neutral
//           </p>
//           <h2 className="text-3xl font-bold text-yellow-600">
//             {summary.neutral || 0}
//           </h2>
//         </div>

//       </div>

//       {/* Charts */}

//       <div className="grid grid-cols-1 lg:grid-cols-2 gap-6 mb-8">

//         {/* Platform Chart */}

//         <div className="bg-white rounded-xl shadow p-5">

//           <h2 className="text-xl font-semibold mb-4">
//             Platform Distribution
//           </h2>

//           <ResponsiveContainer width="100%" height={350}>
//             <BarChart data={platforms}>
//               <CartesianGrid strokeDasharray="3 3" />
//               <XAxis dataKey="platform" />
//               <YAxis />
//               <Tooltip />
//               <Bar dataKey="count" />
//             </BarChart>
//           </ResponsiveContainer>

//         </div>

//         {/* Sentiment Chart */}

//         <div className="bg-white rounded-xl shadow p-5">

//           <h2 className="text-xl font-semibold mb-4">
//             Sentiment Distribution
//           </h2>

//           <ResponsiveContainer width="100%" height={350}>

//             <PieChart>

//               <Pie
//                 data={sentiment}
//                 dataKey="count"
//                 nameKey="sentiment"
//                 outerRadius={120}
//                 label
//               >
//                 {sentiment.map((entry, index) => (
//                   <Cell
//                     key={index}
//                     fill={COLORS[index % COLORS.length]}
//                   />
//                 ))}
//               </Pie>

//               <Tooltip />

//             </PieChart>

//           </ResponsiveContainer>

//         </div>

//       </div>

//       {/* Latest Records */}

//       <div className="bg-white rounded-xl shadow p-5">

//         <div className="flex justify-between items-center mb-4">

//           <h2 className="text-xl font-semibold">
//             Latest Records
//           </h2>

//           <span className="text-gray-500">
//             Showing {latest.length} records
//           </span>

//         </div>

//         <div className="overflow-x-auto">

//           <table className="min-w-full border">

//             <thead>

//               <tr className="bg-gray-100">

//                 <th className="p-3 border text-left">
//                   Platform
//                 </th>

//                 <th className="p-3 border text-left">
//                   Connector
//                 </th>

//                 <th className="p-3 border text-left">
//                   Source File
//                 </th>

//               </tr>

//             </thead>

//             <tbody>

//               {latest.map((row, index) => (

//                 <tr
//                   key={index}
//                   className="hover:bg-gray-50"
//                 >

//                   <td className="p-3 border">
//                     {row.platform || "-"}
//                   </td>

//                   <td className="p-3 border">
//                     {row.connector_name || "-"}
//                   </td>

//                   <td className="p-3 border">
//                     {row.source_file || "-"}
//                   </td>

//                 </tr>

//               ))}

//             </tbody>

//           </table>

//         </div>

//       </div>

//     </div>
//   );
// }







































import { useEffect, useState } from "react";
import axios from "axios";

import {
  PieChart,
  Pie,
  Cell,
  Tooltip,
  Legend,
  ResponsiveContainer,
  BarChart,
  Bar,
  XAxis,
  YAxis,
  CartesianGrid,
} from "recharts";

import "../styles/Dashboard.css";

// const API = "http://127.0.0.1:8000/dashboard";
const API =https://sml-backend-agdr.onrender.com/
const COLORS = [
  "#2563eb",
  "#10b981",
  "#f59e0b",
  "#ef4444",
  "#8b5cf6",
  "#06b6d4",
  "#f97316",
];

export default function Dashboard() {
const [overview, setOverview] = useState({});

const [filterOptions, setFilterOptions] = useState({
  platforms: [],
  sentiments: [],
  brands: []
});

const [platforms, setPlatforms] = useState([]);
const [sentiments, setSentiments] = useState([]);

const [brands, setBrands] = useState([]);
const [hashtags, setHashtags] = useState([]);
const [keywords, setKeywords] = useState([]);

const [youtube, setYoutube] = useState([]);
const [instagram, setInstagram] = useState([]);

const [positiveMentions, setPositiveMentions] = useState([]);
const [negativeMentions, setNegativeMentions] = useState([]);
const [latestRecords, setLatestRecords] = useState([]);

const [loading, setLoading] = useState(true);

const [filters, setFilters] = useState({
  platform: "",
  sentiment: "",
  brand: "",
  keyword: ""
});

  useEffect(() => {
    loadDashboard();
  }, [filters]);

  useEffect(() => {

    loadFilterOptions();

  }, []);

async function loadFilterOptions() {

  try {

    const res = await axios.get(
      `${API}/filter-options`
    );

    setFilterOptions(
      res.data
    );

  } catch (err) {

    console.log(err);

  }

}


async function loadDashboard() {

  try {

    setLoading(true);

    const params = {
      platform: filters.platform || undefined,
      sentiment: filters.sentiment || undefined,
      keyword: filters.keyword || undefined,
    };

    const [
      summaryRes,
      platformRes,
      sentimentRes,
    ] = await Promise.all([
      axios.get(`${API}/summary`, { params }),
      axios.get(`${API}/platforms`, { params }),
      axios.get(`${API}/sentiment`, { params }),
    ]);

    setOverview(summaryRes.data);
    setPlatforms(platformRes.data);
    setSentiments(sentimentRes.data);

    // const overviewRes = await axios.get(`${API}/overview`);
    const overviewRes =
      await axios.get(
        `${API}/overview`,
        {
          params: filters
        }
      );
    const data = overviewRes.data;

    setBrands((data.brands || []).slice(0, 10));
    setHashtags((data.hashtags || []).slice(0, 10));
    setKeywords((data.keywords || []).slice(0, 10));

    setYoutube((data.top_youtube || []).slice(0, 10));
    setInstagram((data.top_instagram || []).slice(0, 10));

    setPositiveMentions(
      (data.top_positive || []).slice(0, 20)
    );

    setNegativeMentions(
      (data.top_negative || []).slice(0, 20)
    );

    setLatestRecords(
      (data.latest || []).slice(0, 50)
    );

  } catch (error) {

    console.log(error);

  } finally {

    setLoading(false);

  }
}
const formatNumber = (value) => {
  if (!value) return "0";
  return Number(value).toLocaleString();
};

const truncate = (text, len = 100) => {
  if (!text) return "";
  return text.length > len
    ? text.substring(0, len) + "..."
    : text;
};

  return (
    <div className="dashboard-container">

    <h1 className="dashboard-title">
      Executive Brand Insights Dashboard
    </h1>

    <p className="dashboard-subtitle">
      Monitor Conversations, Sentiment, Reach & Reputation Across Digital Channels
    </p>
      <div className="filter-section">

      <select
        value={filters.platform}
        onChange={(e) =>
          setFilters({
            ...filters,
            platform: e.target.value
          })
        }
      >
        <option value="">
          All Platforms
        </option>

        {filterOptions.platforms.map((p, i) => (
          <option
            key={i}
            value={p}
          >
            {p}
          </option>
        ))}

      </select>

      <select
        value={filters.sentiment}
        onChange={(e) =>
          setFilters({
            ...filters,
            sentiment: e.target.value
          })
        }
      >
        {filterOptions.sentiments.map(
            (item, i) => (
              <option
                key={i}
                value={item}
              >
                {item}
              </option>
            )
          )}

        {/* <option value="Positive">
          Positive
        </option>

        <option value="Negative">
          Negative
        </option>

        <option value="Neutral">
          Neutral
        </option> */}

      </select>
      {/* <select
        value={filters.brand}
        onChange={(e) =>
          setFilters({
            ...filters,
            brand: e.target.value
          })
        }
        >

        <option value="">
          All Brands
        </option>

        {filterOptions.brands.map(
          (brand, i) => (
            <option
              key={i}
              value={brand}
            >
              {brand}
            </option>
          )
        )}

      </select> */}

      <input
        type="text"
        placeholder="Search keyword..."
        value={filters.keyword}
        onChange={(e) =>
          setFilters({
            ...filters,
            keyword: e.target.value
          })
        }
      />
      <button
        className="reset-btn"
        onClick={() =>
          setFilters({
            platform: "",
            sentiment: "",
            brand: "",
            keyword: ""
          })
        }
      >
        Reset Filters
      </button>

    </div>

      {/* KPI CARDS */}

      <div className="kpi-grid">

        <div className="kpi-card">
          <h3>Total Records</h3>
          <h2>{formatNumber(overview.total_records)}</h2>
        </div>

        <div className="kpi-card">
          <h3>Platforms</h3>
          <h2>{formatNumber(overview.total_platforms)}</h2>
        </div>

        <div className="kpi-card positive">
          <h3>Positive</h3>
          <h2>{formatNumber(overview.positive)}</h2>
        </div>

        <div className="kpi-card negative">
          <h3>Negative</h3>
          <h2>{formatNumber(overview.negative)}</h2>
        </div>

        <div className="kpi-card neutral">
          <h3>Neutral</h3>
          <h2>{formatNumber(overview.neutral)}</h2>
        </div>

      </div>

      {/* CHART ROW 1 */}

      <div className="chart-row">

        <div className="chart-card">

          <h3>Platform Distribution</h3>

          <ResponsiveContainer width="100%" height={350}>
            <PieChart>
              <Pie
                data={platforms}
                dataKey="count"
                nameKey="platform"
                outerRadius={120}
                label
              >
                {platforms.map((entry, index) => (
                  <Cell
                    key={index}
                    fill={COLORS[index % COLORS.length]}
                  />
                ))}
              </Pie>

              <Tooltip />
              <Legend />
            </PieChart>
          </ResponsiveContainer>

        </div>

        <div className="chart-card">

          <h3>Sentiment Distribution</h3>

          <ResponsiveContainer width="100%" height={350}>
            <PieChart>

              <Pie
                data={sentiments}
                dataKey="count"
                nameKey="sentiment"
                innerRadius={70}
                outerRadius={120}
                label
              >
                {sentiments.map((entry, index) => (
                  <Cell
                    key={index}
                    fill={COLORS[index % COLORS.length]}
                  />
                ))}
              </Pie>

              <Tooltip />
              <Legend />

            </PieChart>
          </ResponsiveContainer>

        </div>

      </div>

      {/* CHART ROW 2 */}

      <div className="chart-row">

        <div className="chart-card">

          <h3>Top Brands</h3>

          <ResponsiveContainer width="100%" height={350}>

            <BarChart data={brands}>

              <CartesianGrid strokeDasharray="3 3" />

              <XAxis dataKey="brand" />

              <YAxis />

              <Tooltip />

              <Bar dataKey="count" fill="#064581"/>

            </BarChart>

          </ResponsiveContainer>

        </div>

        <div className="chart-card">

          <h3>Top Hashtags</h3>

          <ResponsiveContainer width="100%" height={350}>

            <BarChart data={hashtags}>

              <CartesianGrid strokeDasharray="3 3" />

              <XAxis dataKey="hashtag" />

              <YAxis />

              <Tooltip />

              <Bar dataKey="count" fill="#09606b"/>

            </BarChart>

          </ResponsiveContainer>

        </div>

      </div>

      {/* KEYWORDS */}

      <div className="chart-card full-width">

        <h3>Top Keywords</h3>

        <ResponsiveContainer width="100%" height={350}>

          <BarChart data={keywords}>

            <CartesianGrid strokeDasharray="3 3" />

            <XAxis dataKey="keyword" />

            <YAxis />

            <Tooltip />

            <Bar dataKey="count" fill="#9ca054"/>

          </BarChart>

        </ResponsiveContainer>

      </div>

      {/* YOUTUBE */}

      <div className="table-card">

        <h3>Top YouTube Videos</h3>

        <table>

          <thead>
            <tr>
              <th>Video</th>
              <th>Channel</th>
              <th>Views</th>
              <th>Likes</th>
              <th>Comments</th>
            </tr>
          </thead>

          <tbody>

            {youtube.map((item, index) => (

              <tr key={index}>
                <td>{item.video_title}</td>
                <td>{item.channel_name}</td>
                <td>{item.view_count_numeric}</td>
                <td>{item.like_count_numeric}</td>
                <td>{item.comment_count_numeric}</td>
              </tr>

            ))}

          </tbody>

        </table>

      </div>

      {/* INSTAGRAM */}

      <div className="table-card">

        <h3>Top Instagram Posts</h3>

        <table>

          <thead>
            <tr>
              <th>Caption</th>
              <th>Engagement</th>
              <th>Likes</th>
              <th>Comments</th>
            </tr>
          </thead>

          <tbody>

            {instagram.map((item, index) => (

              <tr key={index}>
                <td>{item.caption}</td>
                <td>{item.engagement}</td>
                <td>{item.like_count}</td>
                <td>{item.comments_count}</td>
              </tr>

            ))}

          </tbody>

        </table>

      </div>

    </div>
  );
}

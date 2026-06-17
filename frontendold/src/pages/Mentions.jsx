import React, { useEffect, useState } from "react";
import {
  FaInstagram,
  FaYoutube,
  FaNewspaper,
  FaBullhorn,
  FaStar
} from "react-icons/fa";
import {
  ResponsiveContainer,
  PieChart,
  Pie,
  Tooltip,
  Cell,
  LineChart,
  Line,
  XAxis,
  YAxis,
  CartesianGrid
} from "recharts";
import api from "../services/api";
import "../styles/Mentions.css";

export default function Mentions() {

  const [activePlatform, setActivePlatform] =
    useState("instagram");

  const [selectedKeyword, setSelectedKeyword] =
    useState("");

  const [keywords, setKeywords] =
    useState([]);

  const [overview, setOverview] =
    useState({});

  const [charts, setCharts] =
    useState({});

  // const [content, setContent] =
  //   useState([]);
  const [topContent, setTopContent] =
  useState([]);

  const [topPositive, setTopPositive] =
    useState([]);

  const [topNegative, setTopNegative] =
    useState([]);

  // =====================================
  // PLATFORMS
  // =====================================

  const platforms = [
    {
      id: "instagram",
      name: "Instagram",
      icon: <FaInstagram color="#E4405F" />
    },
    {
      id: "youtube",
      name: "YouTube",
      icon: <FaYoutube color="#FF0000" />
    },
    {
      id: "news",
      name: "News",
      icon: <FaNewspaper color="#3B82F6" />
    },
    {
      id: "campaignindia",
      name: "Campaign India",
      icon: <FaBullhorn color="#F59E0B" />
    },
    {
      id: "reviews",
      name: "Reviews",
      icon: <FaStar color="#FACC15" />
    }
  ];

  // =====================================
  // LOAD KEYWORDS
  // =====================================

  useEffect(() => {

    loadKeywords();

  }, [activePlatform]);

  const loadKeywords = async () => {

    try {

      const res = await api.get(
        `/mentions/keywords?platform=${activePlatform}`
      );

      setKeywords(res.data);

      if (res.data.length > 0) {

        loadMentionData(
          res.data[0].keyword
        );

      } else {

        setSelectedKeyword("");
        setOverview({});
        setCharts({});
        setContent([]);

      }

    } catch (err) {

      console.error(err);

    }

  };

  // =====================================
  // LOAD INSIGHTS
  // =====================================

  const loadMentionData = async (
    keyword
  ) => {

    try {

      setSelectedKeyword(keyword);

      const overviewRes =
        await api.get(
          `/mentions/overview?platform=${activePlatform}&keyword=${keyword}`
        );

      const chartRes =
        await api.get(
          `/mentions/charts?platform=${activePlatform}&keyword=${keyword}`
        );

      const contentRes =
        await api.get(
          `/mentions/top-content?platform=${activePlatform}&keyword=${keyword}`
        );

      const positiveRes =
        await api.get(
          `/mentions/top-positive?platform=${activePlatform}&keyword=${keyword}`
        );

      const negativeRes =
        await api.get(
          `/mentions/top-negative?platform=${activePlatform}&keyword=${keyword}`
        );

      setOverview(
        overviewRes.data
      );

      setCharts(
        chartRes.data
      );

      // setContent(
      //   contentRes.data
      // );

      setTopContent(
        contentRes.data.slice(0, 10)
      );

      setTopPositive(
        positiveRes.data
      );

      setTopNegative(
        negativeRes.data
      );

    } catch (err) {

      console.error(err);

    }

  };

  // =====================================
  // CONTENT TEXT
  // =====================================

  const getContentText = (row) => {

    return (
      row.title ||
      row.video_title ||
      row.caption ||
      row.review_title ||
      row.comment_text ||
      row.content ||
      ""
    );

  };

  const getSource = (row) => {

    return (
      row.source ||
      row.channel_name ||
      row.account_username ||
      row.reviewer ||
      ""
    );

  };

  const getDate = (row) => {

    const dateValue =
      row.published_at ||
      row.timestamp ||
      row.post_timestamp ||
      row.published_date;

    if (!dateValue) return "-";

    try {

      const date = new Date(dateValue);

      return date.toLocaleString(
        "en-IN",
        {
          day: "2-digit",
          month: "short",
          year: "numeric",
          hour: "2-digit",
          minute: "2-digit"
        }
      );

    } catch {

      return dateValue;

    }

  };
  const renderTable = (title, rows) => (

  <div className="mentions-table-container">

    <div className="table-header">
      <h3>{title}</h3>
    </div>

    <table className="mentions-table">

      <thead>

        <tr>

          <th>#</th>

          <th>Platform</th>

          <th>Title / Content</th>

          <th>Source</th>

          <th>Sentiment</th>

          <th>Date</th>

        </tr>

      </thead>

      <tbody>

        {rows.map((row, index) => (

          <tr key={index}>

            <td>{index + 1}</td>

            <td>{row.platform}</td>

            <td>{getContentText(row)}</td>

            <td>{getSource(row)}</td>

            <td>

              <span
                className={`sentiment-badge ${
                  (
                    row.sentiment_label ||
                    row.sentiment ||
                    ""
                  ).toLowerCase()
                }`}
              >

                {
                  row.sentiment_label ||
                  row.sentiment ||
                  "-"
                }

              </span>

            </td>

            <td>{getDate(row)}</td>
            

          </tr>

        ))}

      </tbody>

    </table>

  </div>

);

  // =====================================
  // UI
  // =====================================
  const COLORS = [
    "#22c55e",
    "#f59e0b",
    "#ef4444",
    "#3b82f6"
  ];
  return (

    <div className="mentions-page">

      {/* HEADER */}

      <div className="mentions-header">

        <h2>
          Mentions & Insights
        </h2>

        <p>
          Explore platform specific
          conversations, mentions,
          articles, reviews and videos.
        </p>

      </div>

      {/* PLATFORM TABS */}

      <div className="platform-tabs">

        {
          platforms.map(
            (platform) => (

              <div
                key={platform.id}
                className={`platform-tab ${
                  activePlatform === platform.id
                    ? "active"
                    : ""
                }`}
                onClick={() => {

                  setActivePlatform(
                    platform.id
                  );

                }}
              >

                <div className="platform-icon">
                  {platform.icon}
                </div>

                <div>
                  {platform.name}
                </div>

              </div>

            )
          )
        }

      </div>

      {/* KEYWORDS */}

      <div className="keywords-section">

        <h3>
          Keywords / Hashtags
        </h3>

        <div className="keyword-grid">

          {
            keywords.map(
              (item, index) => (

                <div
                  key={index}
                  className={`keyword-card ${
                    selectedKeyword ===
                    item.keyword
                      ? "selected"
                      : ""
                  }`}
                  onClick={() =>
                    loadMentionData(
                      item.keyword
                    )
                  }
                >

                  <h4>
                    {item.keyword}
                  </h4>

                  <span>
                    {item.count} Records
                  </span>

                </div>

              )
            )
          }

        </div>

      </div>

      {/* KPI */}

      <div className="kpi-grid">

        <div className="kpi-card">

          <h4>
            Total Mentions
          </h4>

          <h2>
            {
              overview.total_mentions || 0
            }
          </h2>

        </div>

        <div className="kpi-card">

          <h4>
            Positive
          </h4>

          <h2>
            {overview.positive || 0}
          </h2>

        </div>

        <div className="kpi-card">

          <h4>
            Neutral
          </h4>

          <h2>
            {overview.neutral || 0}
          </h2>

        </div>

        <div className="kpi-card">

          <h4>
            Negative
          </h4>

          <h2>
            {overview.negative || 0}
          </h2>

        </div>

        <div className="kpi-card">

          <h4>
            Engagement
          </h4>

          <h2>
            {overview.engagement || 0}
          </h2>

        </div>

        <div className="kpi-card">

          <h4>
            Quality Score
          </h4>

          <h2>
            {
              overview.quality_score || 0
            }
          </h2>

        </div>

      </div>

      {/* CHART PLACEHOLDERS */}

      {/* <div className="charts-grid"> */}
      <div className="charts-grid">

        <div className="chart-box">

          <h3>Sentiment Distribution</h3>

          <ResponsiveContainer width="100%" height={300}>

            <PieChart>

              <Pie
                data={charts.sentiment || []}
                dataKey="value"
                nameKey="name"
                outerRadius={100}
                label
              >

                {(charts.sentiment || []).map(
                  (entry, index) => (

                    <Cell
                      key={index}
                      fill={
                        COLORS[
                          index %
                          COLORS.length
                        ]
                      }
                    />

                  )
                )}

              </Pie>

              <Tooltip />

            </PieChart>

          </ResponsiveContainer>

        </div>

        <div className="chart-box">

          <h3>Mention Trend</h3>

          <ResponsiveContainer width="100%" height={300}>

            <LineChart
              data={charts.trend || []}
            >

              <CartesianGrid strokeDasharray="3 3" />

              <XAxis dataKey="date" />

              <YAxis />

              <Tooltip />

              <Line
                type="monotone"
                dataKey="count"
                stroke="#3b82f6"
              />

            </LineChart>

          </ResponsiveContainer>

        </div>

      </div>

      {/* CONTENT TABLE */}
      <div className="tables-stack">

        {
          renderTable(
            "Top Mentions",
            topContent
          )
        }

        {
          renderTable(
            "Top Positive Mentions",
            topPositive
          )
        }

        {
          renderTable(
            "Top Negative Mentions",
            topNegative
          )
        }

      </div>

      

    </div>

  );

}